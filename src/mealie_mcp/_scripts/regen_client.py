"""Regenerate the Mealie OpenAPI client from the cached spec."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tomllib
from pathlib import Path

import httpx
import openapi_python_client
from dotenv import load_dotenv
from openapi_python_client.config import Config, ConfigFile, MetaType

REPO_ROOT = Path(__file__).resolve().parents[3]
SPEC_PATH = REPO_ROOT / "spec" / "mealie-openapi.json"
CLIENT_PATH = REPO_ROOT / "src" / "mealie_mcp" / "client"
PYPROJECT_PATH = REPO_ROOT / "pyproject.toml"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read_pinned() -> tuple[str, str]:
    data = tomllib.loads(PYPROJECT_PATH.read_text(encoding="utf-8"))
    pin = data["tool"]["mealie-mcp"]["spec"]
    return pin["version"], pin["sha256"]


def _write_pinned(version: str, sha256: str) -> None:
    text = PYPROJECT_PATH.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    in_section = False
    out: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            in_section = stripped == "[tool.mealie-mcp.spec]"
        if in_section and stripped.startswith("version = "):
            out.append(f'version = "{version}"\n')
        elif in_section and stripped.startswith("sha256 = "):
            out.append(f'sha256 = "{sha256}"\n')
        else:
            out.append(line)
    PYPROJECT_PATH.write_text("".join(out), encoding="utf-8")


def _fetch_spec() -> None:
    base_url = os.environ.get("MEALIE_BASE_URL")
    if not base_url:
        print(  # noqa: T201
            "MEALIE_BASE_URL must be set to fetch the spec with --update.",
            file=sys.stderr,
        )
        raise SystemExit(2)
    url = base_url.rstrip("/") + "/openapi.json"
    response = httpx.get(url, timeout=30.0)
    response.raise_for_status()
    SPEC_PATH.parent.mkdir(parents=True, exist_ok=True)
    SPEC_PATH.write_bytes(response.content)


def _verify_spec() -> str:
    if not SPEC_PATH.exists():
        print(  # noqa: T201
            f"Cached spec missing at {SPEC_PATH}. Run with --update to fetch it.",
            file=sys.stderr,
        )
        raise SystemExit(2)
    pinned_version, pinned_sha = _read_pinned()
    actual_sha = _sha256(SPEC_PATH)
    if actual_sha != pinned_sha:
        print(  # noqa: T201
            "SHA256 drift detected.\n"
            f"  pinned:   {pinned_sha}\n"
            f"  on disk:  {actual_sha}\n"
            "Run with --update to refresh the pin, or restore the cached spec.",
            file=sys.stderr,
        )
        raise SystemExit(1)
    info_version = str(json.loads(SPEC_PATH.read_text(encoding="utf-8"))["info"]["version"])
    if info_version != pinned_version:
        print(  # noqa: T201
            "OpenAPI info.version drift detected.\n"
            f"  pinned:   {pinned_version}\n"
            f"  on disk:  {info_version}\n"
            "Run with --update to refresh the pin.",
            file=sys.stderr,
        )
        raise SystemExit(1)
    return info_version


def _generate() -> None:
    if CLIENT_PATH.exists():
        shutil.rmtree(CLIENT_PATH)
    CLIENT_PATH.parent.mkdir(parents=True, exist_ok=True)
    config = Config.from_sources(
        config_file=ConfigFile(),
        meta_type=MetaType.NONE,
        document_source=SPEC_PATH,
        file_encoding="utf-8",
        overwrite=True,
        output_path=CLIENT_PATH,
    )
    errors = openapi_python_client.generate(config=config)
    fatal = [err for err in errors if err.level.value == "ERROR"]
    if fatal:
        for err in fatal:
            print(f"{err.header}: {err.detail}", file=sys.stderr)  # noqa: T201
        raise SystemExit(1)


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--update",
        action="store_true",
        help="Refresh the cached spec from MEALIE_BASE_URL and rewrite the pin.",
    )
    args = parser.parse_args()

    if args.update:
        _fetch_spec()
        info_version = json.loads(SPEC_PATH.read_text(encoding="utf-8"))["info"]["version"]
        _write_pinned(info_version, _sha256(SPEC_PATH))

    info_version = _verify_spec()
    print(f"Generating client for Mealie OpenAPI {info_version}")  # noqa: T201
    _generate()
    print(f"Client written to {CLIENT_PATH}")  # noqa: T201


if __name__ == "__main__":
    main()
