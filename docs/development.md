# Development and Documentation

## Repository Structure

| Folder | Content |
| --- | --- |
| `src/tiledland/geometry/` | Primitives and grid conversion |
| `src/tiledland/artist/` | Brushes, artists, and supports |
| `src/tiledland/game/` | Experimental scenarios |
| `src/tiledland/interface/` | Integrations, including map loading |
| `tests/` | Tests and reference resources |
| `demo/` | Demonstrations, some of which are old |
| `docs/` | Markdown sources of this site |

## Running Tests

From the root of the repository, after project installation:

```sh
python -m pip install pytest
python -m pytest -q -k 'not long'
python -m pytest -q tests/06-regressions
```

The filter excludes names containing `long`; it is not a universal guarantee of duration. Some tests write `shot-*` files in the current directory. Use a dedicated working copy to avoid overwriting renders you wish to keep.

Regression tests describe the expected behavior even when the code does not yet respect it. See the [current balance](limitations.md).

## Building the MkDocs Site

```sh
python -m pip install -r requirements-docs.txt
python -m mkdocs serve
```

The command displays the local server address. For a controlled build:

```sh
python -m mkdocs build --strict
```

The configuration preserves the `readthedocs` theme, local CSS, and Markdown sources. The static site is produced in `site/`. Search is provided by the MkDocs `search` plugin.

## Adding a Page

Create the file in `docs/`, add it to the `mkdocs.yml` navigation, use relative links to other pages, and execute examples before building the site. Specify when a block depends on a repository resource or an optional component.

## Publishing

Build then examine the site before publishing it. The existing script `bin/docs-deploy.sh` depends on `config.toml` and performs Git operations, including a remote push. This is not a simple local preview. No publication was performed during the writing of this documentation.
