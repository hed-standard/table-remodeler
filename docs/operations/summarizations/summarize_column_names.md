(summarize-column-names-anchor)=

# Summarize column names

The *summarize_column_names* tracks the unique column name patterns found in data files across the dataset and which files have these column names. This summary is useful for determining whether there are any non-conforming data files.

Often event files associated with different tasks have different column names, and this summary can be used to verify that the files corresponding to the same task have the same column names.

A more problematic issue is when some event files for the same task have reordered column names or use different column names.

## Purpose

Use this operation to:

- Verify consistent column structure across dataset files
- Identify files with non-standard column arrangements
- Check for column order inconsistencies
- Document column patterns for different tasks

(summarize-columns-names-parameters-anchor)=

## Parameters

The *summarize_column_names* operation only has the two parameters required of all summaries.

```{admonition} Parameters for the *summarize_column_names* operation.
---
class: tip
---
|  Parameter   | Type | Description | 
| ------------ | ---- | ----------- | 
| *summary_name* | str | A unique name used to identify this summary.| 
| *summary_filename* | str | A unique file basename to use for saving this summary. |  
| *append_timecode* | bool | (**Optional**: Default false) If true, append a time code to filename. |
```

(summarize-column-names-example-anchor)=

## Example

The following example remodeling file produces a summary, which when saved will appear with file name `AOMIC_column_names_xxx.txt` or `AOMIC_column_names_xxx.json` where `xxx` is a timestamp.

````{admonition} A JSON file with a single *summarize_column_names* summarization operation.
---
class: tip
---
```json   
[{
    "operation": "summarize_column_names",
    "description": "Summarize column names.",
    "parameters": {
        "summary_name": "AOMIC_column_names",
        "summary_filename": "AOMIC_column_names"
    }    
}]
```
````

## Results

When this operation is applied to the [**sample remodel event file**](sample-remodel-event-file-anchor), the following text summary is produced.

````{admonition} Result of applying *summarize_column_names* to the sample remodel file.
---
class: tip
---
```text

Summary name: AOMIC_column_names
Summary type: column_names
Summary filename: AOMIC_column_names

Summary details:

Dataset: Number of files=1
    Columns: ['onset', 'duration', 'trial_type', 'stop_signal_delay', 'response_time', 'response_accuracy', 'response_hand', 'sex']
        sub-0013_task-stopsignal_acq-seq_events.tsv

Individual files:

sub-0013_task-stopsignal_acq-seq_events.tsv: 
   ['onset', 'duration', 'trial_type', 'stop_signal_delay', 'response_time', 'response_accuracy', 'response_hand', 'sex']
		
```
````

Since we are only summarizing one event file, there is only one unique pattern -- corresponding to the columns: *onset*, *duration*, *trial_type*, *stop_signal_delay*, *response_time*, *response_accuracy*, *response_hand*, and *response_time*.

When the dataset has multiple column name patterns, the summary lists unique pattern separately along with the names of the data files that have this pattern.

The JSON version of the summary is useful for programmatic manipulation, while the text version shown above is more readable.

## Notes

- Simple but powerful operation for quality assurance
- Helps identify files with different column structures
- Each unique column pattern is listed with its associated files
- Use early in analysis pipelines to catch structural issues
- JSON output enables automated consistency checking
- No complex parameters required - straightforward to use

## Related operations

- [Summarize column values](summarize_column_values.md) - Analyze column content
- [Reorder columns](../transformations/reorder_columns.md) - Fix column order issues
- [Rename columns](../transformations/rename_columns.md) - Standardize column names
