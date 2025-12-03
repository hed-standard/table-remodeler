(merge-consecutive-anchor)=

# Merge consecutive

Sometimes a single long event in experimental logs is represented by multiple repeat events. The *merge_consecutive* operation collapses these consecutive repeat events into one event with duration updated to encompass the temporal extent of the merged events.

## Purpose

Use this operation to:

- Combine consecutive identical events into single longer events
- Clean up experimental logs with repeated event markers
- Consolidate block-level or state-level events
- Correct for data acquisition artifacts that split events

(merge-consecutive-parameters-anchor)=

## Parameters

```{admonition} Parameters for the *merge_consecutive* operation.
---
class: tip
---
|  Parameter   | Type | Description | 
| ------------ | ---- | ----------- | 
| *column_name* | str | The name of the column which is the basis of the merge.| 
| *event_code* | str, int, float | The value in *column_name* that triggers the merge. | 
| *set_durations* | bool | If true, set durations based on merged events. |
| *ignore_missing* | bool | If true, missing *column_name* or *match_columns* do not raise an error. | 
| *match_columns* | list | (**Optional**) Columns whose values must match to collapse events.  | 
```

The first of the group of rows (each representing an event) to be merged is called the anchor for the merge. After the merge, it is the only row in the group that remains in the data file. The result is identical to its original version, except for the value in the `duration` column.

If the *set_duration* parameter is true, the new duration is calculated as though the event began with the onset of the first event (the anchor row) in the group and ended at the point where all the events in the group have ended. This method allows for small gaps between events and for events in which an intermediate event in the group ends after later events. If the *set_duration* parameter is false, the duration of the merged row is set to `n/a`.

If the data file has other columns besides `onset`, `duration` and *column_name*, the values in the other columns must be considered during the merging process. The *match_columns* is a list of the other columns whose values must agree with those of the anchor row in order for a merge to occur. If *match_columns* is empty, the other columns in each row are not taken into account during the merge.

(merge-consecutive-example-anchor)=

## Example

The *merge_consecutive* operation in the following example causes consecutive `succesful_stop` events whose `stop_signal_delay`, `response_hand`, and `sex` columns have the same values to be merged into a single event.

````{admonition} A JSON file with a single *merge_consecutive* transformation operation.
---
class: tip
---
```json
[{ 
    "operation": "merge_consecutive",
    "description": "Merge consecutive *succesful_stop* events that match the *match_columns.",
    "parameters": {
        "column_name": "trial_type",
        "event_code": "succesful_stop",
        "set_durations": true,
        "ignore_missing": true,
        "match_columns": ["stop_signal_delay", "response_hand", "sex"]
    }
}]
```
````

When this operation is applied to the following input file, the three events with a value of `succesful_stop` in the `trial_type` column starting at `onset` value 13.5939 are merged into a single event.

```{admonition} Input file for a *merge_consecutive* operation.

| onset | duration | trial_type | stop_signal_delay | response_hand | sex |
| ----- | -------- | ---------- | ----------------- | ------------- | --- |
| 0.0776 | 0.5083 | go | n/a | right | female| 
| 5.5774 | 0.5083 | unsuccesful_stop | 0.2 | right | female| 
| 9.5856 | 0.5084 | go | n/a | right | female| 
| 13.5939 | 0.5083 | succesful_stop | 0.2 | n/a | female| 
| 14.2 | 0.5083 | succesful_stop | 0.2 |  n/a | female| 
| 15.3 | 0.7083 | succesful_stop | 0.2 |  n/a | female| 
| 17.3 | 0.5083 | unsuccesful_stop | 0.25 |  n/a | female| 
| 19.0 | 0.5083 | unsuccesful_stop | 0.25 | n/a | female| 
| 21.1021 | 0.5083 | unsuccesful_stop | 0.25 | left | male| 
| 22.6103 | 0.5083 | go | n/a | left | male |
```

## Results

Notice that the `succesful_stop` event at `onset` value `17.3` is not merged because the `stop_signal_delay` column value does not match the value in the previous event. The final result has `duration` computed as `2.4144` = `15.3` + `0.7083` - `13.5939`.

```{admonition} The results of the *merge_consecutive* operation.

| onset | duration | trial_type |  stop_signal_delay | response_hand | sex |
| ----- | -------- | ---------- | ------------------ | ------------- | --- |
| 0.0776 | 0.5083 | go | n/a | right | female |
| 5.5774 | 0.5083 | unsuccesful_stop | 0.2 | right | female |
| 9.5856 | 0.5084 | go | n/a | right | female |
| 13.5939 | 2.4144 | succesful_stop | 0.2 | n/a | female |
| 17.3 | 2.2083 | unsuccesful_stop | 0.25 |  n/a | female |
| 21.1021 | 0.5083 | unsuccesful_stop | 0.25 | left | male |
| 22.6103 | 0.5083 | go | n/a | left | male |
```

The events that had onsets at `17.3` and `19.0` are also merged in this example.

## Notes

- Only consecutive events with matching criteria are merged
- The first (anchor) event in the sequence is kept; others are removed
- Duration calculation handles gaps and overlaps intelligently
- Use `match_columns` to ensure only truly identical events merge
- The `event_code` must match exactly (case-sensitive for strings)
- Set `ignore_missing` to true for robust operation across varied datasets

## Related operations

- [Split rows](split_rows.md) - Split trial-level encoding into events (inverse operation)
- [Remove rows](remove_rows.md) - Remove unwanted events
