from __future__ import annotations

import os
import socket
import shutil
import subprocess
import sys
import threading
import time
import webbrowser
import importlib.util
import logging
from pathlib import Path
from urllib import error, request

import uvicorn

try:
    from app.server import app as server_app
except ModuleNotFoundError:
    # Supports running as: `python app/host.py`
    from server import app as server_app

HOST = "127.0.0.1"
DEFAULT_PORT = 8100
LOG_PATH: Path | None = None


def setup_logging() -> None:
    global LOG_PATH
    if getattr(sys, "frozen", False):
        try:
            LOG_PATH = Path(sys.argv[0]).with_suffix(".log")
            logging.basicConfig(
                filename=str(LOG_PATH),
                level=logging.INFO,
                format="%(asctime)s %(levelname)s %(message)s",
            )
            logging.info("Q-Slidee started (frozen exe).")
        except Exception:
            # If logging fails, continue without blocking startup.
            LOG_PATH = None


def log_exception(context: str, exc: BaseException) -> None:
    try:
        logging.exception("%s: %s", context, exc)
    except Exception:
        pass


def safe_print(*args, **kwargs) -> None:
    if sys.stdout is None:
        return
    try:
        print(*args, **kwargs)
    except Exception:
        pass


def find_available_port(start_port: int = DEFAULT_PORT, max_tries: int = 30) -> int:
    for port in range(start_port, start_port + max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind((HOST, port))
                return port
            except OSError:
                continue
    raise RuntimeError("Uygun port bulunamadi.")


def run_server(port: int) -> None:
    ws_mode = "auto" if has_websocket_backend() else "none"
    try:
        uvicorn.run(
            server_app,
            host=HOST,
            port=port,
            log_level="warning",
            ws=ws_mode,
            log_config=None,  # Avoid uvicorn default formatter relying on sys.stdout.isatty() in frozen EXE.
        )
    except Exception as exc:
        log_exception("Uvicorn failed to start", exc)


def has_websocket_backend() -> bool:
    return (
        importlib.util.find_spec("websockets") is not None
        or importlib.util.find_spec("wsproto") is not None
    )


def wait_for_server(url: str, timeout_seconds: float = 12.0) -> bool:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            with request.urlopen(url, timeout=1):
                return True
        except (error.URLError, TimeoutError):
            time.sleep(0.2)
    return False


def launch_host_window(url: str) -> bool:
    app_flag = f"--app={url}"
    candidate_commands: list[list[str]] = [
        ["msedge", app_flag, "--new-window", "--window-size=1120,760"],
        ["chrome", app_flag, "--new-window", "--window-size=1120,760"],
    ]

    edge_paths = [
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    ]
    for edge_path in edge_paths:
        if edge_path.exists():
            candidate_commands.insert(
                0,
                [str(edge_path), app_flag, "--new-window", "--window-size=1120,760"],
            )

    for cmd in candidate_commands:
        exe = cmd[0]
        if shutil.which(exe) or Path(exe).exists():
            try:
                subprocess.Popen(cmd)
                return True
            except Exception:
                continue

    try:
        os.startfile(url)  # type: ignore[attr-defined]
        return True
    except Exception:
        pass

    return webbrowser.open(url)


def main() -> int:
    setup_logging()
    if not has_websocket_backend():
        safe_print("WebSocket backend bulunamadı. Polling fallback ile devam edilecek.")
        if LOG_PATH:
            logging.warning("WebSocket backend bulunamadı. Polling fallback ile devam edilecek.")

    port = find_available_port()
    if LOG_PATH:
        logging.info("Using port %s", port)
    server_thread = threading.Thread(target=run_server, args=(port,), daemon=True)
    server_thread.start()

    api_url = f"http://{HOST}:{port}/api/state"
    host_url = f"http://{HOST}:{port}/host"
    viewer_url = f"http://{HOST}:{port}/"

    if not wait_for_server(api_url):
        safe_print("Sunucu başlatılamadı. Lütfen port ve bağımlılıkları kontrol edin.")
        if LOG_PATH:
            logging.error("Sunucu başlatılamadı. API yanıt vermedi: %s", api_url)
        return 1

    opened = launch_host_window(host_url)
    if opened:
        safe_print(f"Host penceresi açıldı: {host_url}")
    else:
        safe_print(f"Pencere otomatik açılamadı. Manuel aç: {host_url}")

    safe_print(f"Izleyici linki: {viewer_url}")
    safe_print("Kapatmak için Ctrl+C.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        return 0
    except Exception as exc:
        log_exception("Fatal error", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
