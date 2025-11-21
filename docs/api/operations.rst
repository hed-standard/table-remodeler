Operations
==========

Remodeling and analysis operations for transforming tabular data.

Base Classes
------------

All operations inherit from these base classes.

BaseOp
~~~~~~

.. autoclass:: remodel.operations.base_op.BaseOp
   :members:
   :undoc-members:
   :show-inheritance:

BaseSummary
~~~~~~~~~~~

.. autoclass:: remodel.operations.base_summary.BaseSummary
   :members:
   :undoc-members:
   :show-inheritance:

Data Transformation Operations
-------------------------------

Operations that modify or reorganize tabular data.

ConvertColumnsOp
~~~~~~~~~~~~~~~~

.. autoclass:: remodel.operations.convert_columns_op.ConvertColumnsOp
   :members:
   :undoc-members:
   :show-inheritance:

FactorColumnOp
~~~~~~~~~~~~~~

.. autoclass:: remodel.operations.factor_column_op.FactorColumnOp
   :members:
   :undoc-members:
   :show-inheritance:

MergeConsecutiveOp
~~~~~~~~~~~~~~~~~~

.. autoclass:: remodel.operations.merge_consecutive_op.MergeConsecutiveOp
   :members:
   :undoc-members:
   :show-inheritance:

NumberGroupsOp
~~~~~~~~~~~~~~

.. autoclass:: remodel.operations.number_groups_op.NumberGroupsOp
   :members:
   :undoc-members:
   :show-inheritance:

NumberRowsOp
~~~~~~~~~~~~

.. autoclass:: remodel.operations.number_rows_op.NumberRowsOp
   :members:
   :undoc-members:
   :show-inheritance:

RemapColumnsOp
~~~~~~~~~~~~~~

.. autoclass:: remodel.operations.remap_columns_op.RemapColumnsOp
   :members:
   :undoc-members:
   :show-inheritance:

RemoveColumnsOp
~~~~~~~~~~~~~~~

.. autoclass:: remodel.operations.remove_columns_op.RemoveColumnsOp
   :members:
   :undoc-members:
   :show-inheritance:

RemoveRowsOp
~~~~~~~~~~~~

.. autoclass:: remodel.operations.remove_rows_op.RemoveRowsOp
   :members:
   :undoc-members:
   :show-inheritance:

RenameColumnsOp
~~~~~~~~~~~~~~~

.. autoclass:: remodel.operations.rename_columns_op.RenameColumnsOp
   :members:
   :undoc-members:
   :show-inheritance:

ReorderColumnsOp
~~~~~~~~~~~~~~~~

.. autoclass:: remodel.operations.reorder_columns_op.ReorderColumnsOp
   :members:
   :undoc-members:
   :show-inheritance:

SplitRowsOp
~~~~~~~~~~~

.. autoclass:: remodel.operations.split_rows_op.SplitRowsOp
   :members:
   :undoc-members:
   :show-inheritance:

HED-Specific Operations
-----------------------

Operations for working with HED-annotated data.

FactorHedTagsOp
~~~~~~~~~~~~~~~

.. autoclass:: remodel.operations.factor_hed_tags_op.FactorHedTagsOp
   :members:
   :undoc-members:
   :show-inheritance:

FactorHedTypeOp
~~~~~~~~~~~~~~~

.. autoclass:: remodel.operations.factor_hed_type_op.FactorHedTypeOp
   :members:
   :undoc-members:
   :show-inheritance:

SummarizeDefinitionsOp
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: remodel.operations.summarize_definitions_op.SummarizeDefinitionsOp
   :members:
   :undoc-members:
   :show-inheritance:

SummarizeHedTagsOp
~~~~~~~~~~~~~~~~~~

.. autoclass:: remodel.operations.summarize_hed_tags_op.SummarizeHedTagsOp
   :members:
   :undoc-members:
   :show-inheritance:

SummarizeHedTypeOp
~~~~~~~~~~~~~~~~~~

.. autoclass:: remodel.operations.summarize_hed_type_op.SummarizeHedTypeOp
   :members:
   :undoc-members:
   :show-inheritance:

SummarizeHedValidationOp
~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: remodel.operations.summarize_hed_validation_op.SummarizeHedValidationOp
   :members:
   :undoc-members:
   :show-inheritance:

SummarizeSidecarFromEventsOp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: remodel.operations.summarize_sidecar_from_events_op.SummarizeSidecarFromEventsOp
   :members:
   :undoc-members:
   :show-inheritance:

Analysis Operations
-------------------

Operations for analyzing and summarizing tabular data.

SummarizeColumnNamesOp
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: remodel.operations.summarize_column_names_op.SummarizeColumnNamesOp
   :members:
   :undoc-members:
   :show-inheritance:

SummarizeColumnValuesOp
~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: remodel.operations.summarize_column_values_op.SummarizeColumnValuesOp
   :members:
   :undoc-members:
   :show-inheritance:

Operation Registry
------------------

The valid_operations module maintains a registry of all available operations.

.. autodata:: remodel.operations.valid_operations.valid_operations
   :annotation: = {operation_name: OperationClass}
