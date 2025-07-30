"""Example main module."""

import logging
import os
import subprocess
import sys
from collections.abc import Callable

import ollama

logging.basicConfig(
    format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s", datefmt="%d/%m/%Y | %H:%M:%S", level=logging.INFO
)
logger = logging.getLogger(__name__)


def write_to_txt_file(contents: str, filename: str, output_dir: str) -> None:
    """Save the output of a command line tool to a file."""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w") as f:
        f.write(contents)


class CommandLineTool:
    """Class-based decorator for creating command line tool functions."""

    def __init__(self, command: str, default_options: list[str] | None = None, timeout: int = 30) -> None:
        """Initialize the command line tool decorator."""
        self.command = command
        self.default_options = default_options or []
        self.timeout = timeout

    def __call__(self, func: Callable) -> Callable:
        """Call the function with the command and options."""

        def wrapper(*args: list[str], **kwargs: dict[str, str]) -> str:
            """Execute the command with provided options."""
            command = [self.command, *self.default_options]

            if additional_args := func(*args, **kwargs):
                command.extend(additional_args if isinstance(additional_args, list) else [additional_args])

            # You could add timeout handling here
            result = subprocess.run(command, check=False, capture_output=True, text=True)
            return result.stdout

        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper


@CommandLineTool("nmap")
def run_nmap(target: str, options: list[str] | None = None) -> list[str]:
    """Run nmap with the specified target and options."""
    args = options or []
    return [*args, target]


@CommandLineTool("nikto")
def run_nikto(target: str, options: list[str] | None = None) -> list[str]:
    """Run nikto with the specified target and options."""
    args = options or []
    return [*args, target]


@CommandLineTool("dirb")
def run_dirb(target: str, options: list[str] | None = None) -> list[str]:
    """Run dirb with the specified target and options."""
    args = options or []
    return [*args, target]


def query_llm(prompt: str) -> str:
    """Query the language model with a prompt."""
    response = ollama.chat(model="gemma:2b", messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]


def scan_network() -> None:
    """Scan the network for the specified target."""
    target = sys.argv[1]
    if not target:
        msg = "Target must be specified as a command line argument."
        raise ValueError(msg)

    root_dir = os.getenv("CYBERSEC_AI_ROOT_DIR", ".")
    output_dir = os.path.join(root_dir, "output")

    logger.info("Scanning target: %s", target)

    # Run nmap scan with version detection and all ports
    logger.info("Running nmap scan...")
    nmap_output = run_nmap(target, ["-sV", "-p-"])
    write_to_txt_file(nmap_output, "nmap_scan.txt", output_dir)

    # Run nikto scan for web vulnerabilities
    logger.info("Running nikto scan...")
    nikto_output = run_nikto(target, ["-h", target])
    write_to_txt_file(nikto_output, "nikto_scan.txt", output_dir)

    # Run dirb scan for directory brute-forcing
    logger.info("Running dirb scan...")
    dirb_output = run_dirb(f"http://{target}")
    write_to_txt_file(dirb_output, "dirb_scan.txt", output_dir)

    prompt_port_analysis = f"""
    You're a cybersecurity expert. Analyze the following nmap scan results for the target.
    Identify any suspicious or vulnerable open ports and services.
    Note common misconfigurations and recommend security hardening steps.

    nmap Output:
    {nmap_output}
    """

    prompt_web_app_analysis = f"""
    You're a cybersecurity expert. Review the web application scan results for the following target.
    Determine any risky directories or known vulnerabilities.
    Highlight potential exploitation risks and suggest appropriate mitigations.

    Nikto Output:
    {nikto_output}

    Dirb Output:
    {dirb_output}
    """

    logger.info("Querying LLM for port analysis...")
    port_analysis = query_llm(prompt_port_analysis)
    write_to_txt_file(port_analysis, "port_analysis.txt", output_dir)

    logger.info("Querying LLM for web application analysis...")
    web_app_analysis = query_llm(prompt_web_app_analysis)
    write_to_txt_file(web_app_analysis, "web_app_analysis.txt", output_dir)

    prompt_vulnerability_report = f"""
    You're a cybersecurity expert.
    Based on the following analyses, create a comprehensive vulnerability report for the target system.
    Summarize the key findings from both the port and web application assessments, highlight critical risks, and provide
    actionable recommendations for remediation.

    Port Analysis:
    {port_analysis}

    Web Application Analysis:
    {web_app_analysis}
    """

    logger.info("Querying LLM for vulnerability report...")
    vulnerability_report = query_llm(prompt_vulnerability_report)
    write_to_txt_file(vulnerability_report, "vulnerability_report.txt", output_dir)

    logger.info("Network scan completed successfully.")
    logger.info("Results saved in output directory: %s", output_dir)


def main() -> None:
    """Run application main entry."""
    # Send a prompt to the model
    print("User: What is port scanning in cybersecurity?")
    response = ollama.chat(
        model="gemma:2b", messages=[{"role": "user", "content": "What is port scanning in cybersecurity?"}]
    )

    # Print the model's reply
    print("Bot:", response["message"]["content"])
