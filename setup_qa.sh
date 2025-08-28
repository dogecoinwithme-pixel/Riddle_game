#!/bin/bash

# Riddle Game QA Automation Setup Script
# This script sets up the environment for running QA automation

echo "Setting up Riddle Game QA Automation Environment..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p allure-results
mkdir -p allure-report  
mkdir -p locust_reports
mkdir -p mlruns

# Download Allure if not present
if [ ! -d "allure-2.34.1" ]; then
    echo "Downloading Allure CLI..."
    if command -v wget >/dev/null 2>&1; then
        wget https://github.com/allure-framework/allure2/releases/download/2.34.1/allure-2.34.1.zip
        unzip allure-2.34.1.zip
        rm allure-2.34.1.zip
    elif command -v curl >/dev/null 2>&1; then
        curl -L https://github.com/allure-framework/allure2/releases/download/2.34.1/allure-2.34.1.zip -o allure-2.34.1.zip
        unzip allure-2.34.1.zip
        rm allure-2.34.1.zip
    else
        echo "Please download Allure manually from https://github.com/allure-framework/allure2/releases"
    fi
fi

# Set up environment variables (optional)
echo "Setting up environment variables..."
export MLFLOW_TRACKING_URI="./mlruns"
export TEST_URL="http://localhost:8000"

# Create example configuration files
if [ ! -f "client_secrets.json" ]; then
    echo "Creating example Google Drive configuration..."
    cp client_secrets.json.example client_secrets.json
    echo "Please update client_secrets.json with your Google Drive API credentials"
fi

echo "Setup complete!"
echo ""
echo "To run QA automation:"
echo "  python qa_automation.py"
echo ""
echo "To run individual components:"
echo "  pytest tests/                    # Run tests only"
echo "  locust -f locustfile.py --help   # See load testing options"
echo "  bandit -r RiddleZone.py         # Run security scan"
echo ""
echo "Environment variables to configure:"
echo "  EMAIL_SENDER=your_email@gmail.com"
echo "  EMAIL_PASSWORD=your_app_password"
echo "  EMAIL_RECEIVERS=dev1@example.com,dev2@example.com"