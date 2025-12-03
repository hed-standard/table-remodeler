(factor-column-anchor)=

# Factor column

The *factor_column* operation appends factor vectors to tabular files based on the values in a specified file column. Each factor vector contains a 1 if the corresponding row had that column value and a 0 otherwise. The *factor_column* is used to reformat event files for analyses such as linear regression based on column values.

## Purpose

Use this operation to:

- Create binary factor vectors for statistical analysis
- Convert categorical column values into analysis-ready format
- Generate design matrix columns for regression models
- Prepare data for machine learning algorithms requiring one-hot encoding

(factor-column-parameters-anchor)=

## Parameters

```{admonition} Parameters for the *factor_column* operation.
---
class: tip
---
|  Parameter   | Type | Description | 
| ------------ | ---- | ----------- | 
| *column_name* | str | The name of the column to be factored.| 
| *factor_values* | list | Column values to be included as factors. |
| *factor_names* | list| (**Optional**) Column names for created factors. |
```

If *column_name* is not a column in the data file, a `ValueError` is raised.

If *factor_values* is empty, factors are created for each unique value in *column_name*. Otherwise, only factors for the specified column values are generated. If a specified value is missing in a particular file, the corresponding factor column contains all zeros.

If *factor_names* is empty, the newly created columns are of the form *column_name.factor_value*. Otherwise, the newly created columns have names *factor_names*. If *factor_names* is not empty, then *factor_values* must also be specified and both lists must be of the same length.

(factor-column-example-anchor)=

## Example

The *factor_column* operation in the following example specifies that factor columns should be created for *succesful_stop* and *unsuccesful_stop* of the *trial_type* column. The resulting columns are called *stopped* and *stop_failed*, respectively.

````{admonition} A sample JSON file with a single *factor_column* transformation operation.
---
class: tip
---
```json
[{ 
    "operation": "factor_column",
    "description": "Create factors for the succesful_stop and unsuccesful_stop values.",
    "parameters": {
        "column_name": "trial_type",
        "factor_values": ["succesful_stop", "unsuccesful_stop"],
        "factor_names": ["stopped", "stop_failed"]
    }
}]
```
````

## Results

The results of executing this *factor_column* operation on the [**sample remodel event file**](sample-remodel-event-file-anchor) are:

```{admonition} Results of the factor_column operation on the sample data.

| onset | duration | trial_type | stop_signal_delay | response_time | response_accuracy | response_hand | sex | stopped | stop_failed |
| ----- | -------- | ---------- |  ----------------- | ------------- | ----------------- | ------------- | --- | ---------- | ---------- |
| 0.0776 | 0.5083 | go | n/a | 0.565 | correct | right | female | 0 | 0 |
| 5.5774 | 0.5083 | unsuccesful_stop | 0.2 | 0.49 | correct | right | female | 0 | 1 |
| 9.5856 | 0.5084 | go | n/a | 0.45 | correct | right | female | 0 | 0 |
| 13.5939 | 0.5083 | succesful_stop | 0.2 | n/a | n/a | n/a | female | 1 | 0 |
| 17.1021 | 0.5083 | unsuccesful_stop | 0.25 | 0.633 | correct | left | male | 0 | 1 |
| 21.6103 | 0.5083 | go | n/a | 0.443 | correct | left | male | 0 | 0 |
```

## Notes

- The original columns remain in the data; factor columns are appended
- Each factor column contains only 0s and 1s (binary encoding)
- If `factor_values` is empty, all unique values are automatically factored
- Use `factor_names` to create meaningful column names for your analysis
- Factor columns are useful for creating design matrices in statistical analysis

## Related operations

- [Factor HED tags](factor_hed_tags.md) - Create factors based on HED tag queries
- [Factor HED type](factor_hed_type.md) - Create factors from HED type tags
- [Remap columns](remap_columns.md) - Map multiple column values to new columns
