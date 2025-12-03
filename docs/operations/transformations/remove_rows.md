(remove-rows-anchor)=

# Remove rows

The *remove_rows* operation eliminates rows in which the named column has one of the specified values. This operation is useful for removing event markers corresponding to particular types of events or, for example having `n/a` in a particular column.

## Purpose

Use this operation to:

- Filter out unwanted event types
- Remove rows with missing values (`n/a`) in specific columns
- Exclude specific trial types from analysis
- Clean up event files by removing non-essential markers

(remove-rows-parameters-anchor)=

## Parameters

```{admonition} Parameters for *remove_rows*.
---
class: tip
---
|  Parameter   | Type | Description | 
| ------------ | ---- | ----------- | 
| *column_name* | str | The name of the column to be tested.| 
| *remove_values* | list | A list of values to be tested for removal. | 
```

The operation does not raise an error if a data file does not have a column named *column_name* or is missing a value in *remove_values*.

(remove-rows-example-anchor)=

## Example

The following *remove_rows* operation removes the rows whose *trial_type* column contains either `succesful_stop` or `unsuccesful_stop`.

````{admonition} A JSON file with a single *remove_rows* transformation operation.
---
class: tip
---
```json
[{   
    "operation": "remove_rows",
    "description": "Remove rows where trial_type is either succesful_stop or unsuccesful_stop.",
    "parameters": {
        "column_name": "trial_type",
        "remove_values": ["succesful_stop", "unsuccesful_stop"]
    }
}]
```
````

## Results

The results of executing the previous *remove_rows* operation on the [**sample remodel event file**](sample-remodel-event-file-anchor) are:

```{admonition} The results of executing the previous *remove_rows* operation.

| onset | duration | trial_type | stop_signal_delay | response_time | response_accuracy | response_hand | sex |
| ----- | -------- | ---------- | ----------------- | ------------- | ----------------- | ------------- | --- |
| 0.0776 | 0.5083 | go | n/a | 0.565 | correct | right | female |
| 9.5856 | 0.5084 | go | n/a | 0.45 | correct | right | female |
| 21.6103 | 0.5083 | go | n/a | 0.443 | correct | left | male |
```

After removing rows with `trial_type` equal to `succesful_stop` or `unsuccesful_stop` only the three `go` trials remain.

## Notes

- Row removal is permanent in the output files - ensure you have backups
- Does not raise errors if the column is missing from a file
- Does not raise errors if specified values don't appear in the data
- Value matching is exact and case-sensitive
- Commonly used to filter out practice trials, calibration events, or error trials
- Can remove rows with `n/a` values by including "n/a" in `remove_values`

## Related operations

- [Remove columns](remove_columns.md) - Remove entire columns
- [Merge consecutive](merge_consecutive.md) - Combine rows instead of removing them
- [Split rows](split_rows.md) - Add rows instead of removing them
