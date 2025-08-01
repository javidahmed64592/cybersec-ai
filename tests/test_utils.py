"""Unit tests for the cybersec_ai.utils module."""

import os
from unittest.mock import mock_open, patch

from cybersec_ai.utils import get_output_dir, get_root_dir, write_to_txt_file


class TestUtils:
    """Test suite for utility functions in cybersec_ai.utils."""

    def test_get_root_dir_env_not_set(self) -> None:
        """Test get_root_dir when CYBERSEC_AI_ROOT_DIR is not set."""
        assert get_root_dir() == "."

    def test_get_root_dir_env_set(self) -> None:
        """Test get_root_dir when CYBERSEC_AI_ROOT_DIR is set."""
        os.environ["CYBERSEC_AI_ROOT_DIR"] = "/test/root/dir"
        assert get_root_dir() == "/test/root/dir"

    def test_get_output_dir(self) -> None:
        """Test get_output_dir."""
        target = "123.123.123.123"
        assert get_output_dir(target) == os.path.join(get_root_dir(), "output", "123_123_123_123_scan")

    def test_write_to_txt_file(self) -> None:
        """Test write_to_txt_file."""
        contents = "Test content"
        filename = "test_output.txt"
        output_dir = "/test/output/dir"

        with patch("os.makedirs") as mock_makedirs, patch("builtins.open", mock_open()) as mock_file:
            write_to_txt_file(contents, filename, output_dir)

            mock_makedirs.assert_called_once_with(output_dir, exist_ok=True)
            mock_file.assert_called_once_with(os.path.join(output_dir, filename), "w")
            mock_file.return_value.write.assert_called_once_with(contents)
