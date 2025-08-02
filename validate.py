#!/usr/bin/env python3
"""
Validation script to test the Gantt Chart Generator
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path

def run_command(command, description):
    """Run a command and return success status"""
    print(f"🧪 Testing: {description}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  ✅ {description} - PASSED")
            return True
        else:
            print(f"  ❌ {description} - FAILED")
            print(f"  Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"  ❌ {description} - FAILED")
        print(f"  Exception: {e}")
        return False

def main():
    print("🚀 Gantt Chart Generator Validation Test")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 5
    
    # Test 1: Check if script runs with help
    if run_command("python3 gantt_generator.py --help", "Help command"):
        tests_passed += 1
    
    # Test 2: Generate sample data
    if run_command("python3 gantt_generator.py --sample", "Sample data generation"):
        tests_passed += 1
    
    # Test 3: Generate chart from CSV
    if run_command("python3 gantt_generator.py sample_project.csv -o test_validation.png", "CSV to Gantt chart"):
        # Check if file was created
        if os.path.exists("test_validation.png"):
            print("  ✅ Chart file created successfully")
        else:
            print("  ❌ Chart file not found")
        tests_passed += 1
    
    # Test 4: Test Excel support (if Excel file exists)
    if os.path.exists("sample_project.xlsx"):
        if run_command("python3 gantt_generator.py sample_project.xlsx -o test_excel.png", "Excel to Gantt chart"):
            tests_passed += 1
    else:
        print("🧪 Testing: Excel to Gantt chart")
        print("  ⏭️  Skipped - No Excel file found")
        total_tests -= 1
    
    # Test 5: Check dependencies
    print("🧪 Testing: Required dependencies")
    try:
        import pandas
        import matplotlib
        import seaborn
        import numpy
        import openpyxl
        print("  ✅ All dependencies imported successfully")
        tests_passed += 1
    except ImportError as e:
        print(f"  ❌ Missing dependency: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Gantt Chart Generator is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the setup.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
