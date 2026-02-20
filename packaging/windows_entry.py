import os
import socket
import sys
import threading
import time
import webbrowser
from pathlib import Path

import uvicorn


def print_banner(runtime_dir: Path, url: str):
    print("=" * 54)
    print("               INVOICE MANAGER v1.0")
    print("=" * 54)
    print("[1/4] Startēju serveri uz porta 8000...")
    print(f"[2/4] Datu fails: {runtime_dir / 'nc_invoice_manager.db'}")
    print("[3/4] Gaidu servera gatavību...")


def wait_for_server(host: str, port: int, timeout: float = 25.0) -> bool:
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=1.0):
                return True
        except OSError:
            time.sleep(0.3)
    return False


def open_chrome_or_default(url: str):
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for chrome in chrome_paths:
        if Path(chrome).exists():
            webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(chrome))
            webbrowser.get("chrome").open(url)
            return "Chrome"
    webbrowser.open(url)
    return "Default browser"


def main():
    runtime_dir = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parents[1]
    os.chdir(runtime_dir)

    from app.main import app  # import after cwd is set

    host = "127.0.0.1"
    port = 8000
    url = f"http://{host}:{port}"

    print_banner(runtime_dir, url)

    config = uvicorn.Config(app, host=host, port=port, log_level="info")
    server = uvicorn.Server(config)

    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    if wait_for_server(host, port):
        browser_name = open_chrome_or_default(url)
        print("[4/4] Gatavs.")
        print(f"[OK] Atvērts: {url} ({browser_name})")
        print("[INFO] Aizver šo logu vai spied CTRL+C, lai apturētu serveri.")
    else:
        print("[ERROR] Serveris nestartējās laikā.")
        return

    try:
        while thread.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[INFO] Apturu serveri...")
        server.should_exit = True
from pathlib import Path
import uvicorn

from app.main import app


def main():
    root = Path(__file__).resolve().parent
    os.chdir(root)
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")


if __name__ == "__main__":
    main()
