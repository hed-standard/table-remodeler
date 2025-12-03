(summarize-hed-validation-anchor)=

# Summarize HED validation

The *summarize_hed_validation* operation runs the HED validator on the requested data and produces a summary of the errors. For more information on HED validation, see the [**HED validation guide**](https://www.hed-resources.org/en/latest/HedValidationGuide.html).

## Purpose

Use this operation to:

- Validate HED annotations in event files and sidecars
- Identify annotation errors and warnings
- Check consistency of definitions and tag usage
- Verify onset/offset matching and temporal consistency
- Document validation status for datasets

(summarize-hed-validation-parameters-anchor)=

## Parameters

In addition to the required *summary_name* and *summary_filename* parameters, the *summarize_hed_validation* operation has an optional boolean parameter *check_for_warnings*. If *check_for_warnings* is false, the summary will not report warnings.

```{admonition} Parameters for the *summarize_hed_validation* operation.
---
class: tip
---
|  Parameter   | Type | Description | 
| ------------ | ---- | ----------- | 
| *summary_name* | str | A unique name used to identify this summary.| 
| *summary_filename* | str | A unique file basename to use for saving this summary. |
| *append_timecode* | bool | (**Optional**: Default false) If true, append a time code to filename. |  
| *check_for_warnings* | bool | (**Optional**: Default false) If true, warnings are reported in addition to errors. |  
```

The *summarize_hed_validation* is a HED operation and the calling program must provide a HED schema version and usually a JSON sidecar containing the HED annotations.

The validation process takes place in two stages: first the JSON sidecar is validated. This strategy is used because a single error in the JSON sidecar can generate an error message for every line in the corresponding data file.

If the JSON sidecar has errors (warnings don't count), the validation process is terminated without validation of the data file and assembled HED annotations.

If the JSON sidecar does not have errors, the validator assembles the annotations for each line in the data files and validates the assembled HED annotation. Data file-wide consistency, such as matched onsets and offsets, is also checked.

(summarize-hed-validation-example-anchor)=

## Example

````{admonition} A JSON file with a single *summarize_hed_validation* summarization operation.
---
class: tip
---
```json
[{
   "operation": "summarize_hed_validation",
   "description": "Summarize validation errors in the sample dataset.",
   "parameters": {
       "summary_name": "AOMIC_sample_validation",
       "summary_filename": "AOMIC_sample_validation",
       "check_for_warnings": true
   }
}]
```
````

## Results

To demonstrate the output of the validation operation, we modified the first row of the [**sample remodel event file**](sample-remodel-event-file-anchor) so that `trial_type` column contained the value `baloney` rather than `go`. This modification generates a warning because the meaning of `baloney` is not defined in the [**sample remodel sidecar file**](sample-remodel-sidecar-file-anchor). The results of executing the example operation with the modified file are shown in the following example.

````{admonition} Text summary of *summarize_hed_validation* operation on a modified sample data file.
---
class: tip
---
```text
Summary name: AOMIC_sample_validation
Summary type: hed_validation
Summary filename: AOMIC_sample_validation

Summary details:

Dataset: [1 sidecar files, 1 event files]
   task-stopsignal_acq-seq_events.json: 0 issues
   sub-0013_task-stopsignal_acq-seq_events.tsv: 6 issues

Individual files:

   sub-0013_task-stopsignal_acq-seq_events.tsv: 1 sidecar files
      task-stopsignal_acq-seq_events.json has no issues
      sub-0013_task-stopsignal_acq-seq_events.tsv issues:
            HED_UNKNOWN_COLUMN: WARNING: Column named 'onset' found in file, but not specified as a tag column or identified in sidecars.
            HED_UNKNOWN_COLUMN: WARNING: Column named 'duration' found in file, but not specified as a tag column or identified in sidecars.
            HED_UNKNOWN_COLUMN: WARNING: Column named 'response_time' found in file, but not specified as a tag column or identified in sidecars.
            HED_UNKNOWN_COLUMN: WARNING: Column named 'response_accuracy' found in file, but not specified as a tag column or identified in sidecars.
            HED_UNKNOWN_COLUMN: WARNING: Column named 'response_hand' found in file, but not specified as a tag column or identified in sidecars.
            HED_SIDECAR_KEY_MISSING[row=0,column=2]: WARNING: Category key 'baloney' does not exist in column.  Valid keys are: ['succesful_stop', 'unsuccesful_stop', 'go']

```
````

This summary was produced using HED schema version `hed_version="8.1.0"` when creating the `dispatcher` and using the [**sample remodel sidecar file**](sample-remodel-sidecar-file-anchor) in the `do_op`.

## Notes

- **Requires HED schema**: You must specify a HED schema version when creating the Dispatcher
- **Requires sidecar**: Usually needs JSON sidecar with HED annotations
- **Two-stage validation**: Sidecar validated first, then assembled annotations
- Sidecar errors prevent data file validation (one error can cascade)
- Warnings vs. errors: Errors are more severe; set `check_for_warnings` to see both
- Each issue includes error code, severity level, and specific location
- Essential quality assurance step before using HED-dependent operations
- Run this operation early in your pipeline to catch annotation problems

## Related operations

- [Summarize HED tags](summarize_hed_tags.md) - Analyze tag usage after validation
- [Summarize HED type](summarize_hed_type.md) - Extract design after validation
- [Summarize definitions](summarize_definitions.md) - Check definition consistency
- [Factor HED tags](../transformations/factor_hed_tags.md) - Use validated annotations
