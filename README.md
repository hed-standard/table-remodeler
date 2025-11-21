[![Maintainability](https://qlty.sh/gh/hed-standard/projects/hed-python/maintainability.svg)](https://qlty.sh/gh/hed-standard/projects/hed-python)
[![Code Coverage](https://qlty.sh/gh/hed-standard/projects/table-remodeler/coverage.svg)](https://qlty.sh/gh/hed-standard/projects/table-remodeler)
![Python3](https://img.shields.io/badge/python->=3.10-yellow.svg)
[![Documentation](https://img.shields.io/badge/docs-table-remodeler.svg)](https://www.hedtags.org/table-remodeler)

# The table-remodeler

Tabular file remodeling and reorganizing tools for event files and datasets.

## Overview

`table-remodeler` provides a flexible, operation-based framework for transforming tabular data files through JSON-configurable pipelines. Originally extracted from the [hed-python](https://github.com/hed-standard/hed-python) remodeling tools, this package operates as a standalone tool while maintaining compatibility with HED (Hierarchical Event Descriptors) annotations.

**Key Features:**
- Operation-based architecture for reproducible data transformations
- JSON-configurable pipelines for batch processing
- Support for HED-annotated event files
- Built-in backup and restore functionality
- Both programmatic API and command-line interface

## Installation

```bash
pip install table-remodeler
```

For development:
```bash
git clone https://github.com/hed-standard/table-remodeler.git
cd table-remodeler
pip install -e .
```

## Quick Start

### Python API

```python
from remodel import Dispatcher

# Define operations
operations = [
    {
        "operation": "remove_columns",
        "parameters": {"column_names": ["unnecessary_col"]}
    },
    {
        "operation": "rename_columns",
        "parameters": {"column_mapping": {"old_name": "new_name"}}
    }
]

# Execute operations
dispatcher = Dispatcher(operations, data_root="/path/to/dataset")
dispatcher.run_operations()
```

### Command Line

```bash
# Run remodeling operations
run_remodel /path/to/data /path/to/operations.json

# Create backup before modifications
run_remodel_backup /path/to/data --backup-name my_backup

# Restore from backup
run_remodel_restore /path/to/data --backup-name my_backup
```

## Available Operations

### Data Transformation
- `convert_columns` - Convert column data types
- `factor_column` - Create factor columns from value mappings
- `merge_consecutive` - Merge consecutive rows with same values
- `number_groups` - Assign group numbers to row sequences
- `number_rows` - Add sequential row numbers
- `remap_columns` - Remap column values using lookup tables
- `remove_columns` - Remove specified columns
- `remove_rows` - Remove rows based on criteria
- `rename_columns` - Rename columns
- `reorder_columns` - Reorder columns
- `split_rows` - Split rows based on criteria

### HED-Specific Operations
- `factor_hed_tags` - Factor HED tags into separate columns
- `factor_hed_type` - Factor by HED tag types
- `summarize_hed_tags` - Summarize HED tag usage
- `summarize_hed_type` - Summarize HED types
- `summarize_hed_validation` - Validate HED annotations
- `summarize_definitions` - Extract HED definitions
- `summarize_sidecar_from_events` - Generate sidecar from events

### Analysis Operations
- `summarize_column_names` - List column names across files
- `summarize_column_values` - Summarize unique values per column

## Documentation

Full documentation is available at [table-remodeler.readthedocs.io](https://table-remodeler.readthedocs.io/)

## Requirements

- Python 3.10+
- pandas
- numpy
- hedtools (for HED-specific operations)

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please see the development setup in the documentation.

## Related Projects

- [hed-python](https://github.com/hed-standard/hed-python) - Core HED tools
- [hed-schemas](https://github.com/hed-standard/hed-schemas) - HED schema vocabularies
- [hed-specification](https://github.com/hed-standard/hed-specification) - HED specification
