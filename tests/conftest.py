"""Pytest fixtures for CyberSec AI unit tests."""

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest

from cybersec_ai.models.chatbot import Chatbot


# Chatbot fixtures
@pytest.fixture
def mock_ollama_chat() -> Generator[MagicMock, None, None]:
    """Mock the ollama.chat function."""
    with patch("ollama.chat") as mock_chat:
        yield mock_chat


@pytest.fixture
def mock_chatbot(mock_ollama_chat: MagicMock) -> Chatbot:
    """Fixture for creating a Chatbot instance."""
    return Chatbot(model_name="test_model")


# CommandLineTool fixtures
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


# Main fixtures
@pytest.fixture
def mock_get_output_dir() -> Generator[MagicMock, None, None]:
    """Mock the get_output_dir function."""
    with patch("cybersec_ai.main.get_output_dir") as mock_get_dir:
        yield mock_get_dir


@pytest.fixture
def mock_write_to_txt_file() -> Generator[MagicMock, None, None]:
    """Mock the write_to_txt_file function."""
    with patch("cybersec_ai.main.write_to_txt_file") as mock_write:
        yield mock_write


@pytest.fixture
def mock_chatbot_query() -> Generator[MagicMock, None, None]:
    """Mock the Chatbot.query method."""
    with patch("cybersec_ai.main.Chatbot.query") as mock_query:
        yield mock_query


# scan-network fixtures
@pytest.fixture
def mock_run_gobuster() -> Generator[MagicMock, None, None]:
    """Mock the run_gobuster function."""
    with patch("cybersec_ai.main.run_gobuster") as mock_gobuster:
        yield mock_gobuster


@pytest.fixture
def mock_run_nikto() -> Generator[MagicMock, None, None]:
    """Mock the run_nikto function."""
    with patch("cybersec_ai.main.run_nikto") as mock_nikto:
        yield mock_nikto


@pytest.fixture
def mock_run_nmap() -> Generator[MagicMock, None, None]:
    """Mock the run_nmap function."""
    with patch("cybersec_ai.main.run_nmap") as mock_nmap:
        yield mock_nmap


@pytest.fixture
def mock_prompt_network_enumeration() -> Generator[MagicMock, None, None]:
    """Mock the PromptFactory.create_network_enumeration_prompt function."""
    with patch("cybersec_ai.main.PromptFactory.create_network_enumeration_prompt") as mock_prompt:
        yield mock_prompt


@pytest.fixture
def mock_prompt_vulnerability_report() -> Generator[MagicMock, None, None]:
    """Mock the PromptFactory.create_vulnerability_report_prompt function."""
    with patch("cybersec_ai.main.PromptFactory.create_vulnerability_report_prompt") as mock_prompt:
        yield mock_prompt
