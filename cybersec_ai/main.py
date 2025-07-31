"""Main entry point for the CyberSec AI application."""

import logging
import sys

from cybersec_ai.models.chatbot import Chatbot
from cybersec_ai.models.prompt_factory import PromptFactory
from cybersec_ai.tools.network import run_gobuster, run_nikto, run_nmap
from cybersec_ai.utils import get_output_dir, write_to_txt_file

logging.basicConfig(
    format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s", datefmt="%d/%m/%Y | %H:%M:%S", level=logging.INFO
)
logger = logging.getLogger(__name__)
chatbot = Chatbot(model_name="gemma:2b")


def scan_network() -> None:
    """Scan the network for the specified target."""
    target = sys.argv[1]
    if not target:
        msg = "Usage: scan-network <target>"
        raise ValueError(msg)

    logger.info("Scanning target: %s", target)
    output_dir = get_output_dir(target)

    # Run nmap scan with version detection and all ports
    logger.info("Running nmap scan...")
    nmap_output = run_nmap(target, ["-sV", "-p-"])
    write_to_txt_file(nmap_output, "nmap_scan.txt", output_dir)

    # Run nikto scan for web vulnerabilities
    logger.info("Running nikto scan...")
    nikto_output = run_nikto(target, ["-h", target])
    write_to_txt_file(nikto_output, "nikto_scan.txt", output_dir)

    # Run gobuster scan for directory brute-forcing
    logger.info("Running gobuster scan...")
    gobuster_output = run_gobuster(f"http://{target}", ["-w", "/usr/share/wordlists/dirb/common.txt"])
    write_to_txt_file(gobuster_output, "gobuster_scan.txt", output_dir)

    # Query the LLM for port analysis and web application analysis
    logger.info("Creating prompts for LLM queries...")
    prompts_network_enumeration = PromptFactory.create_network_enumeration_prompt(
        nmap_output=nmap_output, nikto_output=nikto_output, gobuster_output=gobuster_output
    )

    logger.info("Querying LLM for port analysis...")
    port_analysis = chatbot.query(prompts_network_enumeration["port_analysis"])
    write_to_txt_file(port_analysis, "port_analysis.txt", output_dir)

    logger.info("Querying LLM for web application analysis...")
    web_app_analysis = chatbot.query(prompts_network_enumeration["web_app_analysis"])
    write_to_txt_file(web_app_analysis, "web_app_analysis.txt", output_dir)

    # Query the LLM for the vulnerability report
    logger.info("Creating prompt for vulnerability report...")
    prompt_vulnerability_report = PromptFactory.create_vulnerability_report_prompt(
        port_analysis=port_analysis, web_app_analysis=web_app_analysis
    )

    logger.info("Querying LLM for vulnerability report...")
    vulnerability_report = chatbot.query(prompt_vulnerability_report)
    write_to_txt_file(vulnerability_report, "vulnerability_report.txt", output_dir)

    # Success messages
    logger.info("Network scan completed successfully.")
    logger.info("Results saved in output directory: %s", output_dir)
    logger.info("Final vulnerability report:\n%s", vulnerability_report)
