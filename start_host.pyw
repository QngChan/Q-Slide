from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    try:
        from app.host import main as host_main
    except ModuleNotFoundError:
        repo_root = Path(__file__).resolve().parent
        sys.path.insert(0, str(repo_root))
        from app.host import main as host_main

    return host_main()


if __name__ == "__main__":
    raise SystemExit(main())
