"""One-click Starcel bootstrapper.

Frozen to StarcelInstaller.exe via PyInstaller. Designed to be runnable on a
fresh Windows install with no Python present.

Flow (auto mode):
  0. Request UAC elevation.
  1. Show donation dialog.
  2. Detect existing Python 3.9.x.
  3. If missing: prompt user about PATH behavior, then silently install
     python-3.9.13-amd64.exe to C:\\Program Files\\Python39.
  4. pip install 'starcel[alpha]' (via absolute-path python.exe).
  5. starcel install  (which downloads build + installs prereqs + shortcuts + env + firewall).
  6. Show success dialog with donation links and "Launch Starcel?" button.

Manual mode: writes Starcel-Install-Guide.html to the desktop and opens it.
"""
from __future__ import annotations

import argparse
import ctypes
import os
import subprocess
import sys
import tempfile
import tkinter as tk
import urllib.request
import webbrowser
import winreg
from pathlib import Path
from tkinter import messagebox


PYTHON_INSTALLER_URL = "https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe"
PYTHON_TARGET_DIR    = Path(r"C:\Program Files\Python39")
DONATION_URLS = {
    "Patreon": "https://www.patreon.com/RecursionIs",
    "PayPal":  "https://www.paypal.com/paypalme/RecursionIs",
}


def is_admin() -> bool:
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def relaunch_as_admin(argv: list[str]) -> None:
    """Re-launch the current process with UAC elevation. Exits if successful."""
    params = " ".join(f'"{a}"' for a in argv)
    rc = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
    if rc > 32:
        sys.exit(0)
    raise RuntimeError(f"UAC elevation denied (ShellExecuteW rc={rc})")


def detect_python_39() -> Path | None:
    """Return the path to an existing Python 3.9.x, or None."""
    for candidate in [
        PYTHON_TARGET_DIR / "python.exe",
        Path(r"C:\Python39\python.exe"),
    ]:
        if candidate.exists() and _is_39(candidate):
            return candidate

    try:
        result = subprocess.run(
            ["py", "-3.9", "-c", "import sys; print(sys.executable)"],
            capture_output=True, text=True, check=False, timeout=10,
        )
        if result.returncode == 0:
            p = Path(result.stdout.strip())
            if p.exists():
                return p
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    try:
        result = subprocess.run(["python", "--version"], capture_output=True, text=True, check=False, timeout=10)
        if result.returncode == 0 and "3.9" in result.stdout + result.stderr:
            exe = subprocess.run(
                ["python", "-c", "import sys; print(sys.executable)"],
                capture_output=True, text=True, check=False, timeout=10,
            ).stdout.strip()
            if exe and Path(exe).exists():
                return Path(exe)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    for hive in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
        try:
            with winreg.OpenKey(hive, r"SOFTWARE\Python\PythonCore\3.9\InstallPath") as k:
                install_dir = Path(winreg.QueryValueEx(k, "")[0])
                exe = install_dir / "python.exe"
                if exe.exists():
                    return exe
        except OSError:
            continue
    return None


def _is_39(exe: Path) -> bool:
    try:
        result = subprocess.run(
            [str(exe), "--version"], capture_output=True, text=True, check=False, timeout=10,
        )
        return "3.9" in result.stdout + result.stderr
    except (OSError, subprocess.TimeoutExpired):
        return False


def ask_path_choice() -> bool | None:
    """Ask whether to prepend Python to PATH. Returns True/False, or None if cancelled."""
    root = tk.Tk()
    root.title("Starcel Installer — Python PATH")
    root.geometry("560x320")
    root.resizable(False, False)

    tk.Label(
        root,
        text="Starcel needs Python 3.9. Add it to the system PATH?",
        font=("Segoe UI", 11, "bold"),
        pady=12,
    ).pack()

    choice = tk.IntVar(value=1)
    options = [
        (1, "Install Python 3.9.13 and add to PATH  (recommended for most users)"),
        (2, "Install Python 3.9.13 WITHOUT changing PATH\n    (I have another Python version on PATH I want to keep)"),
        (3, "Cancel — I'll install Python myself"),
    ]
    for val, text in options:
        tk.Radiobutton(root, text=text, variable=choice, value=val, justify="left",
                        anchor="w", wraplength=520).pack(fill="x", padx=20, pady=4)

    result: dict[str, bool | None] = {"value": None}

    def on_ok() -> None:
        v = choice.get()
        if v == 1:   result["value"] = True
        elif v == 2: result["value"] = False
        else:        result["value"] = None
        root.destroy()

    tk.Button(root, text="OK", command=on_ok, width=16).pack(pady=16)
    root.mainloop()
    return result["value"]


