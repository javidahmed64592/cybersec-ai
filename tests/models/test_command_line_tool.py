"""Unit tests for the cybersec_ai.models.command_line_tool module."""

import subprocess
from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest

from cybersec_ai.models.command_line_tool import CommandLineTool

MOCK_COMMAND = "test_command"
MOCK_TIMEOUT = 5


@pytest.fixture
def mock_command_line_tool() -> CommandLineTool:
    """Fixture to create a CommandLineTool instance."""
    return CommandLineTool(command=MOCK_COMMAND, timeout=MOCK_TIMEOUT)


@pytest.fixture
def mock_command_line_tool_function(mock_command_line_tool: CommandLineTool) -> CommandLineTool:
    """Fixture to create a CommandLineTool function."""

    @mock_command_line_tool
    def mock_function(*args: list[str], **kwargs: dict[str, str]) -> str:
        return ["--option", "value"]

    return mock_function


@pytest.fixture
def mock_shutil_which() -> Generator[MagicMock, None, None]:
    """Mock shutil.which to simulate command availability."""
    with patch("shutil.which") as mock_which:
        yield mock_which


@pytest.fixture
def mock_subprocess_run() -> Generator[MagicMock, None, None]:
    """Mock subprocess.run to simulate command execution."""
    with patch("subprocess.run") as mock_run:
        yield mock_run


class TestCommandLineTool:
    """Tests for the CommandLineTool decorator."""

    def test_init(self, mock_command_line_tool: CommandLineTool) -> None:
        """Test the initialization of the CommandLineTool."""
        assert mock_command_line_tool.command == MOCK_COMMAND
        assert mock_command_line_tool.timeout == MOCK_TIMEOUT

    def test_call_command_not_found(
        self,
        mock_command_line_tool_function: CommandLineTool,
        mock_shutil_which: MagicMock,
        mock_subprocess_run: MagicMock,
    ) -> None:
        """Test the command not found scenario."""
        mock_shutil_which.return_value = None

        with pytest.raises(FileNotFoundError, match=f"Command '{MOCK_COMMAND}' not found in PATH."):
            mock_command_line_tool_function()

        mock_subprocess_run.assert_not_called()

    def test_call_command_success(
        self,
        mock_command_line_tool_function: CommandLineTool,
        mock_shutil_which: MagicMock,
        mock_subprocess_run: MagicMock,
    ) -> None:
        """Test the command execution success scenario."""
        mock_shutil_which.return_value = f"/path/to/{MOCK_COMMAND}"
        mock_subprocess_run.return_value.stdout = "Command executed successfully."

        result = mock_command_line_tool_function()

        assert result == "Command executed successfully."
        mock_subprocess_run.assert_called_once_with(
            [MOCK_COMMAND, "--option", "value"], check=True, capture_output=True, text=True, timeout=MOCK_TIMEOUT
        )

    def test_call_command_timeout(
        self,
        mock_command_line_tool_function: CommandLineTool,
        mock_shutil_which: MagicMock,
        mock_subprocess_run: MagicMock,
    ) -> None:
        """Test the command execution timeout scenario."""
        mock_shutil_which.return_value = f"/path/to/{MOCK_COMMAND}"
        mock_subprocess_run.side_effect = subprocess.TimeoutExpired(MOCK_COMMAND, MOCK_TIMEOUT)

        assert mock_command_line_tool_function() == f"Command '{MOCK_COMMAND}' timed out after {MOCK_TIMEOUT} seconds."

        mock_subprocess_run.assert_called_once_with(
            [MOCK_COMMAND, "--option", "value"], check=True, capture_output=True, text=True, timeout=MOCK_TIMEOUT
        )

    def test_call_command_failure(
        self,
        mock_command_line_tool_function: CommandLineTool,
        mock_shutil_which: MagicMock,
        mock_subprocess_run: MagicMock,
    ) -> None:
        """Test the command execution failure scenario."""
        mock_shutil_which.return_value = f"/path/to/{MOCK_COMMAND}"
        mock_subprocess_run.side_effect = subprocess.CalledProcessError(
            returncode=1, cmd=MOCK_COMMAND, stderr="Command failed with error."
        )

        result = mock_command_line_tool_function()

        assert result == "Command 'test_command' failed with error: Command failed with error."
        mock_subprocess_run.assert_called_once_with(
            [MOCK_COMMAND, "--option", "value"], check=True, capture_output=True, text=True, timeout=MOCK_TIMEOUT
        )
