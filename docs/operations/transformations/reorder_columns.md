(reorder-columns-anchor)=

# Reorder columns

The *reorder_columns* operation reorders the indicated columns in the specified order. This operation is often used to place the most important columns near the beginning of the file for readability or to assure that all the data files in dataset have the same column order. Additional parameters control how non-specified columns are treated.

## Purpose

Use this operation to:

- Ensure consistent column order across dataset files
- Place important columns at the beginning for readability
- Conform to standards (e.g., BIDS requires `onset` and `duration` first)
- Remove unwanted columns while reordering (using keep_others=false)

(reorder-columns-parameters-anchor)=

## Parameters

```{admonition} Parameters for the *reorder_columns* operation.
---
class: tip
---
|  Parameter   | Type | Description | 
| ------------ | ---- | ----------- | 
| *column_order* | list | A list of columns in the order they should appear in the data.| 
| *ignore_missing* | bool | Controls handling column names in the reorder list that aren't in the data. | 
| *keep_others* | bool | Controls handling of columns not in the reorder list. | 

```

If *ignore_missing* is true and items in the reorder list do not exist in the file, the missing columns are ignored. On the other hand, if *ignore_missing* is false, a column name in the reorder list that is missing from the data raises a *ValueError*.

The *keep_others* parameter controls whether columns in the data that do not appear in the *column_order* list are dropped (*keep_others* is false) or put at the end in the relative order that they appear in the file (*keep_others* is true).

BIDS event files are required to have `onset` and `duration` as the first and second columns, respectively.

(reorder-columns-example-anchor)=

## Example

The *reorder_columns* operation in the following example specifies that the first four columns of the dataset should be: `onset`, `duration`, `response_time`, and `trial_type`. Since *keep_others* is false, these will be the only columns retained.

````{admonition} A JSON file with a single *reorder_columns* transformation operation.
---
class: tip
---
```json
[{   
    "operation": "reorder_columns",
    "description": "Reorder columns.",
    "parameters": {
        "column_order": ["onset", "duration", "response_time",  "trial_type"],
        "ignore_missing": true,
        "keep_others": false
    }
}]
```
````

## Results

The results of executing the previous *reorder_columns* transformation on the [**sample remodel event file**](sample-remodel-event-file-anchor) are:

```{admonition} Results of *reorder_columns*.

| onset | duration | response_time | trial_type |
| ----- | -------- | ---------- | ------------- |
| 0.0776 | 0.5083 | 0.565 | go |
| 5.5774 | 0.5083 | 0.49 | unsuccesful_stop |
| 9.5856 | 0.5084 | 0.45 | go |
| 13.5939 | 0.5083 | n/a | succesful_stop |
| 17.1021 | 0.5083 | 0.633 | unsuccesful_stop |
| 21.6103 | 0.5083 | 0.443 | go |
```

## Notes

- With `keep_others=false`, this operation can also remove columns
- BIDS standard requires `onset` and `duration` as the first two columns
- Set `ignore_missing=true` for robust operation across varied datasets
- Unspecified columns are appended at the end if `keep_others=true`
- Useful for ensuring consistency across multiple event files in a dataset
- Can be combined with other operations for complete dataset reorganization

## Related operations

- [Rename columns](rename_columns.md) - Change column names
- [Remove columns](remove_columns.md) - Remove columns explicitly
- [Remap columns](remap_columns.md) - Restructure column values
