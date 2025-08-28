#!/usr/bin/env python3
"""
Demo script to showcase the QA automation capabilities.
This script runs a subset of the QA automation to demonstrate functionality.
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and display results."""
    print(f"\n{'='*60}")
    print(f"🔍 {description}")
    print('='*60)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ SUCCESS: {description}")
            if result.stdout:
                print("Output:")
                print(result.stdout[:500])  # Limit output for demo
        else:
            print(f"❌ FAILED: {description}")
            if result.stderr:
                print("Error:")
                print(result.stderr[:500])
    except Exception as e:
        print(f"❌ ERROR: {description} - {e}")

def main():
    """Run QA automation demo."""
    print("🚀 Riddle Game QA Automation Demo")
    print("This demo showcases the QA automation capabilities")
    
    base_dir = Path(__file__).parent
    
    # 1. Run a quick test
    run_command(
        "python -m pytest tests/test_riddle_game.py::TestRiddlesData::test_riddles_structure -v",
        "Running sample unit test"
    )
    
    # 2. Run quick security scan on main code
    run_command(
        "bandit -r riddles_data.py -f txt",
        "Running security scan on game logic"
    )
    
    # 3. Demonstrate load testing (very short run)
    run_command(
        "locust -f locustfile.py --headless -u 5 -r 1 --run-time 5s --host http://localhost",
        "Running 5-second load test demo"
    )
    
    # 4. Show pytest with Allure
    run_command(
        "python -m pytest tests/test_riddle_game.py::TestGameLogic::test_age_validation --alluredir=demo-allure-results",
        "Running test with Allure reporting"
    )
    
    # 5. Check that files were created
    print(f"\n{'='*60}")
    print("📁 Generated Files and Reports")
    print('='*60)
    
    files_to_check = [
        "allure-results",
        "demo-allure-results", 
        "locust_reports",
        "bandit_report.json",
        "qa_automation.log"
    ]
    
    for file_path in files_to_check:
        path = base_dir / file_path
        if path.exists():
            if path.is_dir():
                count = len(list(path.iterdir()))
                print(f"✅ {file_path}/ (directory with {count} files)")
            else:
                size = path.stat().st_size
                print(f"✅ {file_path} ({size} bytes)")
        else:
            print(f"❌ {file_path} (not found)")
    
    print(f"\n{'='*60}")
    print("🎉 Demo Complete!")
    print('='*60)
    print("\nTo run the full QA automation suite:")
    print("  python qa_automation.py")
    print("\nTo view detailed documentation:")
    print("  cat QA_README.md")
    print("\nGenerated reports can be found in:")
    print("  - allure-results/ (raw test data)")
    print("  - locust_reports/ (performance test results)")
    print("  - bandit_report.json (security scan results)")

if __name__ == "__main__":
    main()