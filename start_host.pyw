from __future__ import annotations

import sys
import subprocess
from pathlib import Path

repo_root = Path(__file__).resolve().parent
venv_python = repo_root / ".venv" / "bin" / "python"

if venv_python.exists():
    result = subprocess.run([str(venv_python), "-c", """
import sys
sys.path.insert(0, '.')
from src.app.host import main
raise SystemExit(main())
"""], cwd=repo_root)
    raise SystemExit(result.returncode)

print("Virtual environment not found. Please run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt")
sys.exit(1)
