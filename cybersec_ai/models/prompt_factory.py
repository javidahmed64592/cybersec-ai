"""Module for creating prompts used in the CyberSec AI application."""


class PromptFactory:
    """A factory class for creating prompts for various tasks."""

    @staticmethod
    def create_network_enumeration_prompt(nmap_output: str, nikto_output: str, gobuster_output: str) -> dict[str, str]:
        """Create a prompt for network enumeration tasks."""
        prompt_port_analysis = f"""
        You're a skilled penetration tester.
        Identify services and ports that may be vulnerable to exploitation based on the following nmap scan results.

        For each service/port:
        - Describe the vulnerability or misconfiguration.
        - Explain how an attacker might exploit it (e.g., tools, techniques).
        - Recommend defensive countermeasures.

        nmap Output:
        ```
        {nmap_output}
        ```
        """

        prompt_web_app_analysis = f"""
        You're a penetration tester specializing in web application security.
        Analyze the scan results below and identify directories and known vulnerabilities that an attacker could target.

        For each finding:
        - Describe its significance and known CVEs (if applicable).
        - Suggest exploitation paths (e.g., brute-forcing admin panels, parameter tampering, directory traversal).
        - Recommend fixes or mitigations.

        Nikto Output:
        ```
        {nikto_output}
        ```

        Gobuster Output:
        ```
        {gobuster_output}
        ```
        """

        return {"port_analysis": prompt_port_analysis, "web_app_analysis": prompt_web_app_analysis}

    @staticmethod
    def create_vulnerability_report_prompt(port_analysis: str, web_app_analysis: str) -> str:
        """Create a prompt for generating a vulnerability report."""
        return f"""
        You're preparing a penetration testing report based on recent reconnaissance and vulnerability scans.

        Using the following assessments, provide a detailed vulnerability report that includes:
        - Key exploitable vulnerabilities.
        - Likely attack chains or entry points.
        - Exploitation methodology: how each could be leveraged to compromise the system.
        - Suggested remediations and security enhancements.

        Port Analysis:
        ```
        {port_analysis}
        ```

        Web Application Analysis:
        ```
        {web_app_analysis}
        ```
        """
