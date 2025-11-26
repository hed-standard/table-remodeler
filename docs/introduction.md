# Introduction

## What is table remodeler?

Table Remodeler is a Python package that provides flexible tools for transforming and reorganizing tabular data files. It's particularly useful for processing event files in neuroimaging research and supports HED (Hierarchical Event Descriptors) annotations.

## Key features

- **Operation-based architecture**: Apply transformations through a series of composable operations
- **JSON configuration**: Define remodeling pipelines in JSON for reproducible workflows
- **HED support**: Built-in operations for working with HED-annotated event files
- **Backup & restore**: Automatic backup management before applying changes
- **Command-line interface**: Easy-to-use CLI tools for batch processing
- **Extensible**: Create custom operations by extending the `BaseOp` class

## Installing table remodeler

You can install table-remodeler from PyPI:

```bash
pip install table-remodeler
```

Or install directly from the [GitHub repository](https://github.com/hed-standard/table-remodeler):

```bash
pip install git+https://github.com/hed-standard/table-remodeler.git
```

For development installation with testing tools:

```bash
git clone https://github.com/hed-standard/table-remodeler.git
cd table-remodeler
pip install -e ".[dev,test]"
```

## Quick start

### Command line

```bash
# Run remodeling operations
run_remodel /path/to/dataset operations.json

# Create a backup
run_remodel_backup /path/to/dataset

# Restore from backup
run_remodel_restore /path/to/dataset
```

### Python api

```python
from remodel import Dispatcher

operations = [
    {"operation": "remove_columns", "parameters": {"column_names": ["unwanted_col"]}},
    {"operation": "rename_columns", "parameters": {"column_mapping": {"old": "new"}}}
]

dispatcher = Dispatcher(operations, data_root="/path/to/dataset")
dispatcher.run_operations()
```

## Finding help

- 📖 [User Guide](user_guide.md) - Tutorials and examples
- 📚 [API Reference](api/index.rst) - API documentation
- 🔗 [GitHub Repository](https://github.com/hed-standard/table-remodeler) - Source code and issues
- 🔗 [Related Projects](#related-projects) - HED and related tools

## Related projects

- **[hed-python](https://github.com/hed-standard/hed-python)**: Core HED tools and validation (provides `hedtools` dependency)
- **[hed-schemas](https://github.com/hed-standard/hed-schemas)**: HED schema vocabularies
- **[hed-specification](https://github.com/hed-standard/hed-specification)**: Formal HED specification
- **[hed-examples](https://github.com/hed-standard/hed-examples)**: Example datasets and notebooks


### Issues and problems

If you encounter problems using table-remodeler, please [open an issue](https://github.com/hed-standard/table-remodeler/issues) in the table-remodeler repository on GitHub.

For HED-specific issues (annotation syntax, schema questions, validation), see the [hed-python issues](https://github.com/hed-standard/hed-python/issues) or [HED specification discussions](https://github.com/hed-standard/hed-specification/discussions).
