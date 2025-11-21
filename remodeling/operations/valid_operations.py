"""The valid operations for the remodeling tools."""

from remodeling.operations.factor_column_op import FactorColumnOp
from remodeling.operations.factor_hed_tags_op import FactorHedTagsOp
from remodeling.operations.factor_hed_type_op import FactorHedTypeOp
from remodeling.operations.merge_consecutive_op import MergeConsecutiveOp
from remodeling.operations.number_rows_op import NumberRowsOp
from remodeling.operations.number_groups_op import NumberGroupsOp
from remodeling.operations.remove_columns_op import RemoveColumnsOp
from remodeling.operations.reorder_columns_op import ReorderColumnsOp
from remodeling.operations.remap_columns_op import RemapColumnsOp
from remodeling.operations.remove_rows_op import RemoveRowsOp
from remodeling.operations.rename_columns_op import RenameColumnsOp
from remodeling.operations.split_rows_op import SplitRowsOp
from remodeling.operations.summarize_column_names_op import SummarizeColumnNamesOp
from remodeling.operations.summarize_column_values_op import SummarizeColumnValuesOp
from remodeling.operations.summarize_definitions_op import SummarizeDefinitionsOp
from remodeling.operations.summarize_sidecar_from_events_op import SummarizeSidecarFromEventsOp
from remodeling.operations.summarize_hed_type_op import SummarizeHedTypeOp
from remodeling.operations.summarize_hed_tags_op import SummarizeHedTagsOp
from remodeling.operations.summarize_hed_validation_op import SummarizeHedValidationOp

valid_operations = {
    # 'convert_columns': ConvertColumnsOp,
    "factor_column": FactorColumnOp,
    "factor_hed_tags": FactorHedTagsOp,
    "factor_hed_type": FactorHedTypeOp,
    "merge_consecutive": MergeConsecutiveOp,
    "number_groups": NumberGroupsOp,
    "number_rows": NumberRowsOp,
    "remap_columns": RemapColumnsOp,
    "remove_columns": RemoveColumnsOp,
    "remove_rows": RemoveRowsOp,
    "rename_columns": RenameColumnsOp,
    "reorder_columns": ReorderColumnsOp,
    "split_rows": SplitRowsOp,
    "summarize_column_names": SummarizeColumnNamesOp,
    "summarize_column_values": SummarizeColumnValuesOp,
    "summarize_definitions": SummarizeDefinitionsOp,
    "summarize_hed_tags": SummarizeHedTagsOp,
    "summarize_hed_type": SummarizeHedTypeOp,
    "summarize_hed_validation": SummarizeHedValidationOp,
    "summarize_sidecar_from_events": SummarizeSidecarFromEventsOp,
}
