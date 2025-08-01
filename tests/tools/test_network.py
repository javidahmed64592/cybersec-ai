"""Unit tests for the cybersec_ai.tools.network module."""

from unittest.mock import MagicMock

from cybersec_ai.tools.network import run_gobuster, run_nikto, run_nmap


def test_run_nmap(mock_shutil_which: MagicMock, mock_subprocess_run: MagicMock) -> None:
    """Test the run_nmap function."""
    mock_shutil_which.return_value = "/path/to/nmap"
    mock_output = "Nmap scan results"
    mock_subprocess_run.return_value = MagicMock(stdout=mock_output)

    target = "123.123.123.123"
    options = ["-sV", "-p-"]
    result = run_nmap(target, options)
    assert result == mock_output
    mock_subprocess_run.assert_called_once_with(
        ["nmap", *options, target],
        check=True,
        capture_output=True,
        text=True,
        timeout=300,
    )


def test_run_nikto(mock_shutil_which: MagicMock, mock_subprocess_run: MagicMock) -> None:
    """Test the run_nikto function."""
    mock_shutil_which.return_value = "/path/to/nikto"
    mock_output = "Nikto scan results"
    mock_subprocess_run.return_value = MagicMock(stdout=mock_output)

    target = "123.123.123.123"
    options = ["-h"]
    result = run_nikto(target, options)
    assert result == mock_output
    mock_subprocess_run.assert_called_once_with(
        ["nikto", *options, target],
        check=True,
        capture_output=True,
        text=True,
        timeout=300,
    )


def test_run_gobuster(mock_shutil_which: MagicMock, mock_subprocess_run: MagicMock) -> None:
    """Test the run_gobuster function."""
    mock_shutil_which.return_value = "/path/to/gobuster"
    mock_output = "Gobuster scan results"
    mock_subprocess_run.return_value = MagicMock(stdout=mock_output)

    target = "123.123.123.123"
    url = f"http://{target}"
    options = ["-w", "/path/to/wordlist.txt"]
    result = run_gobuster(url, options)
    assert result == mock_output
    mock_subprocess_run.assert_called_once_with(
        ["gobuster", "dir", "-u", url, *options],
        check=True,
        capture_output=True,
        text=True,
        timeout=300,
    )
