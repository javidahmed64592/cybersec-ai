"""Unit tests for the cybersec_ai.models.chatbot module."""

from unittest.mock import MagicMock

from cybersec_ai.models.chatbot import Chatbot


class TestChatbot:
    """Test cases for the Chatbot class."""

    def test_init(self, mock_chatbot: Chatbot) -> None:
        """Test initialization of the Chatbot."""
        assert mock_chatbot.model_name == "test_model"

    def test_query_success(self, mock_chatbot: Chatbot, mock_ollama_chat: MagicMock) -> None:
        """Test querying the chatbot with a valid prompt."""
        test_response = "This is a test response."
        mock_ollama_chat.return_value.message.content = test_response
        response = mock_chatbot.query("Hello, model!")
        assert response == test_response

    def test_query_failure(self, mock_chatbot: Chatbot, mock_ollama_chat: MagicMock) -> None:
        """Test querying the chatbot when the model fails to respond."""
        mock_ollama_chat.return_value.message.content = None
        response = mock_chatbot.query("Hello, model!")
        assert response == "Failed to get a response from the model."
