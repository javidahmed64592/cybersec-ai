[![Kali Linux](https://img.shields.io/badge/Kali%20Linux-Optimized-557C94?style=flat&logo=kalilinux&logoColor=white)](https://www.kali.org/)
[![Ollama](https://img.shields.io/badge/Ollama-AI%20Models-FF6B6B?style=flat&logo=ollama&logoColor=white)](https://ollama.ai/)
[![python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=ffd343)](https://docs.python.org/3.12/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<!-- omit from toc -->
# CyberSec AI
An AI-powered cybersecurity toolkit that combines traditional penetration testing tools with intelligent analysis through local LLM models.
This application serves as a Swiss army knife for ethical hacking workflows, automatically executing security scans and providing AI-driven interpretation of results to identify vulnerabilities and recommend countermeasures.

<!-- omit from toc -->
## Disclaimer
This tool is intended for authorized penetration testing and security research only.
Users are responsible for ensuring they have proper authorization before scanning any systems.
The authors are not responsible for any misuse of this software.

- Always run scans only on systems you own or have explicit permission to test
- Some security tools may trigger intrusion detection systems
- Be mindful of network traffic and potential service disruption
- Store scan results securely and follow data protection guidelines

<!-- omit from toc -->
## Table of Contents
- [Features](#features)
- [Architecture](#architecture)
  - [Key Components](#key-components)
- [Prerequisites](#prerequisites)
  - [Installing Ollama](#installing-ollama)
- [Installation](#installation)
- [Configuration](#configuration)
- [Available Scripts](#available-scripts)
  - [`scan-network`](#scan-network)
- [Development](#development)
- [Testing, Linting, and Type Checking](#testing-linting-and-type-checking)
- [License](#license)

## Features

- **Automated Network Scanning**: Integrates nmap, nikto, and gobuster for comprehensive reconnaissance
- **AI-Powered Analysis**: Uses local Ollama models (default: Gemma 2B) to interpret scan results
- **Intelligent Reporting**: Generates detailed vulnerability reports with exploitation paths and remediation advice
- **Modular Architecture**: Easily extensible design for adding new tools and analysis capabilities
- **Command-Line Interface**: Multiple entry points for different security assessment workflows
- **Output Management**: Organized file output with structured directories for scan results
- **Ethical Focus**: Designed specifically for authorized penetration testing and security research

## Architecture

The application follows a modular design pattern:

```
cybersec_ai/
├── main.py                   # Entry point functions for different workflows
├── utils.py                  # Utility functions for file operations and configuration
├── models/
│   ├── chatbot.py            # Ollama LLM integration
│   ├── command_line_tool.py  # Decorator for shell command execution
│   └── prompt_factory.py     # AI prompt templates for security analysis
└── tools/
    └── network.py            # Network scanning tool integrations
```

### Key Components

- **Chatbot**: Interfaces with Ollama models for AI-powered analysis
- **CommandLineTool**: Decorator that safely executes shell commands with timeout and error handling
- **PromptFactory**: Creates specialized prompts for different types of security analysis

## Prerequisites

- **Python 3.12+**: Required for modern type hints and performance improvements
- **Ollama**: Local LLM server for AI analysis capabilities
- **Security Tools**: The tools which are used in this library are typically pre-installed on Kali Linux
- **uv**: Modern Python package manager for dependency management

### Installing Ollama

Install Ollama and download the default Gemma 2B model:

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the default model
ollama pull gemma:2b
```

## Installation

This repository uses `uv` for Python project management. Install `uv` first:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh                                    # Linux/Mac
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex" # Windows
```

Next, install the required dependencies using `uv`:

```bash
uv sync
```

To install with development dependencies:

```bash
uv sync --extra dev
```

## Configuration

Edit the model in `cybersec_ai/main.py`:

```python
chatbot = Chatbot(model_name="gemma:2b")  # Change to your preferred model
```

## Available Scripts

### `scan-network`

**Entry Point:** `cybersec_ai.main:scan_network`

**Description:** Performs comprehensive network reconnaissance and vulnerability analysis by combining multiple security tools with AI-powered interpretation. This script automates the entire process from initial scanning to generating actionable vulnerability reports.

**Usage:**
```bash
# Scan a target IP address
scan-network 192.168.1.100

# Scan a domain
scan-network example.com
```

**What it does:**
1. **nmap scan**: Service version detection across all ports (`-sV -p-`)
2. **nikto scan**: Web vulnerability assessment (`-h`)
3. **gobuster scan**: Directory brute-forcing using common wordlists (`/usr/share/wordlists/dirb/common.txt`)
4. **AI Analysis**:
   - Port analysis with vulnerability identification and exploitation techniques
   - Web application security assessment with CVE mapping and attack vectors
   - Comprehensive vulnerability report with remediation recommendations

**Output Files:**
```
output/
└── <target>_scan/
    ├── nmap_scan.txt            # Raw nmap scan results
    ├── nikto_scan.txt           # Web vulnerability scan output
    ├── gobuster_scan.txt        # Directory enumeration results
    ├── port_analysis.txt        # AI analysis of open ports and services
    ├── web_app_analysis.txt     # AI analysis of web vulnerabilities
    └── vulnerability_report.txt # Final consolidated security report
```

## Development

The application follows a plugin-based architecture for easy extension.
To add a new script:

1. **Create tool wrappers** in `cybersec_ai/tools/`:
```python
# cybersec_ai/tools/example.py
@CommandLineTool("custom-tool", timeout=600)
def run_custom_tool(target: str, options: list[str] | None = None) -> list[str]:
    """Run custom security tool."""
    args = options or []
    return ["--target", target, *args]
```

2. **Add analysis prompts** in `cybersec_ai/models/prompt_factory.py`
```python
@staticmethod
def create_custom_analysis_prompt(scan_output: str) -> str:
    return f"""
    Analyze the following security scan results...
    {scan_output}
    """
```

3. **Create main function** in `cybersec_ai/main.py`

4. **Register entry point** in `pyproject.toml`:
```toml
[project.scripts]
new-scan = "cybersec_ai.main:new_scan_function"
```

## Testing, Linting, and Type Checking

The project uses modern Python tooling for code quality:

- **Run tests:** `uv run pytest`
- **Lint code:** `uv run ruff check .`
- **Format code:** `uv run ruff format .`
- **Type check:** `uv run mypy .`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
