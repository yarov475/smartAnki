# test_runner.py

import sys
from smartanki.main_cli import main

def test_export_apkg():
    # Simulate CLI input:
    test_args = [
        "smartanki",                    # dummy script name
        "input/sample.pdf",             # filepath
        "--no-save",                    # don't store in DB
        "--export-apkg",                # generate .apkg
        "--deck-name", "Testing"        # deck name
    ]

    # Backup original sys.argv and replace it
    original_argv = sys.argv
    sys.argv = test_args

    try:
        main()
    finally:
        sys.argv = original_argv  # restore original arguments

if __name__ == "__main__":
    test_export_apkg()