def install_python(prepend_to_path: bool) -> None:
    with tempfile.TemporaryDirectory(prefix="starcel-bootstrap-") as tmpdir:
        installer = Path(tmpdir) / "python-3.9.13-amd64.exe"
        print(f"Downloading {PYTHON_INSTALLER_URL}...")
        urllib.request.urlretrieve(PYTHON_INSTALLER_URL, installer)
        cmd = [
            str(installer),
            "/quiet",
            "InstallAllUsers=1",
            f'TargetDir={PYTHON_TARGET_DIR}',
            f"PrependPath={1 if prepend_to_path else 0}",
            "Include_test=0",
            "SimpleInstall=1",
        ]
        print("Running Python installer (silent)...")
        subprocess.run(cmd, check=True)


def show_donation_banner(title: str) -> None:
    try:
        root = tk.Tk()
        root.title("Starcel")
        root.geometry("480x240")
        tk.Label(root, text=title, font=("Segoe UI", 11, "bold"), pady=16, wraplength=440).pack()
        for name, url in DONATION_URLS.items():
            link = tk.Label(root, text=f"{name}: {url}", fg="blue", cursor="hand2")
            link.pack(pady=2)
            link.bind("<Button-1>", lambda _e, u=url: webbrowser.open(u))
        tk.Button(root, text="Continue", command=root.destroy, width=14).pack(pady=16)
        root.mainloop()
    except Exception:
        print(f"\n{title}")
        for name, url in DONATION_URLS.items():
            print(f"  {name}: {url}")


def auto_install() -> None:
    show_donation_banner("Thanks for installing Starcel — consider supporting:")

    python = detect_python_39()
    if python is None:
        prepend = ask_path_choice()
        if prepend is None:
            webbrowser.open("https://www.python.org/downloads/release/python-3913/")
            print("Cancelled. Install Python 3.9 manually, then re-run this installer.")
            return
        install_python(prepend_to_path=prepend)
        python = PYTHON_TARGET_DIR / "python.exe"
        if not python.exists():
            raise RuntimeError(f"Python install completed but {python} is missing.")

    print(f"Using Python: {python}")
    subprocess.run([str(python), "-m", "pip", "install", "--upgrade", "pip"], check=True)
    subprocess.run([str(python), "-m", "pip", "install", "starcel[alpha]"], check=True)
    subprocess.run([str(python), "-m", "starcel", "install"], check=True)

    show_donation_banner("Install complete! If Starcel is useful to you, support:")

    if _ask_launch():
        subprocess.Popen([str(python), "-m", "starcel", "run", "--offline"])


def _ask_launch() -> bool:
    try:
        return messagebox.askyesno("Starcel", "Launch Starcel now?")
    except Exception:
        return False


def manual_install() -> None:
    python = detect_python_39()
    if python is not None:
        subprocess.run([str(python), "-m", "pip", "install", "starcel[alpha]"], check=False)
        subprocess.run([str(python), "-m", "starcel", "install", "--manual"], check=False)
        return

    guide_html = _static_manual_guide()
    output = Path.home() / "Desktop" / "Starcel-Install-Guide.html"
    output.write_text(guide_html, encoding="utf-8")
    print(f"Manual guide written to {output}")
    webbrowser.open(output.as_uri())


def _static_manual_guide() -> str:
    donation_html = " &nbsp;|&nbsp; ".join(
        f'<a href="{url}">{name}</a>' for name, url in DONATION_URLS.items()
    )
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Starcel Manual Install</title>
<style>body {{ font: 15px/1.5 system-ui, sans-serif; max-width: 760px; margin: 40px auto; padding: 0 20px; }}
a {{ color: #2a5a9a; }}</style></head><body>
<h1>Starcel Manual Install</h1>
<div style="background:#fff8e1;padding:12px;border-left:4px solid #f5b700;border-radius:4px;margin:16px 0">
  Support Starcel: {donation_html}
</div>
<ol>
  <li>Download Python 3.9.13:
      <a href="https://www.python.org/downloads/release/python-3913/">python.org/downloads/release/python-3913</a>
      — pick "Windows installer (64-bit)", check "Add python.exe to PATH", click Install Now.</li>
  <li>Open a new Command Prompt and run:
      <pre>pip install starcel[alpha]
starcel install</pre></li>
  <li>Wait for the build download to complete (~1.5 GB). It installs to Documents\\Starcel.</li>
  <li>Launch Starcel from the Desktop shortcut, or run <code>starcel</code> from a terminal.</li>
</ol>
</body></html>"""


def main() -> None:
    parser = argparse.ArgumentParser(prog="StarcelInstaller")
    parser.add_argument("--manual", action="store_true", help="write click-through guide instead of silent install")
    args, _ = parser.parse_known_args()

    if not is_admin():
        relaunch_as_admin(sys.argv[1:])
        return

    try:
        if args.manual:
            manual_install()
        else:
            auto_install()
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Starcel Installer", f"A step failed (exit code {e.returncode}).\n"
                                                  "See the console window for details. Falling back to manual guide.")
        manual_install()
    except Exception as e:
        messagebox.showerror("Starcel Installer", f"Unexpected error: {e}\nFalling back to manual guide.")
        manual_install()


if __name__ == "__main__":
    main()
