"""Example main module."""

import subprocess
import sys
from typing import Callable

import ollama


class SecurityTool:
    """Class-based decorator for creating security tool functions."""

    def __init__(self, command: str, default_options: list[str] | None = None, timeout: int = 30) -> None:
        """Initialize the security tool decorator."""
        self.command = command
        self.default_options = default_options or []
        self.timeout = timeout

    def __call__(self, func: Callable) -> Callable:
        """Call the function with the command and options."""

        def wrapper(*args: list[str], **kwargs: dict[str, str]) -> str:
            """Execute the command with provided options."""
            # Build command
            command = [self.command, *self.default_options]

            # Get additional arguments from function
            additional_args = func(*args, **kwargs)
            if additional_args:
                command.extend(additional_args if isinstance(additional_args, list) else [additional_args])

            # You could add timeout handling here
            result = subprocess.run(command, check=False, capture_output=True, text=True)
            return result.stdout

        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper


@SecurityTool("nmap")
def run_nmap(target: str, options: list[str] | None = None) -> list[str]:
    """Run nmap with the specified target and options."""
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

    nmap_output = run_nmap(target, ["-sV", "-p-"])
    prompt = f"""
    You're a cybersecurity expert. Analyze the following scan results:
    NMAP Output:
    {nmap_output}

    Generate a vulnerability report listing suspicious ports, risky directories, and potential exposures.
    """
    report = query_llm(prompt)
    print("Generated Vulnerability Report:")
    print(report)


def main() -> None:
    """Run application main entry."""
    # Send a prompt to the model
    print("User: What is port scanning in cybersecurity?")
    response = ollama.chat(
        model="gemma:2b", messages=[{"role": "user", "content": "What is port scanning in cybersecurity?"}]
    )

    # Print the model's reply
    print("Bot:", response["message"]["content"])
