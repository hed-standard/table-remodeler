(rename-columns-anchor)=

# Rename columns

The `rename_columns` operations uses a dictionary to map old column names into new ones.

## Purpose

Use this operation to:

- Standardize column names across datasets
- Make column names more descriptive or meaningful
- Correct column naming errors
- Conform to naming conventions (e.g., BIDS standards)

(rename-columns-parameters-anchor)=

## Parameters

```{admonition} Parameters for *rename_columns*.
---
class: tip
---
|  Parameter   | Type | Description | 
| ------------ | ---- | ----------- | 
| *column_mapping* | dict | The keys are the old column names and the values are the new names.| 
| *ignore_missing* | bool | If false, a `KeyError` is raised if a dictionary key is not a column name. | 

```

If *ignore_missing* is false, a `KeyError` is raised if a column specified in the mapping does not correspond to a column name in the data file.

(rename-columns-example-anchor)=

## Example

The following example renames the `stop_signal_delay` column to be `stop_delay` and the `response_hand` to be `hand_used`.

````{admonition} A JSON file with a single *rename_columns* transformation operation.
---
class: tip
---
```json
[{   
    "operation": "rename_columns",
    "description": "Rename columns to be more descriptive.",
    "parameters": {
        "column_mapping": {
            "stop_signal_delay": "stop_delay",
            "response_hand": "hand_used"
        },
        "ignore_missing": true
    }
}]

```
````

## Results

The results of executing the previous *rename_columns* operation on the [**sample remodel event file**](sample-remodel-event-file-anchor) are:

```{admonition} After the *rename_columns* operation is executed, the sample events file is:
| onset | duration | trial_type | stop_delay | response_time | response_accuracy | hand_used | sex |
| ----- | -------- | ---------- | ----------------- | ------------- | ----------------- | ------------- | --- |
| 0.0776 | 0.5083 | go | n/a | 0.565 | correct | right | female |
| 5.5774 | 0.5083 | unsuccesful_stop | 0.2 | 0.49 | correct | right | female |
| 9.5856 | 0.5084 | go | n/a | 0.45 | correct | right | female |
| 13.5939 | 0.5083 | succesful_stop | 0.2 | n/a | n/a | n/a | female |
| 17.1021 | 0.5083 | unsuccesful_stop | 0.25 | 0.633 | correct | left | male |
| 21.6103 | 0.5083 | go | n/a | 0.443 | correct | left | male |
```

## Notes

- Only renames columns; does not change data values
- Multiple columns can be renamed in a single operation
- Set `ignore_missing` to true for flexible operation across varied datasets
- Column position in the file is not changed
- Use the mapping dictionary to rename as many columns as needed
- Common use: standardizing column names after importing from different sources

## Related operations

- [Reorder columns](reorder_columns.md) - Change column order
- [Remove columns](remove_columns.md) - Remove unwanted columns
- [Remap columns](remap_columns.md) - Change column values (not just names)
