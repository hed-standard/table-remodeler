(factor-hed-type-anchor)=

# Factor HED type

The *factor_hed_type* operation produces factor columns based on values of the specified HED type tag. The most common type is the HED *Condition-variable* tag, which corresponds to factor vectors based on the experimental design. Other commonly use type tags include *Task*, *Control-variable*, and *Time-block*.

We assume that the dataset has been annotated using HED tags to properly document information such as experimental conditions, and focus on how such an annotated dataset can be used with remodeling to produce factor columns corresponding to these type variables.

For additional information on how to encode experimental designs using HED, see [**HED conditions and design matrices**](https://www.hed-resources.org/en/latest/HedConditionsAndDesignMatrices.html).

## Purpose

Use this operation to:

- Extract experimental design factors from HED annotations
- Generate condition-based factor vectors automatically
- Create design matrices reflecting experimental structure
- Identify task blocks and control variables

(factor-hed-type-parameters-anchor)=

## Parameters

```{admonition} Parameters for *factor_hed_type* operation.
---
class: tip
---
|  Parameter   | Type | Description | 
| ------------ | ---- | ----------- | 
| *type_tag* | str | HED tag used to find the factors (most commonly *Condition-variable*).| 
| *type_values* | list | (**Optional**) Values to factor for the *type_tag*.<br>If omitted, all values of that *type_tag* are used. |
```

The event context (as defined by onsets, offsets and durations) is always expanded and one-hot (0's and 1's) encoding is used for the factors.

(factor-hed-type-example-anchor)=

## Example

The *factor_hed_type* operation in the following example appends additional columns to each data file corresponding to each possible value of each *Condition-variable* tag. The columns contain 1's for rows corresponding to rows (e.g., events) for which that condition applies and 0's otherwise.

````{admonition} A JSON file with a single *factor_hed_type* transformation operation.
---
class: tip
---
```json
[{ 
    "operation": "factor_hed_type",
    "description": "Factor based on the sex of the images being presented.",
    "parameters": {
        "type_tag": "Condition-variable"
    }
}]
```
````

## Results

The results of executing this *factor_hed-tags* operation on the [**sample remodel event file**](sample-remodel-event-file-anchor) using the [**sample remodel sidecar file**](sample-remodel-sidecar-file-anchor) for HED annotations are:

```{admonition} Results of *factor_hed_type*.

| onset | duration | trial_type | stop_signal_delay | response_time | response_accuracy | response_hand | sex | Image-sex.Female-image-cond | Image-sex.Male-image-cond |
| ----- | -------- | ---------- | ----------------- | ------------- | ----------------- | ------------- | --- | ------- | ---------- |
| 0.0776 | 0.5083 | go | n/a | 0.565 | correct | right | female | 1 | 0 |
| 5.5774 | 0.5083 | unsuccesful_stop | 0.2 | 0.49 | correct | right | female | 1 | 0 |
| 9.5856 | 0.5084 | go | n/a | 0.45 | correct | right | female | 1 | 0 |
| 13.5939 | 0.5083 | succesful_stop | 0.2 | n/a | n/a | n/a | female | 1 | 0 |
| 17.1021 | 0.5083 | unsuccesful_stop | 0.25 | 0.633 | correct | left | male | 0 | 1 |
| 21.6103 | 0.5083 | go | n/a | 0.443 | correct | left | male | 0 | 1 |
```

## Notes

- **Requires HED schema**: You must specify a HED schema version when creating the Dispatcher
- **Requires sidecar**: Dataset needs HED annotations with type tags in JSON sidecar
- Event context is automatically expanded (accounts for Onset/Offset/Duration)
- Factor names are automatically generated from the type variable names
- Most commonly used with `Condition-variable` for experimental design
- Can specify `type_values` to factor only specific conditions

## Related operations

- [Factor column](factor_column.md) - Create factors from column values
- [Factor HED tags](factor_hed_tags.md) - Create factors from HED queries
- [Summarize HED type](../summarizations/summarize_hed_type.md) - Summarize type tag usage
