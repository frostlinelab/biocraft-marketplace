#!/usr/bin/env python3
"""Build the marketplace catalog into public/ for Cloudflare deployment.

Scans plugins/**/*.plugin.yaml, computes sha256, reads the curated allowlist
(beautiful-creatures.txt), copies the plugin manifests into public/, and writes
a pretty-printed public/index.json. The public/ directory is the wrangler
assets directory (see wrangler.jsonc), so only the catalog and manifests are
served — never the source scripts or repo metadata.
"""
import hashlib
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PLUGINS_DIR = ROOT / "plugins"
CURATED_FILE = ROOT / "beautiful-creatures.txt"
PUBLIC_DIR = ROOT / "public"
INDEX_FILE = PUBLIC_DIR / "index.json"
DEFAULT_BASE = "https://biocraft-marketplace.pages.dev"


def _load_curated() -> set[str]:
    """Return the set of curated plugin names from beautiful-creatures.txt."""
    if not CURATED_FILE.exists():
        return set()
    names: set[str] = set()
    for line in CURATED_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        names.add(line)
    return names


def _scan(base: str, curated: set[str]) -> list[dict]:
    """Collect plugin metadata from every *.plugin.yaml under plugins/."""
    plugins: list[dict] = []
    if not PLUGINS_DIR.exists():
        return plugins
    files = sorted(PLUGINS_DIR.rglob("*.plugin.yaml"))
    for f in files:
        try:
            data = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as e:
            print(f"WARNING: skipping {f}: {e}", file=sys.stderr)
            continue
        name = str(data.get("name", "")).strip()
        if not name:
            print(f"WARNING: skipping {f}: no name", file=sys.stderr)
            continue
        rel = f.relative_to(ROOT).as_posix()
        plugins.append({
            "name": name,
            "version": str(data.get("version", "")),
            "description": str(data.get("description", "")),
            "icon": str(data.get("icon", "process")),
            "author": str(data.get("author", "official")),
            "curated": name in curated,
            "yaml_url": f"{base}/{rel}",
            "sha256": hashlib.sha256(f.read_bytes()).hexdigest(),
        })
    return plugins


def _prepare_public() -> None:
    """Recreate public/ from scratch and copy the plugin manifests into it.

    A clean rebuild avoids stale manifests lingering after a plugin is removed.
    Only the catalog (index.json) and plugin YAMLs land here — everything under
    public/ is uploaded as static assets by wrangler.
    """
    if PUBLIC_DIR.exists():
        shutil.rmtree(PUBLIC_DIR)
    PUBLIC_DIR.mkdir(parents=True)
    if PLUGINS_DIR.exists():
        shutil.copytree(PLUGINS_DIR, PUBLIC_DIR / "plugins")


def main() -> int:
    base = os.environ.get("MARKETPLACE_BASE_URL", DEFAULT_BASE).rstrip("/")
    curated = _load_curated()
    plugins = _scan(base, curated)
    _prepare_public()
    index = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "plugins": plugins,
    }
    INDEX_FILE.write_text(
        json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Wrote {INDEX_FILE} ({len(plugins)} plugin(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
