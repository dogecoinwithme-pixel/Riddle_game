#!/usr/bin/env python3
"""
QA Automation Script for Riddle Game
Comprehensive testing and reporting automation for the Riddle Game project.
"""
import os
import subprocess
import shutil
from pathlib import Path
import smtplib
from email.message import EmailMessage
import pytest
import mlflow
import tempfile
import json
import logging
from datetime import datetime

# -----------------------------
# Config
# -----------------------------
BASE_DIR = Path(__file__).parent
ALLURE_RESULTS = BASE_DIR / "allure-results"
ALLURE_REPORT = BASE_DIR / "allure-report"
LOCUST_FILE = BASE_DIR / "locustfile.py"
CLIENT_SECRETS = BASE_DIR / "client_secrets.json"
TEST_URL = os.environ.get("TEST_URL", "http://localhost:8000")  # For future web version

# Email configuration
EMAIL_SENDER = os.environ.get("EMAIL_SENDER", "qa-automation@example.com")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "")
EMAIL_RECEIVERS = os.environ.get("EMAIL_RECEIVERS", "dev@example.com").split(",")

# MLflow configuration
MLFLOW_EXPERIMENT = "riddle_game_qa"
MLFLOW_TRACKING_URI = os.environ.get("MLFLOW_TRACKING_URI", str(BASE_DIR / "mlruns"))

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(BASE_DIR / "qa_automation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# -----------------------------
# Helper: Run Pytest + Allure
# -----------------------------
def run_pytest():
    """Run Pytest on all test files with Allure reporting."""
    logger.info("Running Pytest on all test files...")
    
    # Ensure allure-results directory exists
    ALLURE_RESULTS.mkdir(exist_ok=True)
    
    pytest_args = [
        str(BASE_DIR / "tests"),
        f"--alluredir={ALLURE_RESULTS}",
        "--tb=short",
        "-v"
    ]
    
    try:
        pytest_exit = pytest.main(pytest_args)
        logger.info(f"Pytest completed with exit code: {pytest_exit}")
        return pytest_exit
    except Exception as e:
        logger.error(f"Pytest execution failed: {e}")
        return 1

def generate_allure():
    """Generate Allure HTML report from results."""
    if not ALLURE_RESULTS.exists() or not any(ALLURE_RESULTS.iterdir()):
        logger.warning("No Allure results to generate.")
        return False

    try:
        # Try to find allure binary
        allure_paths = [
            BASE_DIR / "allure-2.34.1" / "bin" / "allure",
            BASE_DIR / "allure-2.34.1" / "bin" / "allure.bat",
            shutil.which("allure")
        ]
        
        allure_cmd = None
        for path in allure_paths:
            if path and Path(path).exists():
                allure_cmd = str(path)
                break
        
        if not allure_cmd:
            logger.warning("Allure binary not found. Install Allure CLI tool.")
            return False
            
        result = subprocess.run([
            allure_cmd,
            "generate", str(ALLURE_RESULTS), 
            "-o", str(ALLURE_REPORT), 
            "--clean"
        ], check=True, capture_output=True, text=True)
        
        logger.info(f"Allure report generated at: {ALLURE_REPORT.resolve()}")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Allure generation failed: {e}")
        logger.error(f"Stderr: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"Allure generation error: {e}")
        return False

# -----------------------------
# Helper: Upload to Google Drive
# -----------------------------
def upload_to_drive():
    """Upload test reports to Google Drive."""
    if not CLIENT_SECRETS.exists():
        logger.warning("Client secrets not found, skipping Drive upload.")
        return None

    try:
        from pydrive2.auth import GoogleAuth
        from pydrive2.drive import GoogleDrive
        
        logger.info("Authenticating Google Drive...")
        gauth = GoogleAuth()
        gauth.LoadClientConfigFile(str(CLIENT_SECRETS))
        
        # Use service account or saved credentials
        try:
            gauth.LoadCredentialsFile("credentials.json")
        except:
            logger.info("No saved credentials, using service account auth...")
            gauth.ServiceAuth()
        
        drive = GoogleDrive(gauth)

        # Create zip of reports
        zip_path = BASE_DIR / "qa-reports.zip"
        if zip_path.exists():
            zip_path.unlink()

        # Include both Allure and HTML reports
        reports_to_zip = []
        if ALLURE_REPORT.exists():
            reports_to_zip.append(("allure-report", ALLURE_REPORT))
        
        # Also generate human-readable report  
        html_report = BASE_DIR / "test-report.html"
        if html_report.exists():
            reports_to_zip.append(("test-report.html", html_report))
            
        if not reports_to_zip:
            logger.warning("No reports to upload.")
            return None
            
        # Create temporary directory for zipping
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            for name, source in reports_to_zip:
                if source.is_dir():
                    shutil.copytree(source, temp_path / name)
                else:
                    shutil.copy2(source, temp_path / name)
            
            shutil.make_archive(str(zip_path.with_suffix("")), "zip", temp_path)

        logger.info("Uploading QA reports to Google Drive...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_drive = drive.CreateFile({
            'title': f'riddle-game-qa-reports-{timestamp}.zip'
        })
        file_drive.SetContentFile(str(zip_path))
        file_drive.Upload()
        
        share_link = f"https://drive.google.com/file/d/{file_drive['id']}/view?usp=sharing"
        logger.info(f"Upload complete. Shareable link: {share_link}")
        
        # Clean up
        zip_path.unlink()
        return share_link
        
    except ImportError:
        logger.error("PyDrive2 not installed. Install with: pip install pydrive2")
        return None
    except Exception as e:
        logger.error(f"Google Drive upload failed: {e}")
        return None

# -----------------------------
# Helper: Send Email
# -----------------------------
def send_email(report_link, test_results):
    """Send email notification to dev team."""
    if not EMAIL_PASSWORD or not EMAIL_SENDER:
        logger.warning("Email credentials not configured, skipping email notification.")
        return False
        
    try:
        logger.info("Sending email to dev team...")
        msg = EmailMessage()
        msg['Subject'] = f"Riddle Game QA Automation Results - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        msg['From'] = EMAIL_SENDER
        msg['To'] = ", ".join(EMAIL_RECEIVERS)
        
        # Create email body
        body = f"""
QA Automation run completed for Riddle Game.

Test Results Summary:
- Tests Run: {test_results.get('total', 'N/A')}
- Passed: {test_results.get('passed', 'N/A')} 
- Failed: {test_results.get('failed', 'N/A')}
- Skipped: {test_results.get('skipped', 'N/A')}
- Exit Code: {test_results.get('exit_code', 'N/A')}

"""
        
        if report_link:
            body += f"View detailed reports: {report_link}\n"
        else:
            body += "Reports available locally in the project directory.\n"
            
        body += f"""
Automation completed at: {datetime.now().isoformat()}

Best regards,
QA Automation System
        """
        
        msg.set_content(body)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        
        logger.info("Email sent successfully.")
        return True
        
    except Exception as e:
        logger.error(f"Email sending failed: {e}")
        return False

# -----------------------------
# Helper: Run Locust Load Test
# -----------------------------
def run_locust():
    """Run Locust load tests on the game logic."""
    if not LOCUST_FILE.exists():
        logger.warning("Locust file not found, skipping load test.")
        return False
    
    try:
        logger.info("Running Locust load tests...")
        
        # Create locust reports directory
        locust_reports_dir = BASE_DIR / "locust_reports"
        locust_reports_dir.mkdir(exist_ok=True)
        
        result = subprocess.run([
            "locust", 
            "-f", str(LOCUST_FILE),
            "--headless",
            "-u", "10",  # 10 simulated users
            "-r", "2",   # 2 users spawned per second
            "--run-time", "30s",  # Run for 30 seconds
            "--html", str(locust_reports_dir / "locust_report.html"),
            "--csv", str(locust_reports_dir / "locust_stats")
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            logger.info("Locust load test completed successfully.")
            logger.info(f"Locust reports saved in: {locust_reports_dir}")
        else:
            logger.error(f"Locust test failed with exit code {result.returncode}")
            logger.error(f"Stderr: {result.stderr}")
            
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        logger.error("Locust test timed out.")
        return False
    except FileNotFoundError:
        logger.error("Locust not installed. Install with: pip install locust")
        return False
    except Exception as e:
        logger.error(f"Locust test error: {e}")
        return False

# -----------------------------
# Helper: Run Bandit Security Scan
# -----------------------------
def run_bandit():
    """Run Bandit security scan on the codebase."""
    try:
        logger.info("Running Bandit security scan...")
        
        # Scan the main code and tests
        scan_paths = [str(BASE_DIR / "RiddleZone.py"), str(BASE_DIR / "tests")]
        
        result = subprocess.run([
            "bandit", 
            "-r", 
            *scan_paths,
            "-f", "json",
            "-o", str(BASE_DIR / "bandit_report.json")
        ], capture_output=True, text=True)
        
        # Bandit exit codes: 0=no issues, 1=issues found, other=error
        if result.returncode in [0, 1]:
            logger.info("Bandit security scan completed.")
            
            # Also generate human-readable report
            subprocess.run([
                "bandit",
                "-r",
                *scan_paths,
                "-f", "txt"
            ], capture_output=False)
            
        else:
            logger.error(f"Bandit scan failed with exit code {result.returncode}")
            logger.error(f"Stderr: {result.stderr}")
            
        return result.returncode in [0, 1]
        
    except FileNotFoundError:
        logger.error("Bandit not installed. Install with: pip install bandit")
        return False
    except Exception as e:
        logger.error(f"Bandit scan error: {e}")
        return False

# -----------------------------
# Helper: Parse Test Results
# -----------------------------
def parse_test_results(pytest_exit_code):
    """Parse test results for reporting."""
    results = {
        'exit_code': pytest_exit_code,
        'total': 0,
        'passed': 0,
        'failed': 0,
        'skipped': 0
    }
    
    # Try to parse HTML report for detailed stats
    html_report = BASE_DIR / "test-report.html"
    if html_report.exists():
        try:
            with open(html_report, 'r') as f:
                content = f.read()
                # Simple parsing - look for test results summary
                # This is a basic implementation, could be improved
                if 'passed' in content.lower():
                    results['status'] = 'completed'
        except Exception as e:
            logger.warning(f"Could not parse HTML report: {e}")
    
    return results

# -----------------------------
# Main Orchestrator
# -----------------------------
def main():
    """Main QA automation orchestrator."""
    logger.info("Starting QA Automation for Riddle Game...")
    
    # Initialize MLflow
    try:
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        mlflow.set_experiment(MLFLOW_EXPERIMENT)
    except Exception as e:
        logger.warning(f"MLflow initialization failed: {e}")
    
    with mlflow.start_run():
        try:
            # Log basic info
            mlflow.log_param("project", "riddle_game")
            mlflow.log_param("timestamp", datetime.now().isoformat())
            
            # Run tests
            pytest_exit = run_pytest()
            mlflow.log_metric("pytest_exit_code", pytest_exit)
            
            # Generate reports
            allure_success = generate_allure()
            mlflow.log_metric("allure_generated", 1 if allure_success else 0)
            
            # Upload to cloud
            report_link = upload_to_drive()
            if report_link:
                mlflow.log_param("report_link", report_link)
            
            # Parse test results
            test_results = parse_test_results(pytest_exit)
            
            # Send notifications
            email_sent = send_email(report_link, test_results)
            mlflow.log_metric("email_sent", 1 if email_sent else 0)
            
            # Run load tests
            locust_success = run_locust()
            mlflow.log_metric("load_test_success", 1 if locust_success else 0)
            
            # Run security scan
            bandit_success = run_bandit()
            mlflow.log_metric("security_scan_success", 1 if bandit_success else 0)
            
            # Overall success
            overall_success = pytest_exit == 0
            mlflow.log_metric("overall_success", 1 if overall_success else 0)
            
            logger.info("QA Automation run complete.")
            
            if overall_success:
                logger.info("✅ All tests passed!")
            else:
                logger.warning("⚠️  Some tests failed. Check reports for details.")
                
        except Exception as e:
            logger.error(f"QA Automation failed: {e}")
            mlflow.log_param("error", str(e))
            raise

if __name__ == "__main__":
    main()