"""Find, download, verify and install the newest Starcel build from GitHub Releases."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path, PurePosixPath

import requests
from tqdm import tqdm

from . import config, paths

_RESERVED_TOP_LEVEL = {"bin", "backups", "release.json", "settings.ini"}


def _headers(api: bool = False) -> dict:
    headers = {"User-Agent": f"starcel-installer/{config.VERSION}"}
    if api:
        headers["Accept"] = "application/vnd.github+json"
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"
    return headers


def download(url: str, dest: Path, *, label: str | None = None) -> Path:
    """Stream `url` to `dest` with a tqdm progress bar. Returns dest."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    label = label or dest.name
    with requests.get(url, stream=True, timeout=60, headers=_headers()) as r:
        r.raise_for_status()
        total = int(r.headers.get("Content-Length", 0)) or None
        with open(dest, "wb") as f, tqdm(
            total=total, unit="B", unit_scale=True, desc=label
        ) as bar:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
                    bar.update(len(chunk))
    return dest


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_sha256(path: Path, expected_hex: str) -> None:
    actual = sha256_of(path)
    if actual.lower() != expected_hex.strip().lower():
        raise RuntimeError(
            f"SHA256 mismatch for {path.name}:\n  expected: {expected_hex}\n  actual:   {actual}"
        )


# --- GitHub release lookup -------------------------------------------------

def latest_release() -> dict:
    """Newest published (non-draft) release that has a build zip.

    Pre-releases count too, since Starcel ships alpha builds.
    """
    url = f"https://api.github.com/repos/{config.GAME_REPO}/releases?per_page=20"
    r = requests.get(url, headers=_headers(api=True), timeout=30)
    r.raise_for_status()
    releases = [rel for rel in r.json() if not rel.get("draft")]
    releases.sort(key=lambda rel: rel.get("published_at") or "", reverse=True)
    for rel in releases:
        assets = {a["name"]: a for a in rel.get("assets", [])}
        name = next((n for n in config.BUILD_ASSET_NAMES if n in assets), None)
        if name is None:
            continue
        asset = assets[name]
        sha = assets.get(name + ".sha256")
        return {
            "tag": rel["tag_name"],
            "name": rel.get("name") or rel["tag_name"],
            "asset_id": asset["id"],
            "asset_name": name,
            "updated_at": asset["updated_at"],
            "size": asset["size"],
            "url": asset["browser_download_url"],
            "sha256_url": sha["browser_download_url"] if sha else None,
        }
    raise RuntimeError(
        f"No release with any of {config.BUILD_ASSET_NAMES} found at "
        f"https://github.com/{config.GAME_REPO}/releases"
    )


def installed_release() -> dict | None:
    try:
        return json.loads(config.RELEASE_STATE_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def is_current(state: dict | None, release: dict) -> bool:
    return bool(state) and all(state.get(k) == release[k] for k in ("tag", "asset_id", "updated_at"))


# --- Install / update -----------------------------------------------------

def _safe_extract(zip_path: Path, dest: Path) -> None:
    with zipfile.ZipFile(zip_path) as zf:
        for info in zf.infolist():
            rel = PurePosixPath(info.filename)
            if rel.is_absolute() or ".." in rel.parts or ":" in info.filename:
                raise RuntimeError(f"Refusing unsafe path in archive: {info.filename}")
        zf.extractall(dest)


def backup_scripts() -> Path | None:
    """Copy the installed Content/Scripts to backups/ so user edits survive updates."""
    try:
        src = paths.scripts_dir()
    except FileNotFoundError:
        return None
    if not src.is_dir():
        return None
    label = (installed_release() or {}).get("tag", "unknown")
    dest = config.BACKUPS_DIR / f"Scripts-{label}-{datetime.now():%Y%m%d-%H%M%S}"
    shutil.copytree(src, dest, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    return dest


def install_release(release: dict) -> None:
    """Download `release`, back up the current Scripts folder, and swap in the new build."""
    root = paths.install_root()
    root.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {release['name']} ({release['asset_name']}, "
          f"{release['size'] / 1e9:.2f} GB) to {root}...")

    with tempfile.TemporaryDirectory(dir=root, prefix=".download-") as tmpdir:
        tmp = Path(tmpdir)
        zip_path = download(release["url"], tmp / release["asset_name"], label="Starcel build")
        if release.get("sha256_url"):
            sha_path = download(release["sha256_url"], tmp / "build.sha256", label="SHA256")
            verify_sha256(zip_path, sha_path.read_text(encoding="utf-8").split()[0])
            print("SHA256 verified.")

        print("Extracting...")
        staging = tmp / "build"
        _safe_extract(zip_path, staging)
        zip_path.unlink()

        backup = backup_scripts()
        if backup:
            print(f"Backed up your previous Content/Scripts to {backup}")

        for item in staging.iterdir():
            if item.name.lower() in _RESERVED_TOP_LEVEL:
                continue
            target = root / item.name
            if target.is_dir():
                shutil.rmtree(target)
            elif target.exists():
                target.unlink()
            shutil.move(str(item), str(target))

    config.RELEASE_STATE_FILE.write_text(json.dumps(release, indent=2), encoding="utf-8")
    print(f"Installed {release['name']} to {paths.build_root()}")


def ensure_build(*, offline: bool = False, force: bool = False) -> None:
    """Install the newest release if missing or out of date.

    Network errors fall back to the installed build when there is one.
    """
    if offline:
        if not paths.is_installed():
            raise SystemExit(f"No Starcel build in {paths.install_root()}; run without --offline first.")
        return
    try:
        release = latest_release()
    except Exception as exc:
        if paths.is_installed():
            print(f"Could not check GitHub for updates ({exc}); using installed build.")
            return
        raise SystemExit(f"Could not reach GitHub to download Starcel: {exc}")
    if force or not paths.is_installed() or not is_current(installed_release(), release):
        install_release(release)
    else:
        print(f"{release['name']} is up to date.")


def download_python_installer(dest: Path) -> Path:
    return download(config.PYTHON_INSTALLER_URL, dest, label="Python 3.9.13 installer")


def download_vs2019_installer(dest: Path) -> Path:
    return download(config.VS2019_INSTALLER_URL, dest, label="VS 2019 installer")
