# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2025-12-12

### Initial Release

First public release of table-remodeler as a standalone package, extracted from hed-python.

#### Goals

- Separate remodeling tools from HedTools package for better modularity
- Focus on general tabular file manipulation, not just HED-specific operations
- Make it easier to develop and contribute additional operations

#### Features

- **Core Framework**:

  - Operation-based architecture with JSON-configurable pipelines
  - `Dispatcher` for orchestrating operations
  - `BackupManager` for dataset backup and restore
  - `RemodelerValidator` for operation validation

- **Data Transformation Operations** (8 operations):

  - `factor_column` - Create factor columns from value mappings
  - `merge_consecutive` - Merge consecutive rows
  - `remap_columns` - Remap column values
  - `remove_columns` - Remove specified columns
  - `remove_rows` - Remove rows by criteria
  - `rename_columns` - Rename columns
  - `reorder_columns` - Reorder columns
  - `split_rows` - Split rows by criteria

- **HED-Specific Operations** (7 operations):

  - `factor_hed_tags` - Factor HED tags into columns
  - `factor_hed_type` - Factor by HED tag types
  - `summarize_definitions` - Extract HED definitions
  - `summarize_hed_tags` - Summarize HED tag usage
  - `summarize_hed_type` - Summarize HED types
  - `summarize_hed_validation` - Validate HED annotations
  - `summarize_sidecar_from_events` - Generate sidecar from events

- **Analysis Operations** (2 operations):

  - `summarize_column_names` - List column names
  - `summarize_column_values` - Summarize unique values

- **Command-Line Tools**:

  - `run_remodel` - Execute remodeling operations
  - `run_remodel_backup` - Create dataset backups
  - `run_remodel_restore` - Restore from backups

- **Documentation**:

  - Comprehensive Sphinx documentation
  - API reference for all operations
  - Quickstart guide and user guide
  - Custom operations development guide

- **Testing**:

  - Comprehensive unit test suite
  - Test coverage tracking

#### Dependencies

- Python 3.10+
- hedtools >= 0.8.1
- pandas >= 2.2.3
- numpy >= 2.0.2
- jsonschema >= 4.23.0
- openpyxl >= 3.1.5
- semantic-version >= 2.10.0
