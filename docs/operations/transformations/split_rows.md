(split-rows-anchor)=

# Split rows

The *split_rows* operation is often used to convert event files from trial-level encoding to event-level encoding. This operation is meant only for tabular files that have `onset` and `duration` columns.

In **trial-level** encoding, all the events in a single trial (usually some variation of the cue-stimulus-response-feedback-ready sequence) are represented by a single row in the data file. Often, the onset corresponds to the presentation of the stimulus, and the other events are not reported or are implicitly reported.

In **event-level** encoding, each row represents the temporal marker for a single event. In this case a trial consists of a sequence of multiple events.

## Purpose

Use this operation to:

- Convert trial-level encoding to event-level encoding
- Unfold implicit timing information into explicit events
- Create separate event markers for responses, stimuli, or other sub-trial events
- Prepare data for analyses requiring event-level granularity

(split-rows-parameters-anchor)=

## Parameters

```{admonition} Parameters for the *split_rows* operation.
---
class: tip
---
|  Parameter   | Type | Description | 
| ------------ | ---- | ----------- | 
| *anchor_column* | str | The name of the column that will be used for split_rows codes.| 
| *new_events* | dict | Dictionary whose keys are the codes to be inserted as new events<br>in the *anchor_column* and whose values are dictionaries with<br>keys *onset_source*, *duration*, and *copy_columns (**Optional**)*. | 
| *remove_parent_event* | bool | If true, remove parent event. | 

```

The *split_rows* operation requires an *anchor_column*, which could be an existing column or a new column to be appended to the data. The purpose of the *anchor_column* is to hold the codes for the new events.

The *new_events* dictionary has the new events to be created. The keys are the new event codes to be inserted into the *anchor_column*. The values in *new_events* are themselves dictionaries. Each of these dictionaries has three keys:

- *onset_source* is a list of items to be added to the *onset* of the event row being split to produce the `onset` column value for the new event. These items can be any combination of numerical values and column names.
- *duration* a list of numerical values and/or column names whose values are to be added to compute the `duration` column value for the new event.
- *copy_columns* a list of column names whose values should be copied into each new event. Unlisted columns are filled with `n/a`.

The *split_rows* operation sorts the split rows by the `onset` column and raises a `TypeError` if the `onset` and `duration` are improperly defined. The `onset` column is converted to numeric values as part splitting process.

(split-rows-example-anchor)=

## Example

The *split_rows* operation in the following example specifies that new rows should be added to encode the response and stop signal. The anchor column is `trial_type`.

````{admonition} A JSON file with a single *split_rows* transformation operation.
---
class: tip
---
```json
[{
  "operation": "split_rows",
  "description": "add response events to the trials.",
        "parameters": {
            "anchor_column": "trial_type",
            "new_events": {
                "response": {
                    "onset_source": ["response_time"],
                    "duration": [0],
                    "copy_columns": ["response_accuracy", "response_hand", "sex", "trial_number"]
                },
                "stop_signal": {
                    "onset_source": ["stop_signal_delay"],
                    "duration": [0.5],
                    "copy_columns": ["trial_number"]
                }
            },	
            "remove_parent_event": false
        }
    }]
```
````

## Results

The results of executing this *split_rows* operation on the [**sample remodel event file**](sample-remodel-event-file-anchor) are:

```{admonition} Results of the previous *split_rows* operation.

| onset | duration | trial_type | stop_signal_delay | response_time | response_accuracy | response_hand | sex |
| ----- | -------- | ---------- | ----------------- | ------------- | ----------------- | ------------- | --- |
| 0.0776 | 0.5083 | go | n/a | 0.565 | correct | right | female |
| 0.6426 | 0 | response | n/a | n/a | correct | right | female |
| 5.5774 | 0.5083 | unsuccesful_stop | 0.2 | 0.49 | correct | right | female |
| 5.7774 | 0.5 | stop_signal | n/a | n/a | n/a | n/a | n/a |
| 6.0674 | 0 | response | n/a | n/a | correct | right | female |
| 9.5856 | 0.5084 | go | n/a | 0.45 | correct | right | female |
| 10.0356 | 0 | response | n/a | n/a | correct | right | female |
| 13.5939 | 0.5083 | succesful_stop | 0.2 | n/a | n/a | n/a | female |
| 13.7939 | 0.5 | stop_signal | n/a | n/a | n/a | n/a | n/a |
| 17.1021 | 0.5083 | unsuccesful_stop | 0.25 | 0.633 | correct | left | male |
| 17.3521 | 0.5 | stop_signal | n/a | n/a | n/a | n/a | n/a |
| 17.7351 | 0 | response | n/a | n/a | correct | left | male |
| 21.6103 | 0.5083 | go | n/a | 0.443 | correct | left | male |
| 22.0533 | 0 | response | n/a | n/a | correct | left | male |
```

In a full processing example, it might make sense to rename `trial_type` to be `event_type` and to delete the `response_time` and the `stop_signal_delay` columns, since these items have been unfolded into separate events. This could be accomplished in subsequent clean-up operations.

## Notes

- Onset times are computed by adding values from `onset_source` to the parent event's onset
- Duration can be computed from column values or specified as constants
- Use `copy_columns` to preserve relevant information in new events
- Unlisted columns default to `n/a` in new events
- Results are automatically sorted by onset time
- Set `remove_parent_event=true` to keep only the newly created events
- Often followed by cleanup operations (rename_columns, remove_columns)

## Related operations

- [Merge consecutive](merge_consecutive.md) - Opposite operation (combine events)
- [Rename columns](rename_columns.md) - Often used after split_rows for cleanup
- [Remove columns](remove_columns.md) - Clean up timing columns after splitting
