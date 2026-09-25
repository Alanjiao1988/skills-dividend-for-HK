"""Use the same runtime modules in repository and standalone installations."""
from pathlib import Path

__path__.insert(0, str(Path(__file__).resolve().parents[1]
                       / "dividend-income-equity-analysis" / "scripts"))
