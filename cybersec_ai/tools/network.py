"""Module with command line tools for network scanning and enumeration."""

from cybersec_ai.models.command_line_tool import CommandLineTool


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


@CommandLineTool("gobuster")
def run_gobuster(target: str, options: list[str] | None = None) -> list[str]:
    """Run gobuster for directory brute-forcing with specified target and options."""
    args = options or []
    return ["dir", "-u", target, *args]
