(summarize-sidecar-from-events-anchor)=

# Summarize sidecar from events

The summarize sidecar from events operation generates a sidecar template from the event files in the dataset.

## Purpose

Use this operation to:

- Generate initial sidecar templates from existing event files
- Document column structure and categorical values
- Create starting point for HED annotation
- Understand dataset structure before annotation

(summarize-sidecar-from-events-parameters-anchor)=

## Parameters

The following table lists the parameters required for using the summary.

```{admonition} Parameters for the *summarize_sidecar_from_events* operation.
---
class: tip
---
|  Parameter   | Type | Description | 
| ------------ | ---- | ----------- | 
| *summary_name* | str | A unique name used to identify this summary.| 
| *summary_filename* | str | A unique file basename to use for saving this summary. |
| *skip_columns* | list | A list of column names to omit from the sidecar.| 
| *value_columns* | list | A list of columns to treat as value columns in the sidecar. |  
| *append_timecode* | bool | (**Optional**: Default false) If True, append a time code to filename. |  
```

The standard summary parameters, *summary_name* and *summary_filename* are required. The *summary_name* is the unique key used to identify the particular incarnation of this summary in the dispatcher. Since a particular operation file may use a given operation multiple times, care should be taken to make sure that it is unique.

The *summary_filename* should also be unique and is used for saving the summary upon request. When the remodeler is applied to full datasets rather than single files, the summaries are saved in the `derivatives/remodel/summaries` directory under the dataset root. A time stamp and file extension are appended to the *summary_filename* when the summary is saved.

In addition to the standard parameters, *summary_name* and *summary_filename* required of all summaries, the *summarize_sidecar_from_events* operation requires two additional lists to be supplied. The *skip_columns* list specifies the names of columns to skip entirely in generating the sidecar template. The *value_columns* list specifies the names of columns to treat as value columns when generating the sidecar template.

(summarize-sidecar-from-events-example-anchor)=

## Example

The following example shows the JSON for including this operation in a remodeling file.

````{admonition} A JSON file with a single *summarize_sidecar_from_events* summarization operation.
---
class: tip
---
```json
[{
    "operation": "summarize_sidecar_from_events",
    "description": "Generate a sidecar from the excerpted events file.",
    "parameters": {
        "summary_name": "AOMIC_generate_sidecar",
        "summary_filename": "AOMIC_generate_sidecar",
        "skip_columns": ["onset", "duration"],
        "value_columns": ["response_time", "stop_signal_delay"]
    }
}]
  
```
````

## Results

The results of executing this operation on the [**sample remodel event file**](sample-remodel-event-file-anchor) are shown in the following example using the text format.

````{admonition} Sample *summarize_sidecar_from_events* operation results in text format.
---
class: tip
---
```text
Summary name: AOMIC_generate_sidecar
Summary type: events_to_sidecar
Summary filename: AOMIC_generate_sidecar

Dataset: Currently no overall sidecar extraction is available

Individual files:

aomic_sub-0013_excerpt_events.tsv: Total events=6 Skip columns: ['onset', 'duration']
Sidecar:
{
    "trial_type": {
        "Description": "Description for trial_type",
        "HED": {
            "go": "(Label/trial_type, Label/go)",
            "succesful_stop": "(Label/trial_type, Label/succesful_stop)",
            "unsuccesful_stop": "(Label/trial_type, Label/unsuccesful_stop)"
        },
        "Levels": {
            "go": "Here describe column value go of column trial_type",
            "succesful_stop": "Here describe column value succesful_stop of column trial_type",
            "unsuccesful_stop": "Here describe column value unsuccesful_stop of column trial_type"
        }
    },
    "response_accuracy": {
        "Description": "Description for response_accuracy",
        "HED": {
            "correct": "(Label/response_accuracy, Label/correct)"
        },
        "Levels": {
            "correct": "Here describe column value correct of column response_accuracy"
        }
    },
    "response_hand": {
        "Description": "Description for response_hand",
        "HED": {
            "left": "(Label/response_hand, Label/left)",
            "right": "(Label/response_hand, Label/right)"
        },
        "Levels": {
            "left": "Here describe column value left of column response_hand",
            "right": "Here describe column value right of column response_hand"
        }
    },
    "sex": {
        "Description": "Description for sex",
        "HED": {
            "female": "(Label/sex, Label/female)",
            "male": "(Label/sex, Label/male)"
        },
        "Levels": {
            "female": "Here describe column value female of column sex",
            "male": "Here describe column value male of column sex"
        }
    },
    "response_time": {
        "Description": "Description for response_time",
        "HED": "(Label/response_time, Label/#)"
    },
    "stop_signal_delay": {
        "Description": "Description for stop_signal_delay",
        "HED": "(Label/stop_signal_delay, Label/#)"
    }
}
```
````

## Notes

- Generates BIDS-compliant sidecar JSON structure
- Categorical columns get "Levels" and per-value "HED" entries
- Value columns get placeholder HED annotations with `#` for numeric values
- All descriptions are placeholders - must be manually filled in
- Use `skip_columns` for columns not needing annotation (onset, duration, sample)
- Use `value_columns` for numeric/continuous data columns
- Output provides starting template for manual annotation
- JSON format output can be directly edited for final sidecar

## Related operations

- [Summarize column names](summarize_column_names.md) - Understand column structure first
- [Summarize column values](summarize_column_values.md) - See value distributions before template generation
- [Summarize HED validation](summarize_hed_validation.md) - Validate after manual annotation
