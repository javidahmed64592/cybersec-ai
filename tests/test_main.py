"""Unit tests for the cybersec_ai.main module."""

from collections.abc import Generator
from unittest.mock import MagicMock, call, patch

import pytest

from cybersec_ai.main import scan_network

MOCK_TARGET = "test_target"


@pytest.fixture
def mock_sys_args() -> Generator[list[str], None, None]:
    """Mock sys.argv to simulate command line arguments."""
    argv_list = ["command", MOCK_TARGET]
    with patch("cybersec_ai.main.sys.argv", argv_list):
        yield argv_list


class TestScanNetwork:
    """Tests for the scan_network function."""

    def test_scan_network(
        self,
        mock_get_output_dir: MagicMock,
        mock_write_to_txt_file: MagicMock,
        mock_chatbot_query: MagicMock,
        mock_run_nmap: MagicMock,
        mock_run_nikto: MagicMock,
        mock_run_gobuster: MagicMock,
        mock_prompt_network_enumeration: MagicMock,
        mock_prompt_vulnerability_report: MagicMock,
        mock_sys_args: list[str],
    ) -> None:
        """Test the scan_network function."""
        query_results = [
            "port_analysis_result",
            "web_app_analysis_result",
            "vulnerability_report_result",
        ]
        mock_chatbot_query.side_effect = query_results

        scan_network()

        mock_get_output_dir.assert_called_once_with(MOCK_TARGET)

        mock_run_nmap.assert_called_once_with(MOCK_TARGET, ["-sV", "-p-"])
        mock_run_nikto.assert_called_once_with(MOCK_TARGET, ["-h"])
        mock_run_gobuster.assert_called_once_with(
            f"http://{MOCK_TARGET}", ["-w", "/usr/share/wordlists/dirb/common.txt"]
        )

        mock_prompt_network_enumeration.assert_called_once_with(
            nmap_output=mock_run_nmap.return_value,
            nikto_output=mock_run_nikto.return_value,
            gobuster_output=mock_run_gobuster.return_value,
        )
        mock_prompt_vulnerability_report.assert_called_once_with(
            port_analysis=query_results[0],
            web_app_analysis=query_results[1],
        )

        mock_chatbot_query.assert_has_calls(
            [
                call(mock_prompt_network_enumeration.return_value["port_analysis"]),
                call(mock_prompt_network_enumeration.return_value["web_app_analysis"]),
                call(mock_prompt_vulnerability_report.return_value),
            ]
        )

        mock_write_to_txt_file.assert_has_calls(
            [
                call(mock_run_nmap.return_value, "nmap_scan.txt", mock_get_output_dir.return_value),
                call(mock_run_nikto.return_value, "nikto_scan.txt", mock_get_output_dir.return_value),
                call(mock_run_gobuster.return_value, "gobuster_scan.txt", mock_get_output_dir.return_value),
                call(query_results[0], "port_analysis.txt", mock_get_output_dir.return_value),
                call(query_results[1], "web_app_analysis.txt", mock_get_output_dir.return_value),
                call(query_results[2], "vulnerability_report.txt", mock_get_output_dir.return_value),
            ]
        )

    def test_scan_network_no_target(
        self,
        mock_get_output_dir: MagicMock,
        mock_write_to_txt_file: MagicMock,
        mock_chatbot_query: MagicMock,
        mock_run_nmap: MagicMock,
        mock_run_nikto: MagicMock,
        mock_run_gobuster: MagicMock,
        mock_prompt_network_enumeration: MagicMock,
        mock_prompt_vulnerability_report: MagicMock,
        mock_sys_args: list[str],
    ) -> None:
        """Test scan_network raises ValueError when no target is provided."""
        mock_sys_args.pop()

        with pytest.raises(ValueError, match="Usage: scan-network <target>"):
            scan_network()

        mock_get_output_dir.assert_not_called()
        mock_write_to_txt_file.assert_not_called()
        mock_chatbot_query.assert_not_called()
        mock_run_nmap.assert_not_called()
        mock_run_nikto.assert_not_called()
        mock_run_gobuster.assert_not_called()
        mock_prompt_network_enumeration.assert_not_called()
        mock_prompt_vulnerability_report.assert_not_called()
