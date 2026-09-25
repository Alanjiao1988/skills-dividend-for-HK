"""Repository CLI adapter; the installable skill owns the validator."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.validate_analysis import main

if __name__ == "__main__":
    main()
