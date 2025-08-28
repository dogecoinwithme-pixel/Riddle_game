# Riddle Game QA Automation

This repository contains a comprehensive QA automation framework for the Riddle Game project, including automated testing, reporting, load testing, and security scanning.

## Overview

The QA automation system provides:
- **Automated Testing**: Unit tests, integration tests, and security tests using pytest
- **Test Reporting**: Allure HTML reports for detailed test analysis
- **Load Testing**: Performance testing using Locust
- **Security Scanning**: Static code analysis using Bandit
- **Cloud Integration**: Google Drive upload for test reports
- **Email Notifications**: Automated email alerts for test results
- **Experiment Tracking**: MLflow integration for tracking test metrics

## Project Structure

```
Riddle_game/
├── RiddleZone.py           # Main game application (GUI)
├── riddles_data.py         # Game logic and data for testing
├── qa_automation.py        # Main QA automation script
├── locustfile.py          # Load testing configuration
├── requirements.txt        # Python dependencies
├── pytest.ini            # Pytest configuration
├── setup_qa.sh           # Setup script for QA environment
├── tests/                 # Test suite
│   ├── conftest.py        # Test configuration and fixtures
│   ├── test_riddle_game.py # Unit tests for game logic
│   └── test_integration.py # Integration and performance tests
├── allure-results/        # Allure test results (auto-generated)
├── allure-report/         # Allure HTML reports (auto-generated)
├── locust_reports/        # Load testing reports (auto-generated)
├── mlruns/               # MLflow experiment tracking (auto-generated)
└── bandit_report.json    # Security scan results (auto-generated)
```

## Quick Start

### 1. Setup Environment

```bash
# Make setup script executable and run it
chmod +x setup_qa.sh
./setup_qa.sh

# Or manually install dependencies
pip install -r requirements.txt
```

### 2. Run Complete QA Automation

```bash
python qa_automation.py
```

This will run all QA processes:
- Execute all tests with pytest
- Generate Allure reports
- Run load tests
- Perform security scan
- Track metrics with MLflow

### 3. Run Individual Components

```bash
# Run tests only
pytest tests/ -v

# Run tests with Allure reporting
pytest tests/ --alluredir=allure-results

# Run load tests
locust -f locustfile.py --headless -u 10 -r 2 --run-time 30s

# Run security scan
bandit -r RiddleZone.py tests/

# Generate Allure HTML report (requires Allure CLI)
allure generate allure-results -o allure-report --clean
```

## Test Suite

### Unit Tests (`test_riddle_game.py`)
- **Riddles Data Validation**: Structure, content, and format validation
- **Game Logic**: Age validation, scoring, and answer checking
- **Data Integrity**: Uniqueness and consistency checks

### Integration Tests (`test_integration.py`)
- **Module Imports**: Verifies all modules can be imported
- **Function Testing**: Tests extracted game functions
- **Performance Tests**: Measures riddle loading and access performance
- **Security Tests**: Input validation and sanitization

### Load Testing (`locustfile.py`)
- **User Simulation**: Simulates multiple concurrent game sessions
- **Performance Metrics**: Response times, throughput, and error rates
- **Stress Testing**: Tests system behavior under load
- **Admin Operations**: Administrative task simulation

## Configuration

### Environment Variables

Set these environment variables for full functionality:

```bash
export EMAIL_SENDER="your_email@gmail.com"
export EMAIL_PASSWORD="your_app_password"
export EMAIL_RECEIVERS="dev1@example.com,dev2@example.com"
export MLFLOW_TRACKING_URI="./mlruns"
export TEST_URL="http://localhost:8000"
```

### Google Drive Integration

1. Create a Google Cloud project and enable Drive API
2. Download credentials as `client_secrets.json`
3. Place the file in the project root directory
4. The system will authenticate and upload reports to Drive

### Email Notifications

Configure Gmail with an app password:
1. Enable 2-factor authentication on your Gmail account
2. Generate an app password for the automation script
3. Set the `EMAIL_SENDER` and `EMAIL_PASSWORD` environment variables

## Reports and Outputs

### Test Reports
- **Pytest HTML**: Basic test results in HTML format
- **Allure Reports**: Detailed interactive test reports with steps, attachments, and trends
- **MLflow Tracking**: Experiment metrics and parameters

### Load Testing Reports
- **Locust HTML**: Interactive performance testing dashboard
- **CSV Stats**: Detailed performance metrics and statistics

### Security Reports
- **Bandit JSON**: Detailed security findings in JSON format
- **Bandit Console**: Human-readable security scan output

## Key Features

### Automated Test Execution
- Runs comprehensive test suite covering game logic, data validation, and security
- Supports parallel test execution for faster feedback
- Integrates with CI/CD pipelines

### Advanced Reporting
- Allure reports with step-by-step test execution details
- Trend analysis and historical test data
- Rich attachments and categorized test results

### Performance Testing
- Simulates realistic user load on game logic
- Measures response times and system performance
- Identifies bottlenecks and performance degradation

### Security Scanning
- Static code analysis for common security vulnerabilities
- Input validation testing
- Configuration and secret detection

### Cloud Integration
- Automatic report upload to Google Drive
- Email notifications for team collaboration
- MLflow experiment tracking for metrics

## Development Workflow

### Adding New Tests
1. Create test files in the `tests/` directory
2. Follow naming convention: `test_*.py`
3. Use Allure decorators for better reporting:
   ```python
   @allure.feature("Game Logic")
   @allure.story("Answer Validation")
   @allure.title("Test correct answer handling")
   def test_answer_validation(self):
       # Test implementation
   ```

### Customizing Load Tests
1. Modify `locustfile.py` to add new user behaviors
2. Adjust user count and spawn rate in the QA script
3. Add custom metrics and validation logic

### Security Test Configuration
1. Update `.bandit` configuration file to exclude false positives
2. Add security-focused unit tests in the test suite
3. Configure custom security scanning rules

## Troubleshooting

### Common Issues

**Allure reports not generating:**
- Install Allure CLI tool: Download from [Allure releases](https://github.com/allure-framework/allure2/releases)
- Add allure binary to PATH or update QA script with correct path

**Email notifications failing:**
- Verify Gmail app password configuration
- Check firewall settings for SMTP access
- Ensure environment variables are properly set

**Load tests not running:**
- Verify Locust installation: `pip install locust`
- Check if ports are available for Locust web UI
- Review locustfile.py for syntax errors

**Google Drive upload failing:**
- Verify client_secrets.json file exists and is valid
- Check Google Cloud API permissions
- Ensure Drive API is enabled in Google Cloud Console

### Performance Optimization

**For faster test execution:**
- Use pytest-xdist for parallel testing: `pip install pytest-xdist`
- Run with `-n auto` flag: `pytest tests/ -n auto`

**For reduced resource usage:**
- Adjust Locust user count and spawn rate
- Limit test scope using pytest markers
- Configure MLflow to use lightweight tracking

## Contributing

1. Add comprehensive tests for new features
2. Update documentation for new QA processes
3. Ensure all tests pass before submitting changes
4. Follow the existing code style and conventions

## License

This QA automation framework is part of the Riddle Game project and follows the same license terms.