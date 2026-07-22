# biocraft-marketplace

Plugin registry for [biocraft-spark](https://github.com/deciduous/biocraft-spark),
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

## Cloudflare Pages configuration

- **Build command:** `pip install pyyaml && python scripts/build_index.py`
- **Build output directory:** `.` (the root serves `index.json` + `plugins/`)
- **Production domain:** `https://biocraft-marketplace.pages.dev`
