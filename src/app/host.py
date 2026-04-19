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

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from src.app.server import app as server_app
except ImportError:
    from server import app as server_app

HOST = "127.0.0.1"
DEFAULT_PORT = 8100
LOG_PATH: Path | None = None
_shutdown_event = threading.Event()
_host_alive_timestamps: dict[str, float] = {}
_host_alive_lock = threading.Lock()


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


def is_windows() -> bool:
    return os.name == "nt"


def show_popup(title: str, message: str, kind: str = "error") -> None:
    if is_windows():
        try:
            import ctypes
            flags = 0x00000000
            if kind == "warning":
                flags |= 0x00000030
            elif kind == "info":
                flags |= 0x00000040
            else:
                flags |= 0x00000010
            flags |= 0x00040000
            ctypes.windll.user32.MessageBoxW(0, message, title, flags)
            return
        except Exception:
            pass
    
    try:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        if kind == "warning":
            messagebox.showwarning(title, message)
        elif kind == "info":
            messagebox.showinfo(title, message)
        else:
            messagebox.showerror(title, message)
        root.destroy()
    except Exception:
        safe_print(f"[{kind.upper()}] {title}: {message}")


def popup_websocket_missing() -> None:
    show_popup(
        "WebSocket Destegi Bulunamadi",
        "\n".join(
            [
                "Anlik senkronizasyon icin WebSocket kutuphanesi bulunamadi.",
                "Uygulama calismaya devam edecek ancak izleyici ekrani polling ile guncellenecek.",
                "",
                "Cozum adimlari:",
                "1) Terminalde: pip install websockets",
                "2) veya: pip install wsproto",
                "3) Uygulamayi yeniden baslatin.",
            ]
        ),
        kind="warning",
    )


def popup_port_unavailable(start_port: int) -> None:
    show_popup(
        "Uygun Port Bulunamadi",
        "\n".join(
            [
                f"{start_port} portundan baslayarak bos bir port bulunamadi.",
                "",
                "Cozum adimlari:",
                "1) Q-Slidee'nin baska bir kopyasi acik mi kontrol edin.",
                "2) 8100-8130 arası portları kullanan uygulamaları kapatın.",
                "3) Bilgisayarı yeniden baslatin.",
            ]
        ),
        kind="error",
    )


def popup_server_start_failed(api_url: str) -> None:
    show_popup(
        "Sunucu Baslatilamadi",
        "\n".join(
            [
                "FastAPI sunucusu baslatilamadi veya API yanit vermedi.",
                f"Kontrol edilen adres: {api_url}",
                "",
                "Cozum adimlari:",
                "1) requirements.txt kurulu mu kontrol edin.",
                "2) Port cakismasi icin portlari bosaltin.",
                "3) Q-Slidee.log dosyasini inceleyin.",
            ]
        ),
        kind="error",
    )


def popup_host_window_failed(host_url: str) -> None:
    show_popup(
        "Host Penceresi Acilamadi",
        "\n".join(
            [
                "Host arayuzu otomatik olarak acilamadi.",
                "",
                "Cozum adimlari:",
                "1) Asagidaki adresi tarayicida manuel acin:",
                f"   {host_url}",
                "2) Tarayici kurulu degilse kurun.",
            ]
        ),
        kind="warning",
    )


def popup_uvicorn_failed() -> None:
    show_popup(
        "Uvicorn Baslatma Hatasi",
        "\n".join(
            [
                "Uvicorn sunucusu beklenmedik bir hata ile kapanmis olabilir.",
                "",
                "Cozum adimlari:",
                "1) Q-Slidee.log dosyasini kontrol edin.",
                "2) requirements.txt bagimliliklarinin kurulu oldugundan emin olun.",
                "3) Uygulamayi yeniden baslatin.",
            ]
        ),
        kind="error",
    )


def popup_unhandled_error(context: str, exc: BaseException | None = None) -> None:
    detail = f"Hata: {exc}" if exc else "Bilinmeyen hata."
    show_popup(
        "Beklenmeyen Hata",
        "\n".join(
            [
                f"{context} sirasinda beklenmeyen bir hata olustu.",
                detail,
                "",
                "Cozum adimlari:",
                "1) Uygulamayi kapatip yeniden baslatin.",
                "2) Hata devam ederse log ciktisini paylasin.",
            ]
        ),
        kind="error",
    )


def install_global_exception_handlers() -> None:
    def _excepthook(exc_type, exc, tb):
        if exc_type is KeyboardInterrupt:
            return
        log_exception("Unhandled exception", exc)
        popup_unhandled_error("Uygulama", exc)

    def _thread_excepthook(args):
        if isinstance(args.exc_type, type) and args.exc_type is KeyboardInterrupt:
            return
        log_exception("Unhandled thread exception", args.exc_value)
        popup_unhandled_error("Arka plan islem", args.exc_value)

    sys.excepthook = _excepthook
    if hasattr(threading, "excepthook"):
        threading.excepthook = _thread_excepthook


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


