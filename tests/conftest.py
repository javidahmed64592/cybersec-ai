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
