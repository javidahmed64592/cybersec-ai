"""Unit tests for the cybersec_ai.models.prompt_factory module."""

from cybersec_ai.models.prompt_factory import PromptFactory


class TestPromptFactory:
    """Test suite for the PromptFactory class."""

    def test_create_network_enumeration_prompt(self) -> None:
        """Test the creation of a network enumeration prompt."""
        nmap_output = "Nmap scan results..."
        nikto_output = "Nikto scan results..."
        gobuster_output = "Gobuster scan results..."

        prompts = PromptFactory.create_network_enumeration_prompt(nmap_output, nikto_output, gobuster_output)

        port_analysis_prompt = prompts["port_analysis"]
        web_app_analysis_prompt = prompts["web_app_analysis"]
        assert "port_analysis" in prompts
        assert "web_app_analysis" in prompts

        assert isinstance(port_analysis_prompt, str)
        assert "Nmap Output:" in port_analysis_prompt
        assert nmap_output in port_analysis_prompt
        assert isinstance(web_app_analysis_prompt, str)
        assert "Nikto Output:" in web_app_analysis_prompt
        assert nikto_output in web_app_analysis_prompt
        assert "Gobuster Output:" in web_app_analysis_prompt
        assert gobuster_output in web_app_analysis_prompt

    def test_create_vulnerability_report_prompt(self) -> None:
        """Test the creation of a vulnerability report prompt."""
        port_analysis = "Port analysis details..."
        web_app_analysis = "Web application analysis details..."

        report_prompt = PromptFactory.create_vulnerability_report_prompt(port_analysis, web_app_analysis)

        assert isinstance(report_prompt, str)
        assert "Port Analysis:" in report_prompt
        assert port_analysis in report_prompt
        assert "Web Application Analysis:" in report_prompt
        assert web_app_analysis in report_prompt