def find_any_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, 0))
        return int(sock.getsockname()[1])


def run_server(port: int) -> None:
    ws_mode = "auto" if has_websocket_backend() else "none"
    try:
        uvicorn.run(
            server_app,
            host=HOST,
            port=port,
            log_level="warning",
            ws=ws_mode,
            log_config=None,
        )
    except Exception as exc:
        log_exception("Uvicorn failed to start", exc)
        popup_uvicorn_failed()


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
    if is_windows():
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
            os.startfile(url)
            return True
        except Exception:
            pass
    else:
        try:
            if shutil.which("xdg-open"):
                subprocess.Popen(["xdg-open", url])
                return True
            elif shutil.which("gio"):
                subprocess.Popen(["gio", "open", url])
                return True
            elif shutil.which("gnome-open"):
                subprocess.Popen(["gnome-open", url])
                return True
        except Exception:
            pass
    
    return webbrowser.open(url)


def request_shutdown() -> None:
    _shutdown_event.set()


def register_host_alive(client_id: str) -> None:
    with _host_alive_lock:
        _host_alive_timestamps[client_id] = time.time()


def unregister_host_alive(client_id: str) -> None:
    with _host_alive_lock:
        _host_alive_timestamps.pop(client_id, None)


def check_host_alive(timeout_seconds: float = 10.0) -> bool:
    with _host_alive_lock:
        if not _host_alive_timestamps:
            return False
        now = time.time()
        for timestamp in _host_alive_timestamps.values():
            if now - timestamp < timeout_seconds:
                return True
        return False


def host_monitor_loop() -> None:
    while not _shutdown_event.is_set():
        if _host_alive_timestamps and not check_host_alive():
            safe_print("Host baglantisi kesildi. Uygulama kapatiliyor...")
            request_shutdown()
            break
        _shutdown_event.wait(timeout=2.0)


def main() -> int:
    setup_logging()
    install_global_exception_handlers()
    if not has_websocket_backend():
        safe_print("WebSocket backend bulunamadi. Polling fallback ile devam edilecek.")
        if LOG_PATH:
            logging.warning("WebSocket backend bulunamadi. Polling fallback ile devam edilecek.")
        popup_websocket_missing()

    try:
        port = find_available_port()
    except Exception as exc:
        log_exception("Port bulunamadi", exc)
        try:
            port = find_any_port()
        except Exception as exc2:
            log_exception("Alternatif port bulunamadi", exc2)
            popup_port_unavailable(DEFAULT_PORT)
            return 1
    if LOG_PATH:
        logging.info("Using port %s", port)
    
    server_thread = threading.Thread(target=run_server, args=(port,), daemon=True)
    server_thread.start()
    
    host_monitor_thread = threading.Thread(target=host_monitor_loop, daemon=True)
    host_monitor_thread.start()

    api_url = f"http://{HOST}:{port}/api/state"
    host_url = f"http://{HOST}:{port}/host"
    viewer_url = f"http://{HOST}:{port}/"

    if not wait_for_server(api_url):
        safe_print("Sunucu baslatilamadi. Lütfen port ve bagimliliklari kontrol edin.")
        if LOG_PATH:
            logging.error("Sunucu baslatilamadi. API yanit vermedi: %s", api_url)
        try:
            alt_port = find_any_port()
        except Exception as exc:
            log_exception("Alternatif port bulunamadi", exc)
            popup_server_start_failed(api_url)
            return 1

        if LOG_PATH:
            logging.info("Retrying server with alternative port %s", alt_port)
        server_thread = threading.Thread(target=run_server, args=(alt_port,), daemon=True)
        server_thread.start()

        api_url = f"http://{HOST}:{alt_port}/api/state"
        host_url = f"http://{HOST}:{alt_port}/host"
        viewer_url = f"http://{HOST}:{alt_port}/"

        if not wait_for_server(api_url):
            if LOG_PATH:
                logging.error("Sunucu baslatilamadi. API yanit vermedi: %s", api_url)
            popup_server_start_failed(api_url)
            return 1

    opened = launch_host_window(host_url)
    if opened:
        safe_print(f"Host penceresi acildi: {host_url}")
    else:
        safe_print(f"Pencere otomatik acilamadi. Manuel ac: {host_url}")
        popup_host_window_failed(host_url)

    safe_print(f"Izleyici linki: {viewer_url}")
    safe_print("Host sekmesi kapaninca uygulama otomatik kapanacaktir.")
    safe_print("Manuel kapatmak icin Ctrl+C.")

    try:
        while not _shutdown_event.is_set():
            time.sleep(0.5)
    except KeyboardInterrupt:
        return 0
    except Exception as exc:
        log_exception("Fatal error", exc)
        return 1
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
