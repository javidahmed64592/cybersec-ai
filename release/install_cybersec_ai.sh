#!/bin/bash
set -eu

PACKAGE_NAME="cybersec_ai"
WD=$(pwd)
VENV_NAME=".venv"
EXE_NAMES=("cybersec_ai" "scan-network")
CONFIG_FILE="config.json"
LOG_FILE="cybersec_ai.log"
UNINSTALL_FILE="uninstall_cybersec_ai.sh"
README_FILE="README.txt"

FULL_VENV_PATH="${WD}/${VENV_NAME}"
BIN_DIR="${FULL_VENV_PATH}/bin"
LOGS_DIR="${WD}/logs"

CONFIG_PATH="${WD}/${CONFIG_FILE}"
LOG_PATH="${LOGS_DIR}/${LOG_FILE}"
UNINSTALL_PATH="${WD}/${UNINSTALL_FILE}"
README_PATH="${WD}/${README_FILE}"

mkdir -p "${LOGS_DIR}"

echo "Creating virtual environment..."
uv venv ${VENV_NAME}

echo "Installing from wheel..."
WHEEL_FILE=$(find "${WD}" -name "${PACKAGE_NAME}-*-py3-none-any.whl")
uv pip install "${WHEEL_FILE}"
rm "${WHEEL_FILE}"

echo "Creating API executables..."
for EXE_NAME in "${EXE_NAMES[@]}"; do
    echo "  Creating executable: ${EXE_NAME}"
    cat > "${WD}/${EXE_NAME}" << EOF
#!/bin/bash
export CYBERSEC_AI_ROOT_DIR=${WD}
${BIN_DIR}/${EXE_NAME} "\$@"
EOF
    chmod +x "${WD}/${EXE_NAME}"
done

echo "Creating uninstall script..."
cat > "${UNINSTALL_PATH}" << EOF
#!/bin/bash
set -eu
rm -rf "${WD}/*"
EOF
chmod +x "${UNINSTALL_PATH}"

cat > "${README_PATH}" << EOF
CyberSec AI has been installed successfully.
To configure the application, edit the configuration file at: '${CONFIG_PATH}'
To view the logs: 'cat logs/${LOG_FILE}'
To uninstall, run: './${UNINSTALL_FILE}'
EOF

TERMINAL_WIDTH=$(tput cols 2>/dev/null || echo 80)
SEPARATOR=$(printf '=%.0s' $(seq 1 $TERMINAL_WIDTH))

echo "${SEPARATOR}"
cat "${README_PATH}"
echo "${SEPARATOR}"

rm -- "$0"
