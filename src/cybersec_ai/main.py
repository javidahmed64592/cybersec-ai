"""Example main module."""

import logging
import subprocess
import sys
from collections.abc import Callable

import ollama

logging.basicConfig(
    format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s", datefmt="%d/%m/%Y | %H:%M:%S", level=logging.INFO
)
logger = logging.getLogger(__name__)


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
    args = []
    if options:
        args.extend(options)
    args.append(target)
    return args


@CommandLineTool("nikto")
def run_nikto(target: str, options: list[str] | None = None) -> list[str]:
    """Run nikto with the specified target and options."""
    args = []
    if options:
        args.extend(options)
    args.append(target)
    return args


@CommandLineTool("dirb")
def run_dirb(target: str, options: list[str] | None = None) -> list[str]:
    """Run dirb with the specified target and options."""
    args = []
    if options:
        args.extend(options)
    args.append(target)
    return args


def query_llm(prompt: str) -> str:
    """Query the language model with a prompt."""
    response = ollama.chat(model="gemma:2b", messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]


def scan_network() -> list[str]:
    """Scan the network for the specified target."""
    target = sys.argv[1]
    if not target:
        msg = "Target must be specified as a command line argument."
        raise ValueError(msg)

    logger.info("Scanning target: %s", target)

    # Run nmap scan with version detection and all ports
    logger.info("Running nmap scan...")
    nmap_output = run_nmap(target, ["-sV", "-p-"])

    # Run nikto scan for web vulnerabilities
    logger.info("Running nikto scan...")
    nikto_output = run_nikto(target, ["-h", target])

    # Run dirb scan for directory brute-forcing
    logger.info("Running dirb scan...")
    dirb_output = run_dirb(f"http://{target}")

    prompt = f"""
    You're a cybersecurity expert. Analyze the following scan results:

    nmap Output:
    {nmap_output}

    nikto Output:
    {nikto_output}

    dirb Output:
    {dirb_output}

    Generate a vulnerability report listing suspicious ports, risky directories, and potential exposures.
    """
    logger.info("Querying LLM for vulnerability report...")
    report = query_llm(prompt)

    logger.info("Generated Vulnerability Report:")
    logger.info(report)


def main() -> None:
    """Run application main entry."""
    # Send a prompt to the model
    print("User: What is port scanning in cybersecurity?")
    response = ollama.chat(
        model="gemma:2b", messages=[{"role": "user", "content": "What is port scanning in cybersecurity?"}]
    )

    # Print the model's reply
    print("Bot:", response["message"]["content"])
