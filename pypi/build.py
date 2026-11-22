"""Prepare and build the `starcel` PyPI package.

    python pypi/build.py [--zip PATH] [--no-build]

1. Copies Content/Scripts out of the packaged build zip
   (default: BuildTest/WindowsNoEditor.zip) into src/starcel/scripts.
2. Copies the repo README.md (relative links rewritten to GitHub URLs so they
   render on PyPI) and LICENSE next to pyproject.toml.
3. Runs `uv build` (sdist + wheel into pypi/dist).

Upload afterwards with:  python -m twine upload pypi/dist/*
"""

import argparse
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
SCRIPTS_DEST = HERE / "src" / "starcel" / "scripts"
SCRIPTS_PREFIX = "WindowsNoEditor/Starcel9/Content/Scripts/"
GITHUB = "https://github.com/recursionis/starcel"
RAW = "https://raw.githubusercontent.com/recursionis/starcel/master"

# Paths (relative to Content/Scripts) left out of the package.
EXCLUDE_PARTS = {"__pycache__", ".github", ".pytest_cache", "bench"}
EXCLUDE_SUFFIXES = {".pyc", ".pyo", ".exe", ".class"}


def sync_scripts(zip_path):
    if SCRIPTS_DEST.exists():
        shutil.rmtree(SCRIPTS_DEST)
    count = 0
    with zipfile.ZipFile(zip_path) as zf:
        for info in zf.infolist():
            if info.is_dir() or not info.filename.startswith(SCRIPTS_PREFIX):
                continue
            rel = PurePosixPath(info.filename[len(SCRIPTS_PREFIX):])
            if ".." in rel.parts or rel.is_absolute():
                raise SystemExit("unsafe path in zip: " + info.filename)
            if EXCLUDE_PARTS.intersection(rel.parts) or rel.suffix.lower() in EXCLUDE_SUFFIXES:
                continue
            target = SCRIPTS_DEST.joinpath(*rel.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(info) as src, open(target, "wb") as dst:
                shutil.copyfileobj(src, dst)
            count += 1
    if count == 0:
        raise SystemExit("No files under %s found in %s" % (SCRIPTS_PREFIX, zip_path))
    print("Copied %d script files -> %s" % (count, SCRIPTS_DEST))


def _absolute(url, image):
    if re.match(r"^([a-z]+:|#|/)", url, re.I):
        return url
    return "%s/%s" % (RAW, url) if image else "%s/blob/master/%s" % (GITHUB, url)


def copy_readme():
    text = (REPO / "README.md").read_text(encoding="utf-8")
    text = re.sub(r'(src=")([^"]+)(")', lambda m: m.group(1) + _absolute(m.group(2), True) + m.group(3), text)
    text = re.sub(r"(!\[[^\]]*\]\()([^)\s]+)", lambda m: m.group(1) + _absolute(m.group(2), True), text)
    text = re.sub(r"((?<!!)\[[^\]]*\]\()([^)\s]+)", lambda m: m.group(1) + _absolute(m.group(2), False), text)
    (HERE / "README.md").write_text(text, encoding="utf-8")
    shutil.copyfile(REPO / "LICENSE", HERE / "LICENSE")
    print("Copied README.md and LICENSE")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--zip", type=Path, default=REPO / "BuildTest" / "WindowsNoEditor.zip")
    ap.add_argument("--no-build", action="store_true", help="only sync files, don't run uv build")
    args = ap.parse_args()

    sync_scripts(args.zip)
    copy_readme()
    if not args.no_build:
        dist = HERE / "dist"
        if dist.exists():
            shutil.rmtree(dist)
        subprocess.check_call([sys.executable, "-m", "uv", "build", str(HERE), "--out-dir", str(dist)])
        wheel = next(dist.glob("*.whl"))
        with zipfile.ZipFile(wheel) as zf:
            bundled = [n for n in zf.namelist() if n.startswith("starcel/scripts/")]
        if not bundled:
            raise SystemExit(f"{wheel.name} contains no starcel/scripts files - refusing to continue.")
        print(f"{wheel.name}: {len(bundled)} script files bundled")
        subprocess.check_call([sys.executable, "-m", "twine", "check", "--strict"]
                              + [str(p) for p in sorted(dist.iterdir()) if p.suffix in (".whl", ".gz")])


if __name__ == "__main__":
    main()
