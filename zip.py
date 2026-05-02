#  Copyright (c) 2025 UF4OVER
#   All rights reserved.

from __future__ import annotations

import argparse
import shutil
import subprocess
import zipfile
from pathlib import Path


DEFAULT_BUILD_DIR = Path("build") / "AutoExcal"
DEFAULT_OUTPUT_DIR = Path("dist")
DEFAULT_ARTIFACT_NAME = "AutoExcal-windows-amd64.zip"


def remove_qt_translations(build_dir: Path):
    for translations_dir in build_dir.rglob("translations"):
        if translations_dir.is_dir() and "PyQt5" in str(translations_dir) and "Qt5" in str(translations_dir):
            shutil.rmtree(translations_dir, ignore_errors=True)
            print(f"Deleted translations folder: {translations_dir}")


def compress_with_upx(build_dir: Path, upx_path: Path):
    if not upx_path.exists():
        print(f"UPX not found, skip compression: {upx_path}")
        return

    for file_path in build_dir.rglob("*"):
        if not file_path.is_file() or file_path.suffix.lower() not in {".exe", ".dll", ".pyd"}:
            continue

        if all(part in str(file_path) for part in ("lib", "PyQt5", "Qt5", "plugins")):
            continue

        try:
            subprocess.run([str(upx_path), "--best", str(file_path)], check=True)
            print(f"Compressed: {file_path}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to compress {file_path}: {e}")


def create_zip_archive(build_dir: Path, output_dir: Path, artifact_name: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    zip_path = output_dir / artifact_name

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for file_path in build_dir.rglob("*"):
            if file_path.is_file():
                archive.write(file_path, file_path.relative_to(build_dir))

    print(f"Created archive: {zip_path}")
    return zip_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compress build output with UPX and package it as zip.")
    parser.add_argument("--build-dir", default=str(DEFAULT_BUILD_DIR), help="cx_Freeze build output directory")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="zip artifact output directory")
    parser.add_argument("--artifact-name", default=DEFAULT_ARTIFACT_NAME, help="zip file name")
    parser.add_argument("--upx", default="upx.exe", help="path to upx executable")
    parser.add_argument("--skip-upx", action="store_true", help="skip UPX compression")
    return parser.parse_args()


def main():
    args = parse_args()
    build_dir = Path(args.build_dir)
    output_dir = Path(args.output_dir)
    upx_path = Path(args.upx)

    if not build_dir.exists():
        raise FileNotFoundError(f"Build directory does not exist: {build_dir}")

    print(f"Using build directory: {build_dir}")
    remove_qt_translations(build_dir)

    if not args.skip_upx:
        compress_with_upx(build_dir, upx_path)

    create_zip_archive(build_dir, output_dir, args.artifact_name)


if __name__ == "__main__":
    main()

