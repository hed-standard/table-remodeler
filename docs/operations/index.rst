Operations reference
====================

Table Remodeler provides two main categories of operations for working with tabular data files:

**Transformations** modify tabular data by restructuring, filtering, or augmenting the content. These operations change the data files and can be used to prepare datasets for analysis, convert between formats, or clean up event files.

**Summarizations** extract information and generate reports without modifying the original data. These operations are useful for quality assurance, understanding dataset structure, and generating analysis-ready summaries.

Common operation concepts
--------------------------

All operations are specified using JSON configuration files that define a list of operations to execute sequentially. Each operation has:

- **operation**: The operation name (e.g., "remove_columns", "summarize_hed_tags")
- **description**: A human-readable description of what this operation does
- **parameters**: Operation-specific parameters controlling behavior

Example operation structure:

.. code-block:: json

   [{
       "operation": "remove_columns",
       "description": "Remove unnecessary columns from the dataset",
       "parameters": {
           "column_names": ["column1", "column2"],
           "ignore_missing": true
       }
   }]

Transformations vs summarizations
-----------------------------------

+------------------+---------------------------------------+---------------------------------------+
| Aspect           | Transformations                       | Summarizations                        |
+==================+=======================================+=======================================+
| Data modification| Modify the input data files           | Do not modify data files              |
+------------------+---------------------------------------+---------------------------------------+
| Output           | Modified tabular files                | Summary reports (JSON/text)           |
+------------------+---------------------------------------+---------------------------------------+
| State            | Stateless (process one file at a time)| Stateful (accumulate across files)    |
+------------------+---------------------------------------+---------------------------------------+
| Common use       | Data cleaning, restructuring,         | Quality assurance, validation,        |
|                  | format conversion                     | dataset understanding                 |
+------------------+---------------------------------------+---------------------------------------+

Summary operation parameters
------------------------------

All summarization operations require two standard parameters:

- **summary_name**: A unique identifier for this summary instance
- **summary_filename**: Base filename for saving the summary (timestamp and extension added automatically)

Optional common parameter:

- **append_timecode**: (Default: false) If true, append timestamp to the filename

Operation categories
--------------------

.. toctree::
   :maxdepth: 2

   transformations/index
   summarizations/index

Quick links
-----------

**Most commonly used transformations:**

- :doc:`transformations/remove_columns` - Remove unnecessary columns
- :doc:`transformations/rename_columns` - Rename columns for clarity
- :doc:`transformations/remap_columns` - Map column value combinations to new columns
- :doc:`transformations/factor_column` - Create factor vectors from column values

**Most commonly used summarizations:**

- :doc:`summarizations/summarize_column_values` - Understand column value distributions
- :doc:`summarizations/summarize_hed_validation` - Validate HED annotations
- :doc:`summarizations/summarize_hed_type` - Extract experimental design information
- :doc:`summarizations/summarize_column_names` - Check column name consistency

See also
--------

- :doc:`../quickstart` - Get started with basic operations
- :doc:`../user_guide` - Comprehensive usage guide (including custom operations)
