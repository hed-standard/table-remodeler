(summarize-column-values-anchor)=

# Summarize column values

The summarize column values operation provides a summary of the number of times various column values appear in event files across the dataset.

## Purpose

Use this operation to:

- Understand the distribution of categorical values in columns
- Identify unexpected or erroneous column values
- Count unique values per column across the dataset
- Profile datasets before analysis

(summarize-columns-values-parameters-anchor)=

## Parameters

The following table lists the parameters required for using the summary.

```{admonition} Parameters for the *summarize_column_values* operation.
---
class: tip
---
|  Parameter   | Type | Description | 
| ------------ | ---- | ----------- | 
| *summary_name* | str | A unique name used to identify this summary.| 
| *summary_filename* | str | A unique file basename to use for saving this summary. |
| *append_timecode* | bool | (**Optional**: Default false) If True, append a time code to filename. |  
| *max_categorical* | int | (**Optional**: Default 50) If given, the text summary shows top *max_categorical* values.<br/>Otherwise the text summary displays all categorical values.|   
| *skip_columns* | list | (**Optional**) A list of column names to omit from the summary.| 
| *value_columns* | list | (**Optional**) A list of columns to omit the listing unique values. |  
| *values_per_line* | int | (**Optional**: Default 5) If given, the text summary displays this <br/>number of values per line (default is 5).|   

```

In addition to the standard parameters, *summary_name* and *summary_filename* required of all summaries, the *summarize_column_values* operation requires two additional lists to be supplied. The *skip_columns* list specifies the names of columns to skip entirely in the summary. Typically, the `onset`, `duration`, and `sample` columns are skipped, since they have unique values for each row and their values have limited information.

The *summarize_column_values* is mainly meant for creating summary information about columns containing a finite number of distinct values. Columns that contain numeric information will usually have distinct entries for each row in a tabular file and are not amenable to such summarization. These columns could be specified as *skip_columns*, but another option is to designate them as *value_columns*. The *value_columns* are reported in the summary, but their distinct values are not reported individually.

For datasets that include multiple tasks, the event values for each task may be distinct. The *summarize_column_values* operation does not separate by task, but expects the calling programs filter the files by task as desired. The `run_remodel` program supports selecting files corresponding to a particular task.

Two additional optional parameters are available for specifying aspects of the text summary output. The *max_categorical* optional parameter specifies how many unique values should be displayed for each column. The *values_per_line* controls how many categorical column values (with counts) are displayed on each line of the output. By default, 5 values are displayed.

(summarize-column-values-example-anchor)=

## Example

The following example shows the JSON for including this operation in a remodeling file.

````{admonition} A JSON file with a single *summarize_column_values* summarization operation.
---
class: tip
---
```json
[{
   "operation": "summarize_column_values",
   "description": "Summarize the column values in an excerpt.",
   "parameters": {
       "summary_name": "AOMIC_column_values",
       "summary_filename": "AOMIC_column_values",
       "skip_columns": ["onset", "duration"],
       "value_columns": ["response_time", "stop_signal_delay"]
   }
}]
```
````

## Results

A text format summary of the results of executing this operation on the [**sample remodel event file**](sample-remodel-event-file-anchor) is shown in the following example.

````{admonition} Sample *summarize_column_values* operation results in text format.
---
class: tip
---
```text
Summary name: AOMIC_column_values
Summary type: column_values
Summary filename: AOMIC_column_values

Overall summary:
Dataset: Total events=6 Total files=1
   Categorical column values[Events, Files]:
      response_accuracy:
         correct[5, 1] n/a[1, 1]
      response_hand:
         left[2, 1] n/a[1, 1] right[3, 1]
      sex:
         female[4, 1] male[2, 1]
      trial_type:
         go[3, 1] succesful_stop[1, 1] unsuccesful_stop[2, 1]
   Value columns[Events, Files]:
      response_time[6, 1]
      stop_signal_delay[6, 1]

Individual files:

sub-0013_task-stopsignal_acq-seq_events.tsv:
Total events=200
      Categorical column values[Events, Files]:
         response_accuracy:
            correct[5, 1] n/a[1, 1]
         response_hand:
            left[2, 1] n/a[1, 1] right[3, 1]
         sex:
            female[4, 1] male[2, 1]
         trial_type:
            go[3, 1] succesful_stop[1, 1] unsuccesful_stop[2, 1]
      Value columns[Events, Files]:
         response_time[6, 1]
         stop_signal_delay[6, 1]
```
````

Because the [**sample remodel event file**](sample-remodel-event-file-anchor) only has 6 events, we expect that no value will be represented in more than 6 events. The column names corresponding to value columns just have the event counts in them.

This command was executed with the `-i` option in `run_remodel`, results from the individual data files are shown after the overall summary. The individual results are similar to the overall summary because only one data file was processed.

For a more extensive example see the [**text**](../../_static/data/summaries/FacePerception_column_values_summary.txt) and [**JSON**](../../_static/data/summaries/FacePerception_column_values_summary.json) format summaries of the sample dataset [**ds003645s_hed**](https://github.com/hed-standard/hed-examples/tree/main/datasets/eeg_ds003645s_hed) using the [**summarize_columns_rmdl.json**](../../_static/data/summaries/summarize_columns_rmdl.json) remodeling file.

## Notes

- Essential for understanding categorical column distributions
- Use `skip_columns` for high-cardinality columns (onset, duration, sample)
- Use `value_columns` for numeric columns to avoid listing all unique values
- Counts show [events_with_value, files_with_value] format
- Helps identify data quality issues and unexpected values
- Text output formatting controlled by `values_per_line` and `max_categorical`

## Related operations

- [Summarize column names](summarize_column_names.md) - Check column structure first
- [Summarize sidecar from events](summarize_sidecar_from_events.md) - Generate sidecar from values
- [Remove rows](../transformations/remove_rows.md) - Filter based on discovered values
