"""Utility functions for the CyberSec AI application."""

import os


def get_root_dir() -> str:
    """Get the root directory of the CyberSec AI application."""
    return os.getenv("CYBERSEC_AI_ROOT_DIR", ".")


def get_output_dir(target: str) -> str:
    """Get the output directory for scan results based on the target."""
    root_dir = get_root_dir()
    return os.path.join(root_dir, "output", f"{target.replace('.', '_')}_scan")


def write_to_txt_file(contents: str, filename: str, output_dir: str) -> None:
    """Save the output of a command line tool to a file."""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w") as f:
        f.write(contents)
