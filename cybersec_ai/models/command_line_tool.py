"""Command line tool decorator for executing shell commands."""

import shutil
import subprocess
from collections.abc import Callable


class CommandLineTool:
    """Class-based decorator for creating command line tool functions."""

    def __init__(self, command: str, timeout: int = 300) -> None:
        """Initialize the command line tool decorator."""
        self.command = command
        self.timeout = timeout

    def __call__(self, func: Callable) -> Callable:
        """Call the function with the command and options."""

        def wrapper(*args: list[str], **kwargs: dict[str, str]) -> str:
            """Execute the command with provided options."""
            if not shutil.which(self.command):
                msg = f"Command '{self.command}' not found in PATH."
                raise FileNotFoundError(msg)

            command = [self.command]

            if additional_args := func(*args, **kwargs):
                command.extend(additional_args if isinstance(additional_args, list) else [additional_args])

            try:
                result = subprocess.run(command, check=False, capture_output=True, text=True, timeout=self.timeout)  # noqa: S603
            except subprocess.TimeoutExpired:
                return f"Command '{self.command}' timed out after {self.timeout} seconds."
            else:
                return result.stdout

        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper
