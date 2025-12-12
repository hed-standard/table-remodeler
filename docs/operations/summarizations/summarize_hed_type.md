(summarize-hed-type-anchor)=

# Summarize HED type

The *summarize_hed_type* operation is designed to extract experimental design matrices or other experimental structure. This summary operation assumes that the structure in question is suitably annotated with HED (Hierarchical Event Descriptors). The [**HED conditions and design matrices guide**](https://www.hedtags.org/hed-resources/HedConditionsAndDesignMatrices.html) explains how this works.

## Purpose

Use this operation to:

- Extract experimental design information from HED annotations
- Document condition variables and their levels
- Understand task structure and blocks
- Generate design matrix information for analysis

(summarize-hed-type-parameters-anchor)=

## Parameters

The *summarize_hed_type* operation provides detailed information about a specified tag, usually `Condition-variable` or `Task`. This summary provides useful information about experimental design.

```{admonition} Parameters for the *summarize_hed_type* operation.
---
class: tip
---
|  Parameter   | Type | Description | 
| ------------ | ---- | ----------- | 
| *summary_name* | str | A unique name used to identify this summary.| 
| *summary_filename* | str | A unique file basename to use for saving this summary. |
| *type_tag* | str | Tag to produce a summary for (most often *condition-variable*).|  
| *append_timecode* | bool | (**Optional**: Default false) If true, append a time code to filename.| 
```

In addition to the two standard parameters (*summary_name* and *summary_filename*), the *type_tag* parameter is required. Only one tag can be given, so you must provide a separate operations in the remodel file for multiple type tags.

(summarize-hed-type-example-anchor)=

## Example

````{admonition} A JSON file with a single *summarize_hed_type* summarization operation.
---
class: tip
---
```json
[{
   "operation": "summarize_hed_type",
   "description": "Summarize experimental conditions.",
   "parameters": {
       "summary_name": "AOMIC_condition_variables",
       "summary_filename": "AOMIC_condition_variables",
       "type_tag": "condition-variable"
   }
}]
```
````

## Results

The results of executing this operation on the [**sample remodel event file**](sample-remodel-event-file-anchor) are shown below.

````{admonition} Text summary of *summarize_hed_types* operation on the sample remodel file.
---
class: tip
---
```text
Summary name: AOMIC_condition_variables
Summary type: hed_type_summary
Summary filename: AOMIC_condition_variables

Overall summary:

Dataset: Type=condition-variable Type values=1 Total events=6 Total files=1
   image-sex: 2 levels in 6 event(s) out of 6 total events in 1 file(s)
       female-image-cond [4,1]: ['Female', 'Image', 'Face']
       male-image-cond [2,1]: ['Male', 'Image', 'Face']

Individual files:

aomic_sub-0013_excerpt_events.tsv:
Type=condition-variable Total events=6 
      image-sex: 2 levels in 6 events
         female-image-cond [4 events, 1 files]: 
            Tags: ['Female', 'Image', 'Face']
         male-image-cond [2 events, 1 files]: 
            Tags: ['Male', 'Image', 'Face']
```
````

Because *summarize_hed_type* is a HED operation, a HED schema version is required and a JSON sidecar is also usually needed. This summary was produced by using `hed_version="8.1.0"` when creating the `dispatcher` and using the [**sample remodel sidecar file**](sample-remodel-sidecar-file-anchor) in the `do_op`. The sidecar provides the annotations that use the `condition-variable` tag in the summary.

For a more extensive example, see the [**text**](../../_static/data/summaries/FacePerception_hed_type_summary.txt) and [**JSON**](../../_static/data/summaries/FacePerception_hed_type_summary.json) format summaries of the sample dataset [**ds003645s_hed**](https://github.com/hed-standard/hed-examples/tree/main/datasets/eeg_ds003645s_hed) using the [**summarize_hed_types_rmdl.json**](../../_static/data/summaries/summarize_hed_types_rmdl.json) remodeling file.

## Notes

- **Requires HED schema**: You must specify a HED schema version
- **Requires sidecar**: JSON sidecar with HED type annotations required
- Most commonly used with `type_tag="Condition-variable"`
- Each type variable shows its levels and associated tags
- Counts show [events, files] format
- Essential for understanding experimental design
- Can be used with `Task`, `Control-variable`, `Time-block`, etc.
- Provides information needed for creating design matrices

## Related operations

- [Summarize HED tags](summarize_hed_tags.md) - Broader tag usage summary
- [Factor HED type](../transformations/factor_hed_type.md) - Create factors from type tags
- [Summarize HED validation](summarize_hed_validation.md) - Validate annotations first
