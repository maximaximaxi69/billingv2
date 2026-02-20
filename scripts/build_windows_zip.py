import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = ROOT / "dist"
PACKAGE_DIR = DIST_DIR / "NCInvoiceManager-windows"
ZIP_PATH = DIST_DIR / "NCInvoiceManager-windows.zip"


def run(cmd):
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main():
    if sys.platform != "win32":
        raise SystemExit("Šis skripts jāpalaiž uz Windows (win32), jo PyInstaller veido platformai specifisku EXE.")

    DIST_DIR.mkdir(exist_ok=True)

    run([sys.executable, "-m", "pip", "install", "-r", str(ROOT / "requirements.txt"), "pyinstaller"])

    run([
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--name",
        "NCInvoiceManager",
        "--add-data",
        "app\\templates;app\\templates",
        "--add-data",
        "app\\static;app\\static",
        "--collect-all",
        "reportlab",
        "--collect-all",
        "jinja2",
        str(ROOT / "packaging" / "windows_entry.py"),
    ])

    if PACKAGE_DIR.exists():
        shutil.rmtree(PACKAGE_DIR)
    PACKAGE_DIR.mkdir(parents=True, exist_ok=True)

    exe_src = DIST_DIR / "NCInvoiceManager.exe"
    shutil.copy2(exe_src, PACKAGE_DIR / "NCInvoiceManager.exe")

    (PACKAGE_DIR / "run.bat").write_text(
        "@echo off\n"
        "cd /d %~dp0\n"
        "title Invoice Manager\n"
        "echo Starting Invoice Manager...\n"
        "NCInvoiceManager.exe\n",
        encoding="utf-8",
    )

    (PACKAGE_DIR / "README-WINDOWS.txt").write_text(
        "NC Invoice Manager (Windows)\n"
        "===========================\n\n"
        "1) Double click run.bat (or NCInvoiceManager.exe).\n"
        "2) A terminal opens with status info.\n"
        "3) Browser opens automatically on http://127.0.0.1:8000\n"
        "4) Data is stored in nc_invoice_manager.db in this folder.\n",
        encoding="utf-8",
    )

    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    shutil.make_archive(str(ZIP_PATH.with_suffix("")), "zip", PACKAGE_DIR)

    print(f"\nDone: {ZIP_PATH}")


if __name__ == "__main__":
    main()
