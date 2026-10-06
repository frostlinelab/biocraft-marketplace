# biocraft-marketplace

<p align="center">
  <a href="https://frostlinelab.pages.dev"><img src="https://raw.githubusercontent.com/frostlinelab/.github/main/site/assets/banners/biocraft-marketplace.svg" alt="Biocraft Marketplace — a Frostline Lab project" width="820"></a>
</p>

Plugin registry for [biocraft-spark](https://github.com/frostlinelab/biocraft-spark),
statically hosted on **Cloudflare Pages**. Each plugin is a `.plugin.yaml`
manifest; this repo publishes an `index.json` catalog that biocraft-spark's
Marketplace page fetches to let users browse, install, and uninstall plugins.

> **Curation = certification.** A plugin enters this repo only after its code
> has been reviewed. Plugins promoted to the **Beautiful Creatures** selection
> are listed in `beautiful-creatures.txt`.

## Directory layout

```
biocraft-marketplace/
├── README.md
├── beautiful-creatures.txt   # curated allowlist (one plugin name per line)
├── plugins/
│   └── <name>/
│       └── <name>.plugin.yaml
├── scripts/
│   └── build_index.py        # generates index.json
└── index.json                # generated catalog (served by CF Pages)
```

## `index.json` contract

| Field         | Type    | Description                                                        |
|---------------|---------|--------------------------------------------------------------------|
| `schema_version` | int | Always `1`                                                         |
| `generated_at`   | str | UTC timestamp the index was built                                  |
| `plugins[]`      |     | One entry per `.plugin.yaml`                                       |
| `name`           | str | Plugin name (matches the YAML `name` field)                        |
| `version`        | str | Plugin version                                                     |
| `description`    | str | Short human-readable description                                   |
| `icon`           | str | Icon key (defaults to `process`)                                   |
| `author`         | str | Author (defaults to `official`)                                    |
| `curated`        | bool| `true` if listed in `beautiful-creatures.txt`                      |
| `yaml_url`       | str | Absolute URL to the plugin YAML on CF Pages                        |
| `sha256`         | str | SHA-256 of the plugin YAML file bytes                              |

## Curation workflow

1. **Review** the plugin's code (image, command, ports/params).
2. **Add** the manifest at `plugins/<name>/<name>.plugin.yaml`.
3. **(Optional)** promote to the selection by appending the plugin name to
   `beautiful-creatures.txt`.
4. **Commit & push** — Cloudflare Pages rebuilds `index.json` automatically.

## Building the index locally

```bash
pip install pyyaml
python scripts/build_index.py
```

Override the public base URL (e.g. for a preview deployment) with:

```bash
MARKETPLACE_BASE_URL=https://example.com python scripts/build_index.py
```

## Cloudflare Pages deployment

- **Build command:** `pip install pyyaml && python scripts/build_index.py`
- **Build output directory:** `public/` (only the catalog + manifests are served)
- **Production domain:** `https://biocraft-marketplace.pages.dev`

`build_index.py` emits into a clean `public/` directory so source scripts and
repo metadata are never uploaded as static assets. Pages serves `public/` as the
root, so URLs are `/index.json` and `/plugins/<name>/<name>.plugin.yaml`.

<p align="center">
  <a href="https://frostlinelab.pages.dev"><img src="https://raw.githubusercontent.com/frostlinelab/.github/main/site/assets/logos/biocraft-marketplace.svg" alt="" width="28" height="28"></a><br>
  <sub>Part of <a href="https://frostlinelab.pages.dev">Frostline Lab</a> · <a href="https://frostlinelab.pages.dev/gallery.html#biocraft-marketplace">All projects</a></sub>
</p>
