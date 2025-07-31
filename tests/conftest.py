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
