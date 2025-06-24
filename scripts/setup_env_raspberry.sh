#!/bin/bash

# ===============================
# Drowsiness Detection Setup Script for Raspberry Pi OS
# ===============================

VENV_DIR="venv"
REQUIREMENTS_FILE="requirements-linux.txt"

echo "=========================================="
echo " Drowsiness Detection - Raspberry Pi Setup"
echo "=========================================="

# Step 0: Safety check
if [[ "$(uname -m)" != "aarch64" && "$(uname -m)" != "armv7l" ]]; then
    echo "[WARNING] This script is designed for Raspberry Pi OS. Proceed with caution."
fi

# Step 1: Update system packages
echo "[INFO] Updating system packages..."
sudo apt update

# Step 2: Install libcamera system packages
echo "[INFO] Installing Raspberry Pi camera libraries..."
sudo apt install -y python3-libcamera libcamera-dev

# Step 3: Confirm system Python version
PY_VERSION=$(python3 --version)
echo "[INFO] Raspberry Pi System Python default version: $PY_VERSION"

# Step 4: Create virtual environment using system Python
if [ -d "$VENV_DIR" ]; then
    echo "[INFO] Virtual environment already exists. Skipping creation."
else
    echo "[INFO] Creating virtual environment with system site packages..."
    python3 -m venv --system-site-packages "$VENV_DIR"
fi

# Step 5: Install Node.js 
if ! command -v node >/dev/null 2>&1; then
    echo "[INFO] Installing Node.js via NVM..."
    # Download and install nvm:
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash

    # Initialize nvm without restarting shell
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

    # Install Node.js
    nvm install 22
else
    echo "[INFO] Node.js already installed. Skipping."
fi

# Verify the Node.js version:
nvm current
node -v
npm -v

# Install serve to serve React dashboard for now
npm install -g serve

# Step 6: Activate virtual environment
echo "[INFO] Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Step 7: Upgrade pip (optional but recommended)
echo "[INFO] Upgrading pip..."
pip install --upgrade pip

# Step 8: Install project dependencies
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "[INFO] Installing dependencies from $REQUIREMENTS_FILE..."
    pip install -r "$REQUIREMENTS_FILE"
else
    echo "[WARNING] $REQUIREMENTS_FILE not found. Skipping."
fi

# Step 9: Install uvicorn for FastAPI
echo "[INFO] Installing uvicorn server..."
pip install "uvicorn[standard]"

echo
echo "[SUCCESS] Environment setup complete!"
echo "[INFO] To activate the environment later, run:"
echo "       source $VENV_DIR/bin/activate"
echo "[INFO] To deactivate the environment, run: deactivate"
