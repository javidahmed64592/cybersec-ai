"""Example main module."""

import ollama


def main() -> None:
    """Run application main entry."""
    # Send a prompt to the model
    print("User: What is port scanning in cybersecurity?")
    response = ollama.chat(
        model="gemma:2b", messages=[{"role": "user", "content": "What is port scanning in cybersecurity?"}]
    )

    # Print the model's reply
    print("Bot:", response["message"]["content"])
