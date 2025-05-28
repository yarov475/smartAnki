import os
import sys
import tempfile
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from smartanki.main_cli import main

def test_apkg_export_creates_file():
    # Path to your sample input file (relative to root)
    sample_path = project_root / "input" / "sample.txt"
    assert sample_path.exists(), f"Missing input file: {sample_path}"

    # Output path
    output_path = project_root / "anki_exports" / "testing.apkg"

    # Clean up before test
    if output_path.exists():
        os.remove(output_path)

    # Simulate CLI call
    sys.argv = [
        "smartanki",
        str(sample_path),
        "--no-save",
        "--export-apkg",
        "--deck-name", "testing"
    ]

    # Run the CLI
    main()

    # ✅ Assertions
    assert output_path.exists(), "APKG file was not created"
    assert output_path.stat().st_size > 0, "APKG file is empty"

    # Optional: Clean up after test
    output_path.unlink()
