# Table remodeler user guide

This comprehensive guide provides step-by-step instructions for using Table Remodeler in various scenarios, from basic column manipulation to complex HED-annotated data transformations.

## Quick links

- 📚 [API Reference](api/index.rst)
- 🐛 [GitHub Issues](https://github.com/hed-standard/table-remodeler/issues)
- 🔗 [hed-python](https://github.com/hed-standard/hed-python) - Core HED tools
- 📖 [HED Specification](https://hed-specification.readthedocs.io/)

## Table of contents

1. [Getting started](#getting-started)
2. [Basic data transformation](#basic-data-transformation)
3. [Working with hed annotations](#working-with-hed-annotations)
4. [Backup and restore](#backup-and-restore)
5. [Using the cli](#using-the-cli)
6. [Advanced workflows](#advanced-workflows)
7. [Creating custom operations](#creating-custom-operations)
8. [Best practices](#best-practices)
9. [Troubleshooting](#troubleshooting)

## Getting started

### Installation

Install Table Remodeler from PyPI:
```bash
pip install table-remodeler
```

For development with testing tools:
```bash
git clone https://github.com/hed-standard/table-remodeler.git
cd table-remodeler
pip install -e ".[dev,test]"
```

### Your first remodeling pipeline

Here's a simple example to get you started:

```python
from remodel import Dispatcher
import pandas as pd

# Define your remodeling operations
operations = [
    {
        "operation": "rename_columns",
        "parameters": {"column_mapping": {"old_col_name": "new_col_name"}}
    },
    {
        "operation": "remove_columns",
        "parameters": {"column_names": ["unwanted_column"]}
    }
]

# Create a dispatcher and run operations
dispatcher = Dispatcher(operations, data_root="/path/to/dataset")
dispatcher.run_operations()

print("✓ Remodeling complete!")
```

## Basic data transformation

### Renaming columns

```python
from remodel import Dispatcher

operations = [{
    "operation": "rename_columns",
    "parameters": {
        "column_mapping": {
            "stimulus_type": "trial_type",
            "resp_time": "response_time"
        }
    }
}]

dispatcher = Dispatcher(operations, data_root="/path/to/data")
dispatcher.run_operations()
```

### Removing columns

```python
operations = [{
    "operation": "remove_columns",
    "parameters": {
        "column_names": ["temporary_col", "debug_info"]
    }
}]
```

### Converting column types

```python
operations = [{
    "operation": "convert_columns",
    "parameters": {
        "column_names": ["duration", "response_time"],
        "data_type": "float"
    }
}]
```

### Reordering columns

```python
operations = [{
    "operation": "reorder_columns",
    "parameters": {
        "column_names": ["onset", "duration", "trial_type", "response"]
    }
}]
```

### Remapping values

```python
operations = [{
    "operation": "remap_columns",
    "parameters": {
        "remap": {
            "trial_type": {
                "go": "go_trial",
                "stop": "stop_trial"
            }
        }
    }
}]
```

## Working with hed annotations

### Validate hed strings

```python
operations = [{
    "operation": "summarize_hed_validation",
    "parameters": {
        "summary_name": "hed_validation_report"
    }
}]

dispatcher = Dispatcher(
    operations,
    data_root="/path/to/dataset",
    hed_versions="8.3.0"
)
dispatcher.run_operations()
```

### Summarize hed tags

```python
operations = [{
    "operation": "summarize_hed_tags",
    "parameters": {
        "summary_name": "hed_tags_summary"
    }
}]

dispatcher = Dispatcher(
    operations,
    data_root="/path/to/dataset",
    hed_versions="8.3.0"
)
dispatcher.run_operations()
```

### Factor hed tags

```python
operations = [{
    "operation": "factor_hed_tags",
    "parameters": {
        "tag_columns": {
            "visual_tags": ["Visual-presentation", "Red"],
            "action_tags": ["Action", "Button-press"]
        }
    }
}]
```

## Backup and restore

### Creating a backup

```python
from remodel import BackupManager

backup_manager = BackupManager(data_root="/path/to/dataset")
backup_manager.create_backup(backup_name="pre_remodeling")
```

### Automatic backup with dispatcher

```python
operations = [...]

dispatcher = Dispatcher(
    operations,
    data_root="/path/to/dataset",
    backup_name="automatic_backup"  # Creates backup automatically
)
dispatcher.run_operations()
```

### Restoring from Backup

```python
backup_manager = BackupManager(data_root="/path/to/dataset")
backup_manager.restore_backup(backup_name="pre_remodeling")
```

## Using the cli

### Running remodeling operations

```bash
run_remodel /path/to/dataset operations.json --verbose
```

**Common options:**
- `-v, --verbose`: Show detailed progress
- `-nb, --no-backup`: Skip automatic backup
- `-ns, --no-summaries`: Don't save summaries
- `-hv, --hed-versions 8.3.0`: Specify HED version for HED operations

### Creating a Backup

```bash
run_remodel_backup /path/to/dataset --backup-name my_backup
```

### Restoring from backup

```bash
run_remodel_restore /path/to/dataset --backup-name my_backup
```

## Advanced workflows

### Chaining multiple operations

```python
operations = [
    # First: standardize column names
    {
        "operation": "rename_columns",
        "parameters": {"column_mapping": {"stim": "stimulus", "resp": "response"}}
    },
    # Second: remove unnecessary columns
    {
        "operation": "remove_columns",
        "parameters": {"column_names": ["debug", "temp"]}
    },
    # Third: convert types
    {
        "operation": "convert_columns",
        "parameters": {"column_names": ["duration"], "data_type": "float"}
    },
    # Fourth: reorder for readability
    {
        "operation": "reorder_columns",
        "parameters": {
            "column_names": ["onset", "duration", "stimulus", "response"]
        }
    }
]

dispatcher = Dispatcher(operations, data_root="/path/to/data")
dispatcher.run_operations()
```

### Batch processing multiple datasets

```python
from pathlib import Path

datasets = Path("/data").glob("sub-*/")

operations = [
    {"operation": "rename_columns", "parameters": {...}},
    {"operation": "remove_columns", "parameters": {...}}
]

for dataset_dir in datasets:
    dispatcher = Dispatcher(operations, data_root=str(dataset_dir))
    dispatcher.run_operations()
    print(f"✓ Processed {dataset_dir.name}")
```

## Creating custom operations

Create custom remodeling operations by extending `BaseOp`:

```python
from remodel.operations.base_op import BaseOp
import pandas as pd

class MyCustomOp(BaseOp):
    NAME = "my_custom_operation"
    
    PARAMS = {
        "type": "object",
        "properties": {
            "column": {"type": "string"},
            "multiplier": {"type": "number"}
        },
        "required": ["column", "multiplier"]
    }
    
    def do_op(self, dispatcher, df, name, sidecar=None):
        """Multiply values in a column."""
        col = self.parameters["column"]
        mult = self.parameters["multiplier"]
        df[col] = df[col] * mult
        return df
    
    @staticmethod
    def validate_input_data(parameters):
        """Validate parameters."""
        return []  # No additional validation needed
```

Register your operation in `valid_operations.py`:
```python
from my_module import MyCustomOp

valid_operations = {
    # ... existing operations ...
    "my_custom_operation": MyCustomOp
}
```

## Best practices

1. **Always create backups** before applying operations to important datasets
2. **Test operations locally first** before applying to large datasets
3. **Use JSON operation files** for reproducibility and documentation
4. **Validate results** after applying operations (e.g., check row/column counts)
5. **Keep operation definitions simple** - chain multiple simple ops rather than creating complex ones
6. **Document your custom operations** with clear parameter descriptions
7. **Use meaningful backup names** with timestamps for easy identification

## Troubleshooting

### Common issues

#### "File not found" errors
- Ensure data paths are absolute paths, not relative
- Check that file extensions match (e.g., .tsv vs .csv)

#### "Column not found" errors
- Verify column names are spelled correctly (case-sensitive)
- Check operation order - maybe a column was removed by a previous operation

#### Hed validation fails with "Schema not found"
- Ensure internet connection for automatic schema download
- Schemas are cached in `~/.hedtools/`
- Specify HED version explicitly: `hed_versions="8.3.0"`

#### Operations run but files don't change
- Check that `--no-update` flag is not set in CLI
- Verify backup wasn't created instead (check backup directory)
- Ensure write permissions on data directory

### Getting help

- Check the [API Reference](api/index.rst) for detailed documentation
- Visit our [GitHub Issues](https://github.com/hed-standard/table-remodeler/issues) page
- Review examples in the repository README
