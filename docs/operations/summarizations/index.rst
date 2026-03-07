Summarizations
===============

Summarization operations extract information and generate reports from tabular data files without modifying the original data. These operations are essential for quality assurance, understanding dataset structure, and validating annotations.

What are summarizations?
--------------------------

Summarizations analyze data files and accumulate results across the dataset. They can:

- **Validate data**: Check for errors, inconsistencies, or missing information
- **Profile datasets**: Understand column structure, value distributions, and patterns
- **Generate reports**: Create text and JSON summaries for documentation
- **Extract metadata**: Pull out definitions, conditions, and design information

Key characteristics:

- Do not modify the input data files
- Accumulate information across multiple files (stateful)
- Generate both text and JSON format outputs
- Can be used multiple times in a pipeline as checkpoints

Common summarization workflows
--------------------------------

**Quality assurance pipeline:**

1. :doc:`summarize_column_names` - Verify consistent column structure
2. :doc:`summarize_column_values` - Check for unexpected values
3. :doc:`summarize_hed_validation` - Validate HED annotations

**Dataset understanding:**

1. :doc:`summarize_column_names` - Identify column patterns
2. :doc:`summarize_column_values` - Understand value distributions
3. :doc:`summarize_hed_type` - Extract experimental design

**HED annotation analysis:**

1. :doc:`summarize_hed_validation` - Check annotation validity
2. :doc:`summarize_definitions` - Review HED definitions
3. :doc:`summarize_hed_tags` - Analyze tag usage patterns

Available summarizations
--------------------------

.. toctree::
   :maxdepth: 1

   summarize_column_names
   summarize_column_values
   summarize_definitions
   summarize_hed_tags
   summarize_hed_type
   summarize_hed_validation
   summarize_sidecar_from_events

Summarization summary
----------------------

Column analysis
^^^^^^^^^^^^^^^

- :doc:`summarize_column_names` - List unique column name patterns across files
- :doc:`summarize_column_values` - Count unique values and distributions per column
- :doc:`summarize_sidecar_from_events` - Generate sidecar template from event files

HED operations
^^^^^^^^^^^^^^

- :doc:`summarize_hed_validation` - Validate HED annotations and report errors
- :doc:`summarize_hed_tags` - Summarize HED tag usage across dataset
- :doc:`summarize_hed_type` - Extract experimental design from HED type tags
- :doc:`summarize_definitions` - Analyze HED definitions for consistency

Common parameters
------------------

All summarization operations require two standard parameters:

**summary_name** (str)
   A unique identifier for this summary instance. Use descriptive names that indicate what is being summarized.

**summary_filename** (str)
   Base filename for saving the summary. Timestamp and extension (.txt or .json) are added automatically.

**append_timecode** (bool, optional, default: False)
   If true, append a timestamp to the filename to prevent overwriting previous summaries.

Output formats
--------------

Summaries are saved in two formats:

**Text format (.txt)**
   Human-readable format with:
   
   - Overall dataset summary
   - Individual file details (when requested)
   - Formatted tables and lists
   - Good for documentation and manual review

**JSON format (.json)**
   Machine-readable format with:
   
   - Structured data for programmatic access
   - All summary information preserved
   - Suitable for automated processing
   - Can be loaded into analysis tools

Output location
---------------

When processing full datasets (not individual files), summaries are automatically saved to:

.. code-block:: text

   <dataset_root>/derivatives/remodel/summaries/

The directory structure is created automatically if it doesn't exist.

HED operations note
-------------------

Operations with "HED" in their name require:

- A HED schema version specified when creating the Dispatcher
- Often a JSON sidecar file containing HED annotations
- Data files with HED-annotated columns

See the :doc:`../../user_guide` for details on using HED operations.

Examples
--------

**Basic column profiling:**

.. code-block:: json

   [
       {
           "operation": "summarize_column_names",
           "description": "Check column consistency across files",
           "parameters": {
               "summary_name": "column_name_check",
               "summary_filename": "column_names"
           }
       },
       {
           "operation": "summarize_column_values",
           "description": "Profile column value distributions",
           "parameters": {
               "summary_name": "column_value_profile",
               "summary_filename": "column_values",
               "skip_columns": ["onset", "duration"],
               "value_columns": ["response_time"]
           }
       }
   ]

**HED validation:**

.. code-block:: json

   [
       {
           "operation": "summarize_hed_validation",
           "description": "Validate HED annotations",
           "parameters": {
               "summary_name": "hed_validation_check",
               "summary_filename": "hed_validation",
               "check_for_warnings": true
           }
       }
   ]

See also
--------

- :doc:`../transformations/index` - Transformation operations
- :doc:`../../quickstart` - Getting started guide
- :doc:`../../user_guide` - Complete usage documentation
