# Table-Remodeler Developer Instructions

> **Local environment**: If `.status/local-environment.md` exists in the repo root, read it first for OS- and shell-specific setup (virtual environment activation, command syntax, etc.).

Use Google-format docstrings (`Parameters:` not `Args:`). Place all work summaries in `.status/` at the repo root.

## Project Overview

`table-remodeler` (PyPI package: `table-remodeler`, importable as `remodeler`) transforms tabular data files through JSON-configurable operation pipelines. Primary use case: neuroimaging event file preprocessing with optional HED (Hierarchical Event Descriptors) annotation support. Python 3.10+, pandas 2.x (**pandas 3 is not supported**), MIT license.

Related: [hed-python](https://github.com/hed-standard/hed-python) (required `hedtools` dependency), [hed-schemas](https://github.com/hed-standard/hed-schemas).

## Repository Layout

```
remodeler/                  # Main package — always import as `remodeler`
  __init__.py               # Exports: Dispatcher, BackupManager, RemodelerValidator
  dispatcher.py             # Orchestrates operation execution and file I/O
  backup_manager.py         # Dataset backup/restore with timestamped versions
  remodeler_validator.py    # Validates remodeling JSON specifications
  cli/                      # CLI entry points (run_remodel, run_remodel_backup, run_remodel_restore)
  operations/               # All operation classes
    valid_operations.py     # Registry: maps string names → operation classes
    base_op.py              # BaseOp abstract class
    base_summary.py         # BaseSummary abstract class
tests/                      # unittest suite; mirrors remodeler/ structure
  data/                     # Test data files (TSV, JSON)
  cli/                      # CLI tests
  operations/               # Operation-level tests
.github/workflows/          # CI: ci.yaml, ci_windows.yaml, ruff.yaml, codespell.yaml, docs.yml, links.yml
pyproject.toml              # Build config, all dependencies, ruff + codespell settings
qlty.toml                   # Code quality thresholds (complexity, line counts)
.status/                    # Work summaries and local notes (ignored by ruff)
```

## Bootstrap & Build

```bash
# Install with all extras — always required before running tests
pip install -e .[test,docs,examples]
```

Editable install is required; plain `pip install -e .` is sufficient for non-docs/examples work.

## Running Tests

```bash
python -m unittest discover tests -v                                          # All tests
python -m unittest tests.test_dispatcher.Test.test_constructor                # Single test
```

Use `unittest` exclusively — never pytest. Test data lives in `tests/data/`.

## Linting & Style

Ruff is configured in `pyproject.toml` (`[tool.ruff]`): line length 120, target py310.

```bash
ruff check .              # Lint
ruff format --check .     # Format check (use `ruff format .` to auto-fix)
codespell .               # Spell check (skips TSV, YAML, JSON, TOML, etc.)
```

Key ruff ignores: `E501` (line length), `N802/803/806` (lowercase naming in scientific code).

## CI Workflows (`.github/workflows/`)

All checks run on push/PR to `main` and must pass before merging.

| Workflow | What it checks |
|---|---|
| `ci.yaml` | Tests on ubuntu-latest, Python 3.10–3.14 (3.10+3.13 on non-main branches) |
| `ci_windows.yaml` | Tests on windows-latest, Python 3.10–3.12 |
| `ruff.yaml` | `ruff check` + `ruff format --check` |
| `codespell.yaml` | Spelling via codespell |
| `docs.yml` | Sphinx documentation build |
| `links.yml` | Link validation |

## Key Implementation Patterns

### Imports

```python
from remodeler import Dispatcher, BackupManager, RemodelerValidator
from remodeler.operations.base_op import BaseOp
```

### Adding a new operation

1. Create `remodeler/operations/my_op.py` inheriting `BaseOp`; define `NAME`, `PARAMS` (JSON schema), `do_op(dispatcher, df, name, sidecar=None)`, and `validate_input_data(parameters)`.
2. Register in `remodeler/operations/valid_operations.py`.

### Registered operations

`factor_column`, `factor_hed_tags`, `factor_hed_type`, `merge_consecutive`, `remap_columns`, `remove_columns`, `remove_rows`, `rename_columns`, `reorder_columns`, `split_rows`, `summarize_column_names`, `summarize_column_values`, `summarize_definitions`, `summarize_hed_tags`, `summarize_hed_type`, `summarize_hed_validation`, `summarize_sidecar_from_events`

### Basic pipeline example

```python
from remodeler import Dispatcher

operations = [
    {"operation": "remove_columns", "parameters": {"column_names": ["col1"]}},
    {"operation": "rename_columns", "parameters": {"column_mapping": {"old": "new"}}},
]
dispatcher = Dispatcher(operations, data_root="/path/to/dataset")
dispatcher.run_operations()
```

## Dependencies & Constraints

- `pandas>=2.2.3,<3.0.0` — **pandas 3 not supported**
- `hedtools>=0.9.0` — HED operations; schemas auto-cached in `~/.hedtools/`
- `jsonschema>=4.23.0`

## Common Pitfalls

- Import from `remodeler` (not `remodel`) — the package directory is `remodeler/`
- Always install with `pip install -e .[test,docs,examples]` before running tests
- Use `unittest` exclusively — not pytest
- Do not hardcode HED schema versions; use `Dispatcher`'s `hed_versions` parameter
- Summaries save to `remodel/summaries/` at runtime; status notes go in `.status/`
