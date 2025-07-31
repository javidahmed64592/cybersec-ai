import shutil
import subprocess
from collections.abc import Callable


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
            if not shutil.which(self.command):
                msg = f"Command '{self.command}' not found in PATH."
                raise FileNotFoundError(msg)

            command = [self.command, *self.default_options]

            if additional_args := func(*args, **kwargs):
                command.extend(additional_args if isinstance(additional_args, list) else [additional_args])

            # You could add timeout handling here
            result = subprocess.run(command, check=False, capture_output=True, text=True)
            return result.stdout

        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper
