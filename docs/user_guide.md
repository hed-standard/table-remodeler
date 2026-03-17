# Remodeler user guide

This comprehensive guide provides step-by-step instructions for using Table Remodeler in various scenarios, from basic column manipulation to complex HED-annotated data transformations.

## Getting started

### Installation

Table-remodeler is available on PyPI and can be installed with pip:

```bash
pip install table-remodeler
```

**Development installation:**

For contributing to table-remodeler or running tests:

```bash
git clone https://github.com/hed-standard/table-remodeler.git
cd table-remodeler
pip install -e ".[dev,test]"
```

The `-e` flag installs in editable mode, so code changes are immediately reflected.

**Optional dependencies:**

Install specific extras as needed:

- **Development tools** (ruff, typos, mdformat): `pip install table-remodeler[dev]`
- **Testing tools** (coverage): `pip install table-remodeler[test]`
- **Documentation** (sphinx, furo): `pip install table-remodeler[docs]`
- **Jupyter examples** (jupyter, notebook): `pip install table-remodeler[examples]`

**Requirements:**

- Python 3.10 or later
- Core dependencies: pandas, numpy, jsonschema, openpyxl, semantic-version
- HED support: `hedtools` package (automatically installed from [hed-python](https://github.com/hed-standard/hed-python))

**Online tools:**

You can also use remodeling without installation via the [HED online tools](https://hedtools.org/hed/). Navigate to the Events page and select "Execute remodel script" to test operations on individual files. This is especially useful for debugging operations before running on full datasets.

### Your first remodeling pipeline

Here's a simple example to get you started:

```python
from remodeler import Dispatcher
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
from remodeler import Dispatcher

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

[HED (Hierarchical Event Descriptors)](https://www.hedtags.org/) is a system for annotating experimental data in a manner that is both human-understandable and machine-actionable. HED provides detailed semantic information about events, enabling advanced data analysis and automated information extraction.

Table-remodeler supports five HED-specific operations:

- `factor_hed_tags`: Extract factor vectors from HED tag queries
- `factor_hed_type`: Extract design matrices by HED tag type
- `summarize_hed_tags`: Summarize HED tag usage
- `summarize_hed_type`: Summarize specific HED types (e.g., Condition-variable)
- `summarize_hed_validation`: Validate HED annotations

If you're new to HED, see the [HED documentation](https://www.hedtags.org/hed-resources).

### HED schemas

HED annotations use a controlled vocabulary defined by HED schemas. Schemas are versioned (e.g., `8.3.0`) and automatically downloaded and cached in `~/.hedtools/` (cross-platform location) when needed. The `hedtools` package (from hed-python) manages schema loading and caching.

**Standard schema versions:**

```python
dispatcher = Dispatcher(operations, hed_versions="8.3.0")
```

**Multiple schemas with libraries:**

```python
# Using standard HED 8.3.0 + SCORE library 1.0.0
dispatcher = Dispatcher(
    operations,
    hed_versions=["8.3.0", "sc:score_1.0.0"]
)
```

When using multiple schemas, all but one must have a namespace prefix (e.g., `sc:`). Tags from that schema must use the prefix in annotations (e.g., `sc:Sleep-modulator`).

### Using HED with BIDS datasets

The easiest way to use HED operations is with BIDS-formatted datasets:

**Command line:**

```bash
run_remodel /data/my_bids_dataset /data/operations_rmdl.json -b -hv 8.3.0
```

The `-b` flag enables BIDS mode, which:

- Extracts HED schema version from `dataset_description.json`
- Automatically locates JSON sidecars for each data file
- Uses BIDS inheritance rules for annotation resolution

**Python:**

```python
from remodeler import Dispatcher

operations = [
    {
        "operation": "summarize_hed_validation",
        "parameters": {"summary_name": "validation_check"}
    }
]

dispatcher = Dispatcher(
    operations,
    data_root="/data/my_bids_dataset",
    hed_versions="8.3.0",
    bids_format=True
)
dispatcher.run_operations()
```

### Using HED with non-BIDS datasets

For non-BIDS datasets, explicitly provide the HED schema version and sidecar path:

**Command line:**

```bash
run_remodel /data/my_experiment /data/operations_rmdl.json \
  -hv 8.3.0 -j /data/my_experiment/task_events.json
```

**Python:**

```python
dispatcher = Dispatcher(
    operations,
    data_root="/data/my_experiment",
    hed_versions="8.3.0",
    json_sidecar="/data/my_experiment/task_events.json"
)
```

### HED validation

Validate HED annotations across all files:

```python
operations = [{
    "operation": "summarize_hed_validation",
    "parameters": {
        "summary_name": "hed_validation_report",
        "summary_filename": "validation_results"
    }
}]

dispatcher = Dispatcher(
    operations,
    data_root="/path/to/dataset",
    hed_versions="8.3.0",
    bids_format=True
)
dispatcher.run_operations()
```

Validation errors are reported in the summary file, not as exceptions. This allows you to see all validation issues at once.

### HED tag summaries

Generate comprehensive summaries of HED tag usage:

```python
operations = [{
    "operation": "summarize_hed_tags",
    "parameters": {
        "summary_name": "all_hed_tags",
        "summary_filename": "tag_usage"
    }
}]

dispatcher = Dispatcher(
    operations,
    data_root="/path/to/dataset",
    hed_versions="8.3.0",
    bids_format=True
)
dispatcher.run_operations()
```

The summary includes:

- All unique HED tags used
- Frequency of each tag
- Files containing each tag
- Tag hierarchy information

### Factoring HED tags

Extract binary factor columns based on HED tag queries:

```python
operations = [{
    "operation": "factor_hed_tags",
    "parameters": {
        "queries": [
            "Visual-presentation",
            "Auditory-presentation",
            "Action and Button-press"
        ],
        "query_names": [
            "has_visual",
            "has_auditory",
            "has_button_press"
        ]
    }
}]

dispatcher = Dispatcher(
    operations,
    data_root="/path/to/dataset",
    hed_versions="8.3.0",
    bids_format=True
)
dispatcher.run_operations()
```

This creates new columns (`has_visual`, `has_auditory`, `has_button_press`) with values 1 (match) or 0 (no match) for each row.

### Extracting experimental designs

Extract condition variables and design matrices using HED type tags:

```python
operations = [{
    "operation": "factor_hed_type",
    "parameters": {
        "type_tag": "Condition-variable",
        "type_values": ["stimulus-type", "response-hand"]
    }
}]

dispatcher = Dispatcher(
    operations,
    data_root="/path/to/dataset",
    hed_versions="8.3.0",
    bids_format=True
)
dispatcher.run_operations()
```

This automatically extracts experimental design information encoded with `Condition-variable` tags.

For more details on HED integration, see the [Transformation operations](./operations/transformations/index.rst) and [Summarization operations](./operations/summarizations/index.rst).

## Backup and restore

The backup system is a core safety feature of table-remodeler. Backups provide a mirror copy of your data files that remodeling always reads from, ensuring your original data is never modified.

### Backup directory structure

Backups are stored in `derivatives/remodel/backups/` under your dataset root:

```
dataset_root/
├── sub-001/
│   └── ses-01/
│       └── func/
│           └── sub-001_ses-01_task-rest_events.tsv
├── sub-002/
│   └── ...
└── derivatives/
    └── remodel/
        ├── backups/
        │   ├── default_back/           # Default backup
        │   │   ├── backup_lock.json    # Backup metadata
        │   │   └── backup_root/        # Mirrored file structure
        │   │       ├── sub-001/
        │   │       │   └── ses-01/
        │   │       │       └── func/
        │   │       │           └── sub-001_ses-01_task-rest_events.tsv
        │   │       └── sub-002/
        │   │           └── ...
        │   └── checkpoint_2024/        # Named backup
        │       └── ...
        ├── remodeling_files/
        │   └── operations_rmdl.json
        └── summaries/
            └── ...
```

### Creating backups

**Method 1: Command line (recommended for initial backup)**

```bash
# Create default backup
run_remodel_backup /path/to/dataset

# Create named backup
run_remodel_backup /path/to/dataset -bn checkpoint_2024 -v

# Backup only specific tasks (BIDS)
run_remodel_backup /path/to/dataset -t stopsignal -t gonogo
```

**Method 2: Python/Jupyter**

```python
from remodeler import BackupManager

backup_manager = BackupManager(data_root="/path/to/dataset")

# Create default backup
backup_manager.create_backup()

# Create named backup
backup_manager.create_backup(backup_name="before_major_changes")
```

**Method 3: Automatic with Dispatcher**

The Dispatcher can create backups automatically if they don't exist:

```python
from remodeler import Dispatcher

operations = [...]

dispatcher = Dispatcher(
    operations,
    data_root="/path/to/dataset",
    backup_name="auto_backup"  # Creates if doesn't exist
)
dispatcher.run_operations()
```

### How remodeling uses backups

**Critical concept:** Remodeling always reads from the backup and writes to the original file location.

```
Backup file → Remodeling operations → Original file
  (read)         (transform)            (write)
```

This means:

- ✅ Original data is never directly modified
- ✅ You can rerun operations multiple times safely
- ✅ Each run starts fresh from the original backup
- ✅ No need to restore between remodeling runs

**Example workflow:**

```bash
# 1. Create backup once
run_remodel_backup /data/my_dataset

# 2. Run remodeling (reads from backup, writes to originals)
run_remodel /data/my_dataset operations_v1_rmdl.json

# 3. Found a mistake? Just edit operations and rerun
#    (automatically starts fresh from backup)
run_remodel /data/my_dataset operations_v2_rmdl.json

# 4. Still not right? Edit and rerun again
run_remodel /data/my_dataset operations_v3_rmdl.json
```

### Named backups as checkpoints

Use multiple named backups as checkpoints in your workflow:

```python
from remodeler import BackupManager

backup_manager = BackupManager(data_root="/path/to/dataset")

# Checkpoint 1: Original data
backup_manager.create_backup(backup_name="01_original")

# ... perform initial cleanup remodeling ...

# Checkpoint 2: After cleanup
backup_manager.create_backup(backup_name="02_cleaned")

# ... perform analysis-specific transformations ...

# Checkpoint 3: Analysis-ready
backup_manager.create_backup(backup_name="03_analysis_ready")

# Later, start from checkpoint 2 for different analysis
dispatcher = Dispatcher(
    different_operations,
    data_root="/path/to/dataset",
    backup_name="02_cleaned"  # Use checkpoint as starting point
)
```

### Restoring from backups

**When to restore:**

- After completing analysis, to return files to original state
- To completely start over from a checkpoint
- To switch between different analysis workflows

**Method 1: Command line**

```bash
# Restore from default backup
run_remodel_restore /path/to/dataset

# Restore from named backup
run_remodel_restore /path/to/dataset -bn checkpoint_2024 -v

# Restore only specific tasks (BIDS)
run_remodel_restore /path/to/dataset -t stopsignal
```

**Method 2: Python/Jupyter**

```python
from remodeler import BackupManager

backup_manager = BackupManager(data_root="/path/to/dataset")

# Restore from default backup
backup_manager.restore_backup()

# Restore from named backup
backup_manager.restore_backup(backup_name="before_major_changes")
```

### Backup best practices

1. **Create backup before first remodeling**: Always run `run_remodel_backup` once before any transformations

2. **Don't delete backups**: They provide provenance and safety. Disk space is cheap compared to lost data.

3. **Use meaningful names**:

   ```bash
   # Good names
   run_remodel_backup /data -bn "2024-01-15_before_recoding"
   run_remodel_backup /data -bn "checkpoint_after_validation"

   # Less helpful
   run_remodel_backup /data -bn "backup1"
   run_remodel_backup /data -bn "test"
   ```

4. **No backup needed for summarization**: If you're only using summarization operations (no transformations), you can skip backup with `-nb`:

   ```bash
   run_remodel /data summaries_only_rmdl.json -nb
   ```

5. **Backup lock file**: Don't manually modify `backup_lock.json` - it's used internally by the remodeling tools

6. **Storage location**: Backups go in `derivatives/remodel/backups/` by default, but you can specify a different location:

   ```bash
   run_remodel_backup /data -bd /external_drive/backups
   ```

## Using the cli

The table-remodeler package provides three command-line scripts:

1. **run_remodel_backup**: Create backups of tabular files
2. **run_remodel**: Execute remodeling operations
3. **run_remodel_restore**: Restore files from backup

These scripts can be run from the command line or called from Python/Jupyter notebooks.

### Command-line argument types

**Positional arguments** are required and must appear in order:

- `data_dir`: Full path to dataset root directory
- `model_path`: Full path to JSON remodel file (run_remodel only)

**Named arguments** are optional and can appear in any order:

- Short form: single hyphen + letter (e.g., `-v`)
- Long form: double hyphen + name (e.g., `--verbose`)
- Flag arguments: presence = true, absence = false
- Value arguments: followed by one or more values

### run_remodel_backup

Create a backup of specified tabular files before remodeling.

**Basic usage:**

```bash
run_remodel_backup /path/to/dataset
```

**With options:**

```bash
run_remodel_backup /path/to/dataset -bn my_backup -x derivatives stimuli -v
```

**Available options:**

`-bd`, `--backup-dir PATH`

> Directory for backups (default: `[data_root]/derivatives/remodel/backups`)

`-bn`, `--backup-name NAME`

> Name for this backup (default: `default_back`). Use named backups as checkpoints.

`-fs`, `--file-suffix SUFFIX [SUFFIX ...]`

> File suffixes to process (default: `events`). Files must end with suffix (e.g., `events.tsv`).

`-t`, `--task-names TASK [TASK ...]`

> Process only specific tasks (BIDS format only). Omit to process all tasks.

`-v`, `--verbose`

> Print detailed progress messages.

`-x`, `--exclude-dirs DIR [DIR ...]`

> Exclude directories (e.g., `derivatives stimuli`). Paths with `remodeler` are auto-excluded.

**Example - BIDS dataset:**

```bash
run_remodel_backup /data/ds002790 -x derivatives -t stopsignal -v
```

**From Python/Jupyter:**

```python
import remodeler.cli.run_remodel_backup as cli_backup

data_root = '/path/to/dataset'
arg_list = [data_root, '-x', 'derivatives', 'stimuli', '-v']
cli_backup.main(arg_list)
```

### run_remodel

Execute remodeling operations specified in a JSON file.

**Basic usage:**

```bash
run_remodel /path/to/dataset /path/to/operations_rmdl.json
```

**Full example:**

```bash
run_remodel /data/ds002790 /data/ds002790/derivatives/remodel/remodeling_files/cleanup_rmdl.json \
  -b -x derivatives -t stopsignal -s .txt -s .json -hv 8.3.0 -v
```

**Available options:**

`-b`, `--bids-format`

> Dataset is BIDS-formatted. Enables automatic sidecar and schema detection.

`-bd`, `--backup-dir PATH`

> Directory containing backups (default: `[data_root]/derivatives/remodel/backups`)

`-bn`, `--backup-name NAME`

> Backup to use (default: `default_back`)

`-fs`, `--file-suffix SUFFIX [SUFFIX ...]`

> File suffixes to process (default: `events`)

`-hv`, `--hed-versions VERSION [VERSION ...]`

> HED schema versions for HED operations (e.g., `8.3.0` or `8.3.0 sc:score_1.0.0`)

`-i`, `--individual-summaries {separate,consolidated,none}`

> How to save individual file summaries:
>
> - `separate`: Each file in separate file + overall summary
> - `consolidated`: All in same file as overall summary
> - `none`: Only overall summary

`-j`, `--json-sidecar PATH`

> Path to JSON sidecar with HED annotations (for non-BIDS datasets)

`-ld`, `--log-dir PATH`

> Directory for log files (written on exceptions)

`-nb`, `--no-backup`

> Skip backup, operate directly on files (NOT RECOMMENDED)

`-ns`, `--no-summaries`

> Don't save summary files

`-nu`, `--no-update`

> Don't write modified files (useful for dry runs)

`-s`, `--save-formats EXT [EXT ...]`

> Summary formats (default: `.txt .json`)

`-t`, `--task-names TASK [TASK ...] | *`

> Tasks to process (BIDS only):
>
> - Omit: process all tasks, combined summaries
> - List: process listed tasks with separate summaries per task
> - `*`: process all tasks with separate summaries per task

`-v`, `--verbose`

> Print detailed progress

`-w`, `--work-dir PATH`

> Working directory for outputs (default: `[data_root]/derivatives/remodel`)

`-x`, `--exclude-dirs DIR [DIR ...]`

> Directories to exclude from processing

**Example - BIDS with HED:**

```bash
run_remodel /data/ds002790 /data/remodeling_files/hed_analysis_rmdl.json \
  -b -hv 8.3.0 -s .txt -s .json -x derivatives -v
```

**Example - Non-BIDS with explicit sidecar:**

```bash
run_remodel /data/my_experiment /data/my_experiment/cleanup_rmdl.json \
  -hv 8.3.0 -j /data/my_experiment/annotations.json -x derivatives
```

**From Python/Jupyter:**

```python
import remodeler.cli.run_remodel as cli_remodel

data_root = '/path/to/dataset'
model_path = '/path/to/operations_rmdl.json'
arg_list = [data_root, model_path, '-b', '-x', 'derivatives', '-v']
cli_remodel.main(arg_list)
```

**Important notes:**

- Always reads from backup (unless `-nb` specified)
- Overwrites original data files (backup remains safe)
- Can be run multiple times - always starts fresh from backup
- Summaries saved to `derivatives/remodel/summaries/`

### run_remodel_restore

Restore data files from a backup.

**Basic usage:**

```bash
run_remodel_restore /path/to/dataset
```

**With specific backup:**

```bash
run_remodel_restore /path/to/dataset -bn checkpoint_20240115 -v
```

**Available options:**

`-bd`, `--backup-dir PATH`

> Directory containing backups

`-bn`, `--backup-name NAME`

> Backup to restore from (default: `default_back`)

`-t`, `--task-names TASK [TASK ...]`

> Restore only specific tasks (BIDS only)

`-v`, `--verbose`

> Print detailed progress

**From Python/Jupyter:**

```python
import remodeler.cli.run_remodel_restore as cli_restore

data_root = '/path/to/dataset'
arg_list = [data_root, '-bn', 'my_backup', '-v']
cli_restore.main(arg_list)
```

**When to restore:**

- You don't need to restore between remodeling runs (always uses backup)
- Restore when finished with analysis to return to original state
- Restore if you want to start completely fresh

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

This section provides comprehensive documentation for developers who want to create custom remodeling operations for Table Remodeler. It covers the architecture, requirements, and best practices for extending the remodeling framework.

### Architecture overview

Operations are defined as classes that extend `BaseOp` regardless of whether they are transformations or summaries. However, summaries must also implement an additional supporting class that extends `BaseSummary` to hold the summary information.

In order to be executed by the remodeling functions, an operation must appear in the `valid_operations` dictionary located in `remodeler/operations/valid_operations.py`.

**Key components:**

- **BaseOp**: Abstract base class for all operations
- **BaseSummary**: Abstract base class for summary support classes
- **Dispatcher**: Orchestrates operation execution on datasets
- **RemodelerValidator**: Validates operation specifications against JSON schemas
- **valid_operations**: Registry dictionary mapping operation names to classes

### Operation class structure

Each operation class must have:

1. **NAME**: Class variable (string) specifying the operation name
2. **PARAMS**: Class variable containing a JSON schema dictionary of parameters
3. **Constructor**: Calls `super().__init__(parameters)` and sets up operation-specific properties
4. **do_op()**: Main method that performs the operation
5. **validate_input_data()**: Static method for additional validation beyond JSON schema

**Basic operation template:**

```python
from remodeler.operations.base_op import BaseOp

class MyCustomOp(BaseOp):
    """Brief description of what this operation does."""
    
    NAME = "my_custom_operation"
    
    PARAMS = {
        "type": "object",
        "properties": {
            "my_parameter": {
                "type": "string",
                "description": "Description of parameter"
            },
            "optional_param": {
                "type": "integer", 
                "description": "Optional parameter"
            }
        },
        "required": ["my_parameter"],
        "additionalProperties": False
    }
    
    def __init__(self, parameters):
        """Initialize the operation with validated parameters."""
        super().__init__(parameters)
        self.my_parameter = parameters['my_parameter']
        self.optional_param = parameters.get('optional_param', None)
    
    def do_op(self, dispatcher, df, name, sidecar=None):
        """
        Execute the operation on a DataFrame.
        
        Parameters:
            dispatcher (Dispatcher): The dispatcher managing operations
            df (pd.DataFrame): The tabular data to transform
            name (str): Identifier for the file (for error messages)
            sidecar (dict): Optional JSON sidecar for HED operations
            
        Returns:
            pd.DataFrame: The transformed DataFrame
        """
        # Your transformation logic here
        # For transformations, return modified DataFrame
        # For summaries, update dispatcher.summary_dict and return original df
        return df
    
    @staticmethod
    def validate_input_data(parameters):
        """
        Perform additional validation beyond JSON schema.
        
        Parameters:
            parameters (dict): The operation parameters
            
        Returns:
            list: List of error message strings (empty if no errors)
        """
        errors = []
        # Add custom validation logic here
        return errors
```

### PARAMS dictionary specification

The `PARAMS` dictionary uses [JSON Schema](https://json-schema.org/) (draft-2020-12) to specify operation parameters.

**Basic structure:**

```python
PARAMS = {
    "type": "object",  # Always "object" at top level
    "properties": {
        # Define each parameter here
    },
    "required": [
        # List required parameter names
    ],
    "additionalProperties": False  # Recommended: disallow unexpected parameters
}
```

**Parameter types:**

String parameter:

```python
"column_name": {
    "type": "string",
    "description": "The name of the column to process"
}
```

Integer/number parameter:

```python
"max_count": {
    "type": "integer",
    "minimum": 1,
    "description": "Maximum number of items"
}
```

Boolean parameter:

```python
"ignore_missing": {
    "type": "boolean",
    "description": "If true, ignore missing columns"
}
```

Array (list) parameter:

```python
"column_names": {
    "type": "array",
    "items": {
        "type": "string"
    },
    "minItems": 1,
    "description": "List of column names"
}
```

Object (dictionary) parameter:

```python
"column_mapping": {
    "type": "object",
    "patternProperties": {
        ".*": {
            "type": "string"
        }
    },
    "minProperties": 1,
    "description": "Mapping of old names to new names"
}
```

**Example: rename_columns PARAMS**

```python
PARAMS = {
    "type": "object",
    "properties": {
        "column_mapping": {
            "type": "object",
            "patternProperties": {
                ".*": {
                    "type": "string"
                }
            },
            "minProperties": 1,
            "description": "Dictionary mapping old column names to new names"
        },
        "ignore_missing": {
            "type": "boolean",
            "description": "If false, raise error for missing columns"
        }
    },
    "required": [
        "column_mapping",
        "ignore_missing"
    ],
    "additionalProperties": False
}
```

**Parameter dependencies:**

Use `dependentRequired` for conditional requirements:

```python
"dependentRequired": {
    "factor_names": ["factor_values"]  # factor_names requires factor_values
}
```

### Implementing BaseOp

**Constructor requirements:**

Always call the superclass constructor first:

```python
def __init__(self, parameters):
    super().__init__(parameters)
    # Then initialize operation-specific attributes
    self.column_names = parameters['column_names']
```

**The do_op method:**

Signature:

```python
def do_op(self, dispatcher, df, name, sidecar=None):
```

Parameters:

- `dispatcher`: Instance of `Dispatcher` managing the remodeling process
- `df`: Pandas DataFrame representing the tabular file
- `name`: Identifier for the file (usually filename or relative path)
- `sidecar`: Optional JSON sidecar containing HED annotations (for HED operations)

Returns:

- Modified DataFrame (for transformations)
- Original DataFrame (for summaries - they modify dispatcher.summary_dict instead)

Important Notes:

1. **n/a Handling**: The `do_op` method assumes that `n/a` values have been replaced with `numpy.NaN` in the incoming DataFrame. The `Dispatcher` handles this conversion automatically using `prep_data()` before operations and `post_proc_data()` after.

2. **Don't Modify in Place**: Return a new DataFrame rather than modifying the input DataFrame in place.

3. **Error Handling**: Raise appropriate exceptions with clear messages for error conditions.

Example implementation:

```python
def do_op(self, dispatcher, df, name, sidecar=None):
    """Remove specified columns from the DataFrame."""
    return df.drop(self.column_names, axis=1, errors=self.error_handling)
```

**The validate_input_data method:**

Use this static method for validation that cannot be expressed in JSON schema.

```python
@staticmethod
def validate_input_data(parameters):
    """
    Validate parameters beyond JSON schema constraints.
    
    Common use cases:
    - Checking list lengths match
    - Validating value ranges based on other parameters
    - Checking for logical inconsistencies
    
    Returns:
        list: User-friendly error messages (empty if valid)
    """
    errors = []
    
    # Example: Check that two lists have the same length
    if parameters.get("query_names"):
        if len(parameters["query_names"]) != len(parameters["queries"]):
            errors.append(
                "The query_names list must have the same length as queries list."
            )
    
    return errors
```

### Implementing summarization operations

Summarization operations require both an operation class (extending `BaseOp`) and a summary class (extending `BaseSummary`).

**Summarization operation class:**

```python
from remodeler.operations.base_summary import BaseSummary

class MySummarySummary(BaseSummary):
    """Holds summary information for my_summary operation."""
    
    def __init__(self, sum_op):
        """Initialize with operation parameters."""
        super().__init__(sum_op)
        self.summary_data = {}  # Store your summary data
    
    def update_summary(self, summary_dict):
        """
        Update summary with information from one file.
        
        Parameters:
            summary_dict (dict): File-specific information
                Example: {"name": "file.tsv", "column_names": [...]}
        """
        # Extract and store information
        name = summary_dict['name']
        # ... accumulate your summary data
    
    def get_summary_details(self, verbose=True):
        """
        Return the summary information as a dictionary.
        
        Parameters:
            verbose (bool): If True, include detailed information
            
        Returns:
            dict: Summary data formatted for output
        """
        return {
            'summary_type': 'my_summary',
            'data': self.summary_data
            # ... your summary structure
        }

class MySummaryOp(BaseOp):
    """Summarize some aspect of the data."""
    
    NAME = "my_summary"
    
    PARAMS = {
        "type": "object",
        "properties": {
            "summary_name": {
                "type": "string",
                "description": "Unique identifier for this summary"
            },
            "summary_filename": {
                "type": "string",
                "description": "Base filename for saving summary"
            }
        },
        "required": ["summary_name", "summary_filename"],
        "additionalProperties": False
    }
    
    def __init__(self, parameters):
        super().__init__(parameters)
        self.summary_name = parameters['summary_name']
        self.summary_filename = parameters['summary_filename']
    
    def do_op(self, dispatcher, df, name, sidecar=None):
        """Update summary without modifying DataFrame."""
        # Get or create summary object
        summary = dispatcher.summary_dict.get(self.summary_name)
        if not summary:
            summary = MySummarySummary(self)
            dispatcher.summary_dict[self.summary_name] = summary
        
        # Update with file-specific information
        summary.update_summary({
            "name": name,
            "data": self._extract_data(df)
        })
        
        # Return original DataFrame unchanged
        return df
    
    def _extract_data(self, df):
        """Helper method to extract relevant data."""
        extracted_data = {}
        # TODO: Your data extraction logic goes here
        return extracted_data
    
    @staticmethod
    def validate_input_data(parameters):
        return []  # No additional validation needed
```

**BaseSummary required methods:**

`update_summary(summary_dict)` - Called by the operation's `do_op` method for each file processed. Accumulates information across all files.

```python
def update_summary(self, summary_dict):
    file_name = summary_dict['name']
    file_data = summary_dict['data']
    
    # Store file-specific information
    self.file_summaries[file_name] = file_data
    
    # Update overall statistics
    self.total_files += 1
    # ... accumulate other data
```

`get_summary_details(verbose=True)` - Returns the accumulated summary data as a dictionary. This is called when saving summaries to JSON or text format.

```python
def get_summary_details(self, verbose=True):
    details = {
        'overall': {
            'total_files': self.total_files,
            # ... overall statistics
        }
    }
    
    if verbose:
        details['individual_files'] = self.file_summaries
    
    return details
```

### Validator integration

**Registering your operation:**

Add your operation to `remodeler/operations/valid_operations.py`:

```python
from remodeler.operations.my_custom_op import MyCustomOp

valid_operations = {
    # ... existing operations ...
    "my_custom_operation": MyCustomOp,
}
```

**Validation stages:**

The validator processes operations in stages:

1. **Stage 0**: Top-level structure (must be array of operations)
2. **Stage 1**: Operation dictionary format (must have operation, description, parameters keys)
3. **Stage 2**: Operation dictionary values (validate types and check valid operation names)
4. **Later Stages**: Nested parameter validation using JSON schema
5. **Final Stage**: Call `validate_input_data()` for each operation

**Error messages:**

The validator provides user-friendly error messages indicating:

- Operation index in the remodeling file
- Operation name
- Path to the invalid value
- What constraint was violated

### Testing custom operations

**Unit testing structure:**

Create test files in `tests/operations/` following the pattern:

```python
import unittest
import pandas as pd
from remodeler.operations.my_custom_op import MyCustomOp
from remodeler import Dispatcher

class TestMyCustomOp(unittest.TestCase):
    """Test cases for MyCustomOp."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_df = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': ['a', 'b', 'c']
        })
    
    def test_basic_functionality(self):
        """Test basic operation behavior."""
        params = {
            'my_parameter': 'value'
        }
        op = MyCustomOp(params)
        
        # Create a simple dispatcher for testing
        dispatcher = Dispatcher([], data_root=".")
        
        result = op.do_op(dispatcher, self.sample_df, "test_file.tsv")
        
        # Assert expected transformations
        self.assertIsInstance(result, pd.DataFrame)
        # ... more assertions
    
    def test_parameter_validation(self):
        """Test parameter validation."""
        # Test invalid parameters
        errors = MyCustomOp.validate_input_data({
            'my_parameter': 'value',
            'invalid_list': [1, 2]  # Wrong length
        })
        self.assertTrue(len(errors) > 0)
        
        # Test valid parameters
        errors = MyCustomOp.validate_input_data({
            'my_parameter': 'value',
            'valid_list': [1, 2, 3]
        })
        self.assertEqual(len(errors), 0)
    
    def test_error_handling(self):
        """Test error conditions."""
        params = {'my_parameter': 'value'}
        op = MyCustomOp(params)
        dispatcher = Dispatcher([], data_root=".")
        
        # Test with problematic data
        bad_df = pd.DataFrame({'wrong_col': [1, 2, 3]})
        
        with self.assertRaises(KeyError):
            op.do_op(dispatcher, bad_df, "test.tsv")

if __name__ == '__main__':
    unittest.main()
```

**Integration testing:**

Test with complete remodeling workflows:

```python
def test_full_remodeling_workflow(self):
    """Test operation in a complete remodeling pipeline."""
    operations = [
        {
            "operation": "my_custom_operation",
            "description": "Test my operation",
            "parameters": {
                "my_parameter": "test_value"
            }
        }
    ]
    
    dispatcher = Dispatcher(operations, data_root="path/to/test/data")
    dispatcher.run_operations()
    
    # Assert expected results
```

### Developer best practices

**Design principles:**

1. **Single Responsibility**: Each operation should do one thing well
2. **Immutability**: Don't modify input DataFrames in place
3. **Clear Errors**: Provide helpful error messages with context
4. **Documentation**: Include docstrings for class and methods
5. **Type Hints**: Use type hints for better IDE support

**Parameter design:**

1. **Required vs Optional**: Make commonly-used parameters required
2. **Sensible Defaults**: Provide defaults for optional parameters
3. **Clear Names**: Use descriptive parameter names
4. **Consistent**: Follow naming conventions from existing operations

**Error handling:**

```python
def do_op(self, dispatcher, df, name, sidecar=None):
    # Check preconditions
    if self.column_name not in df.columns:
        raise ValueError(
            f"Column '{self.column_name}' not found in {name}. "
            f"Available columns: {list(df.columns)}"
        )
    
    # Perform operation with try/except for specific errors
    try:
        result = df.copy()
        # ... transformation logic
        return result
    except Exception as e:
        raise RuntimeError(
            f"Error processing {name} with {self.NAME}: {str(e)}"
        )
```

**Performance considerations:**

1. **Vectorize Operations**: Use pandas vectorized operations instead of loops
2. **Avoid Copies**: Only copy DataFrames when necessary
3. **Lazy Evaluation**: Compute expensive operations only when needed
4. **Memory Efficiency**: For large datasets, consider memory usage

**Documentation:**

Include comprehensive docstrings:

```python
class MyCustomOp(BaseOp):
    """
    Transform data by applying custom logic.
    
    This operation processes tabular data by...
    
    Common use cases:
    - Use case 1
    - Use case 2
    
    Example JSON:
        {
            "operation": "my_custom_operation",
            "description": "Process the data",
            "parameters": {
                "my_parameter": "value"
            }
        }
    
    See Also:
        - related_operation: For alternative approach
        - another_operation: For complementary functionality
    """
```

**Testing checklist:**

- [ ] Unit tests for basic functionality
- [ ] Tests for edge cases
- [ ] Tests for error conditions
- [ ] Parameter validation tests
- [ ] Integration tests with Dispatcher
- [ ] Tests with various DataFrame structures
- [ ] Tests with n/a values
- [ ] Performance tests for large datasets (if applicable)

### Example: complete custom operation

Here's a complete example of a custom operation that converts column values to uppercase:

```python
from remodeler.operations.base_op import BaseOp
import pandas as pd

class UppercaseColumnsOp(BaseOp):
    """
    Convert specified columns to uppercase.
    
    Example JSON:
        {
            "operation": "uppercase_columns",
            "description": "Convert trial_type to uppercase",
            "parameters": {
                "column_names": ["trial_type", "condition"],
                "ignore_missing": true
            }
        }
    """
    
    NAME = "uppercase_columns"
    
    PARAMS = {
        "type": "object",
        "properties": {
            "column_names": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 1,
                "description": "List of column names to convert to uppercase"
            },
            "ignore_missing": {
                "type": "boolean",
                "description": "If true, ignore columns not in DataFrame"
            }
        },
        "required": ["column_names", "ignore_missing"],
        "additionalProperties": False
    }
    
    def __init__(self, parameters):
        super().__init__(parameters)
        self.column_names = parameters['column_names']
        self.ignore_missing = parameters['ignore_missing']
    
    def do_op(self, dispatcher, df, name, sidecar=None):
        """Convert specified columns to uppercase."""
        result = df.copy()
        
        for col in self.column_names:
            if col not in result.columns:
                if not self.ignore_missing:
                    raise KeyError(
                        f"Column '{col}' not found in {name}. "
                        f"Available: {list(result.columns)}"
                    )
                continue
            
            # Convert to uppercase, preserving NaN values
            result[col] = result[col].str.upper()
        
        return result
    
    @staticmethod
    def validate_input_data(parameters):
        """No additional validation needed beyond JSON schema."""
        return []
```

Register it:

```python
# In remodeler/operations/valid_operations.py
from remodeler.operations.uppercase_columns_op import UppercaseColumnsOp

valid_operations = {
    # ... existing operations ...
    "uppercase_columns": UppercaseColumnsOp,
}
```

### Resources for operation development

- **JSON Schema Documentation**: https://json-schema.org/
- **Pandas DataFrame API**: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
- **Python unittest**: https://docs.python.org/3/library/unittest.html
- **Table Remodeler Repository**: https://github.com/hed-standard/table-remodeler
- **Operations Reference**: [operations/index.rst](operations/index.rst)

**Getting help with custom operations:**

- Review existing operations in `remodeler/operations/` for examples
- Check the test suite in `tests/operations/` for testing patterns
- Open an issue on GitHub for questions or feature requests

## Best practices

1. **Always create backups** before applying operations to important datasets
2. **Test operations locally first** before applying to large datasets
3. **Use JSON operation files** for reproducibility and documentation
4. **Validate results** after applying operations (e.g., check row/column counts)
5. **Keep operation definitions simple** - chain multiple simple ops rather than creating complex ones
6. **Document your custom operations** with clear parameter descriptions
7. **Use meaningful backup names** with timestamps for easy identification

## Error handling

Table-remodeler validates operations at multiple stages to catch errors early and provide clear error messages.

### Validation stages

**Stage 1: JSON syntax validation**

The remodeling file must be valid JSON. Common JSON syntax errors:

- Missing commas between dictionary items
- Mismatched brackets/braces
- Unquoted keys or values (where quotes are required)
- Trailing commas (not allowed in standard JSON)

Use a JSON validator or IDE with JSON support to catch these early.

**Stage 2: JSON schema validation**

Each operation defines its required parameters using JSON Schema. The `RemodelerValidator` validates the entire remodeling file against compiled schemas before execution.

Example error:

```
Error in operation 'rename_columns' at index 0:
  Missing required parameter: 'column_mapping'
```

**Stage 3: Data validation**

Each operation's `validate_input_data()` method performs additional checks beyond JSON schema:

- Column names exist in the data
- Value mappings are valid
- Query syntax is correct
- File references are accessible

**Stage 4: Execution-time validation**

Errors during actual operation execution:

- File I/O errors (permissions, disk space)
- Type conversion errors
- HED validation errors (reported, not raised)

**Stage 5: Output validation**

Post-execution checks:

- Files can be written
- Summaries can be saved
- Results are internally consistent

### Error types and handling

**Remodeling file errors**

If the JSON remodeling file has errors, validation fails before any data processing:

```bash
run_remodel /data operations_rmdl.json
# Output:
# ERROR: Invalid remodeling file
# Operation 'rename_columns' at index 2: Missing required parameter 'column_mapping'
# Operation 'remove_columns' at index 5: Invalid type for 'column_names' (expected array)
# Remodeling aborted - fix errors and retry
```

All errors are reported at once, allowing you to fix multiple issues in one pass.

**Execution-time errors**

If an error occurs during execution, an exception is raised and processing stops:

```python
try:
    dispatcher.run_operations()
except Exception as e:
    print(f"Remodeling failed: {e}")
    # Check log file for details
```

Common execution errors:

- `FileNotFoundError`: Data file or sidecar not found
- `PermissionError`: Can't write output files
- `KeyError`: Column doesn't exist in data
- `ValueError`: Invalid data type conversion

**HED validation errors (special case)**

The `summarize_hed_validation` operation reports HED errors in the summary file rather than raising exceptions. This allows you to see all validation issues across all files:

```python
operations = [{
    "operation": "summarize_hed_validation",
    "parameters": {"summary_name": "validation_check"}
}]

dispatcher.run_operations()
# No exception raised even if HED errors exist
# Check summary file for validation results
```

### Using the online tools for debugging

Before running remodeling on an entire dataset, use the [HED online tools](https://hedtools.org/hed/) to debug your operations:

1. Navigate to **Events** → **Execute remodel script**
2. Upload a single data file and your JSON remodeling file
3. Click **Process**
4. If errors exist, download the error report
5. Fix errors and repeat until successful
6. Run on full dataset

The online tools provide immediate feedback without modifying your dataset.

### Troubleshooting

**Common issues:**

#### "File not found" errors

- Use absolute paths, not relative paths
- Check file extensions match (`.tsv` vs `.csv`)
- Verify case-sensitive filenames on Linux/Mac
- Ensure `-x` exclusions aren't hiding your files

#### "Column not found" errors

- Column names are case-sensitive
- Check operation order - earlier ops may have removed the column
- Verify column names in original file (not just backup)
- Try `summarize_column_names` to see actual column names

#### "HED schema not found"

- Ensure internet connection for automatic download
- Schemas cached in `~/.hedtools/` directory (managed by `hedtools` package)
- Specify version explicitly: `-hv 8.3.0`
- Check version exists: [HED Schema Viewer](https://www.hedtags.org/display_hed.html)
- Clear cache if corrupted: delete `~/.hedtools/` and rerun

#### "Operations run but files don't change"

- Check for `--no-update` or `-nu` flag
- Verify write permissions on data directory
- Confirm you're not only running summarization operations
- Check if backup system is engaged (look for backup directory)

#### "JSON parsing error"

- Validate JSON syntax with online validator
- Check for trailing commas
- Ensure all strings are quoted
- Verify bracket/brace matching

#### "Import errors" or "Module not found"

- Ensure table-remodeler is installed: `pip install table-remodeler`
- For development, install in editable mode: `pip install -e .`
- Check Python version: requires 3.10+
- Verify virtual environment is activated

### Log files

When exceptions occur, log files are written to help debugging:

**Default log location:** `[data_root]/derivatives/remodel/logs/`

**Custom log location:**

```bash
run_remodel /data operations_rmdl.json -ld /custom/log/directory
```

Log files include:

- Full stack trace
- Operation that failed
- File being processed
- Parameter values
- System information

**Note:** Log files are NOT written for normal HED validation errors since those are reported in summary files.

### Getting help

**Documentation:**

- [Quickstart guide](./quickstart.md) for tutorials
- [Operations reference](./operations/index.rst) for operation details
- [Creating custom operations](#creating-custom-operations) for extending Table Remodeler
- [API Reference](api/index.rst) for Python API details

**Support:**

- [table-remodeler Issues](https://github.com/hed-standard/table-remodeler/issues) for bugs and feature requests
- [hed-python Issues](https://github.com/hed-standard/hed-python/issues) for HED validation issues
- [HED Forum](https://github.com/hed-standard/hed-specification/discussions) for HED questions and discussions
- [HED Discussions](https://github.com/orgs/hed-standard/discussions) for general community discussions and ideas
- [hed-examples repository](https://github.com/hed-standard/hed-examples) for working examples and tutorials

**Contact:**

- Email: [hed.maintainers@gmail.com](mailto:hed.maintainers@gmail.com)
