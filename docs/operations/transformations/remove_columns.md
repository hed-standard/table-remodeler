(remove-columns-anchor)=

# Remove columns

Sometimes columns are added during intermediate processing steps. The *remove_columns* operation is useful for cleaning up unnecessary columns after these processing steps complete.

## Purpose

Use this operation to:

- Remove temporary or intermediate processing columns
- Clean up data files before final output
- Remove columns not needed for analysis
- Simplify datasets by removing unused information

(remove-columns-parameters-anchor)=

## Parameters

```{admonition} Parameters for the *remove_columns* operation.
---
class: tip
---
|  Parameter   | Type | Description | 
| ------------ | ---- | ----------- | 
| *column_names* | list of str | A list of columns to remove.| 
| *ignore_missing* | boolean | If true, missing columns are ignored, otherwise raise `KeyError`. |
```

If one of the specified columns is not in the file and the *ignore_missing* parameter is *false*, a `KeyError` is raised for the missing column.

(remove-columns-example-anchor)=

## Example

The following example specifies that the *remove_columns* operation should remove the `stop_signal_delay`, `response_accuracy`, and `face` columns from the tabular data.

````{admonition} A JSON file with a single *remove_columns* transformation operation.
---
class: tip
---
```json
[{   
    "operation": "remove_columns",
    "description": "Remove extra columns before the next step.",
    "parameters": {
        "column_names": ["stop_signal_delay", "response_accuracy", "face"],
        "ignore_missing": true
    }
}]
```
````

## Results

The results of executing this operation on the [**sample remodel event file**](sample-remodel-event-file-anchor) are shown below. The *face* column is not in the data, but it is ignored, since *ignore_missing* is true. If *ignore_missing* had been false, a `KeyError` would have been raised.

```{admonition} Results of executing the *remove_columns*.
| onset | duration | trial_type | response_time | response_hand | sex |
| ----- | -------- | ---------- | ------------- | ------------- | --- |
| 0.0776 | 0.5083 | go | 0.565 | right | female |
| 5.5774 | 0.5083 | unsuccesful_stop | 0.49 | right | female |
| 9.5856 | 0.5084 | go | 0.45 | right | female |
| 13.5939 | 0.5083 | succesful_stop | n/a | n/a | female |
| 17.1021 | 0.5083 | unsuccesful_stop | 0.633 | left | male |
| 21.6103 | 0.5083 | go | 0.443 | left | male |
```

## Notes

- Set `ignore_missing` to true when removing columns that may not exist in all files
- This is a simple, straightforward operation for data cleanup
- Often used after operations like `remap_columns` that create new columns
- Cannot be undone - ensure you have backups if needed
- Column removal is permanent in the output files

## Related operations

- [Remap columns](remap_columns.md) - Often followed by remove_columns to clean up
- [Reorder columns](reorder_columns.md) - Can also drop columns with keep_others=false
- [Rename columns](rename_columns.md) - Rename rather than remove columns
