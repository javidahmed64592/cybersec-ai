"""Chatbot module for interacting with Ollama models."""

import ollama


class Chatbot:
    """Chatbot class for interacting with the Ollama model."""

    def __init__(self, model_name: str = "gemma:2b") -> None:
        """Initialize the chatbot with a specific model."""
        self.model_name = model_name

    def query(self, prompt: str) -> str:
        """Query the chatbot with a prompt."""
        response = ollama.chat(model=self.model_name, messages=[{"role": "user", "content": prompt}])
        if reply := response.message.content:
            return reply
        return "Failed to get a response from the model."
