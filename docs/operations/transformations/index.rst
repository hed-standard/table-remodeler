Transformations
================

Transformation operations modify tabular data files by restructuring, filtering, or augmenting their content. These operations are the primary tools for preparing event files for analysis, converting between encodings, and cleaning datasets.

What are transformations?
--------------------------

Transformations process data files sequentially, applying changes to each file independently. They can:

- **Restructure data**: Reorder, rename, or reorganize columns
- **Filter data**: Remove unwanted rows or columns
- **Augment data**: Add computed columns (e.g., factor vectors)
- **Convert formats**: Transform between different data representations
- **Merge/split**: Combine or separate events

Key characteristics:

- Modify the input data files directly
- Process files independently (stateless)
- Can be chained together in sequences
- Changes are saved to the output location

Common transformation workflows
--------------------------------

**Data cleaning pipeline:**

1. :doc:`remove_columns` - Remove unnecessary columns
2. :doc:`remove_rows` - Filter out unwanted events
3. :doc:`rename_columns` - Standardize column names
4. :doc:`reorder_columns` - Establish consistent column order

**Factor vector generation:**

1. :doc:`factor_column` - Create factors from categorical columns
2. :doc:`factor_hed_tags` - Create factors from HED tag queries
3. :doc:`factor_hed_type` - Create factors from HED type tags

**Event restructuring:**

1. :doc:`split_rows` - Convert trial-level to event-level encoding
2. :doc:`merge_consecutive` - Combine consecutive identical events
3. :doc:`remap_columns` - Map value combinations to new encodings

Available transformations
--------------------------

.. toctree::
   :maxdepth: 1

   factor_column
   factor_hed_tags
   factor_hed_type
   merge_consecutive
   remap_columns
   remove_columns
   remove_rows
   rename_columns
   reorder_columns
   split_rows

Transformation summary
----------------------

Basic column operations
^^^^^^^^^^^^^^^^^^^^^^^

- :doc:`remove_columns` - Remove specified columns from data files
- :doc:`rename_columns` - Rename columns using a mapping dictionary
- :doc:`reorder_columns` - Reorder columns in a specified sequence

Row operations
^^^^^^^^^^^^^^

- :doc:`remove_rows` - Remove rows based on column value criteria
- :doc:`merge_consecutive` - Merge consecutive rows with identical values
- :doc:`split_rows` - Split trial-level encoding into event-level

Value mapping
^^^^^^^^^^^^^

- :doc:`remap_columns` - Map combinations of source column values to destination columns

Factor generation
^^^^^^^^^^^^^^^^^

- :doc:`factor_column` - Create factor vectors from column values
- :doc:`factor_hed_tags` - Create factor vectors from HED tag search queries
- :doc:`factor_hed_type` - Create factor vectors from HED type tags (e.g., Condition-variable)

HED operations note
-------------------

Operations with "HED" in their name require:

- A HED schema version specified when creating the Dispatcher
- Often a JSON sidecar file containing HED annotations
- Data files with HED-annotated columns

See the :doc:`../../user_guide` for details on using HED operations.

Examples
--------

**Simple column cleanup:**

.. code-block:: json

   [
       {
           "operation": "remove_columns",
           "description": "Remove temporary processing columns",
           "parameters": {
               "column_names": ["temp_col", "debug_info"],
               "ignore_missing": true
           }
       },
       {
           "operation": "reorder_columns",
           "description": "Standardize column order",
           "parameters": {
               "column_order": ["onset", "duration", "trial_type"],
               "keep_others": true,
               "ignore_missing": false
           }
       }
   ]

**Factor vector generation:**

.. code-block:: json

   [
       {
           "operation": "factor_column",
           "description": "Create factors for trial types",
           "parameters": {
               "column_name": "trial_type",
               "factor_values": ["go", "stop"],
               "factor_names": ["is_go", "is_stop"]
           }
       }
   ]

See also
--------

- :doc:`../summarizations/index` - Summarization operations
- :doc:`../../quickstart` - Getting started guide
- :doc:`../../user_guide` - Complete usage documentation
