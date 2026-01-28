# Table remodeler overview

## What is table remodeler?

Table Remodeler is a Python package that provides flexible tools for transforming and reorganizing tabular data files. It's particularly useful for processing event files in neuroimaging research and supports HED (Hierarchical Event Descriptors) annotations.

## Key remodeler features

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

For development with all extras:

```bash
git clone https://github.com/hed-standard/table-remodeler.git
cd table-remodeler
pip install -e ".[dev,test,docs,examples]"
```

Or install specific optional dependencies:

- **Development tools**: `pip install -e ".[dev]"`
- **Testing tools**: `pip install -e ".[test]"`
- **Documentation**: `pip install -e ".[docs]"`
- **Jupyter examples**: `pip install -e ".[examples]"`

## Example usage

### Command line

```bash
# Run remodeling operations
run_remodel /path/to/dataset operations.json

# Create a backup
run_remodel_backup /path/to/dataset

# Restore from backup
run_remodel_restore /path/to/dataset
```

!!! warning "Backup requirement" Running `run_remodel` will raise an error unless a backup exists. To run operations without creating a backup, use the `--no-backup` flag: `bash     run_remodel /path/to/dataset operations.json --no-backup     `

### Python api

```python
from remodeler import Dispatcher

operations = [
    {"operation": "remove_columns", "parameters": {"column_names": ["unwanted_col"]}},
    {"operation": "rename_columns", "parameters": {"column_mapping": {"old": "new"}}}
]

dispatcher = Dispatcher(operations, data_root="/path/to/dataset")
dispatcher.run_operations()
```

## Finding help

- 📖 [User guide](user_guide.md) - Tutorials and examples
- 📚 [API reference](api/index.rst) - API documentation
- 🔗 [Issues](https://github.com/hed-standard/table-remodeler/issues) - Github issues
- � [Discussions and ideas](https://github.com/orgs/hed-standard/discussions) - Community discussions
- 📧 [Contact](mailto:hed.maintainers@gmail.com) - hed.maintainers@gmail.com

## Related projects

- [hed-python](https://github.com/hed-standard/hed-python): Core HED tools and validation (provides `hedtools` dependency)
- [hed-schemas](https://github.com/hed-standard/hed-schemas): HED schema vocabularies
- [hed-specification](https://github.com/hed-standard/hed-specification): Formal HED specification
- [hed-examples](https://github.com/hed-standard/hed-examples): Example datasets and notebooks

### Issues and problems

If you encounter problems using table-remodeler, please [open an issue](https://github.com/hed-standard/table-remodeler/issues) in the table-remodeler repository on GitHub.

For HED-specific issues (annotation syntax, schema questions, validation), see the [hed-python issues](https://github.com/hed-standard/hed-python/issues) or [HED specification discussions](https://github.com/hed-standard/hed-specification/discussions).
