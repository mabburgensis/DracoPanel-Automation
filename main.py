# main.py
import subprocess
import os

TEST_FILES = [
    "register.py",
    "login.py",
    "mines.py",
    "diamonds.py",
    "dice.py"
]

def run_test(file_name):
    print(f"\nTest starting: {file_name}")
    result = subprocess.run(["python", file_name])
    if result.returncode != 0:
        print(f"Test failed: {file_name} (exit code: {result.returncode})")
        print("Test chain stopped.")
        exit(1)
    else:
        print(f"Test finished successfully: {file_name}")

if __name__ == "__main__":
    print("=== Automation Test Runner (main.py) ===")
    for test_file in TEST_FILES:
        if os.path.exists(test_file):
            run_test(test_file)
        else:
            print(f"File not found: {test_file}")
