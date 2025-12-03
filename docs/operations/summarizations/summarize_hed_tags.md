(summarize-hed-tags-anchor)=

# Summarize HED tags

The *summarize_hed_tags* operation extracts a summary of the HED tags present in the annotations of a dataset. This summary operation assumes that the structure in question is suitably annotated with HED (Hierarchical Event Descriptors). You must provide a HED schema version. If the data has annotations in a JSON sidecar, you must also provide its path.

## Purpose

Use this operation to:

- Understand which HED tags are used across the dataset
- Count tag occurrences for documentation
- Organize tags into user-defined categories
- Verify that expected tags appear in annotations

(summarize-hed-tags-parameters-anchor)=

## Parameters

The *summarize_hed_tags* operation has the two required parameters (*tags* and *expand_context*) in addition to the standard *summary_name* and *summary_filename* parameters.

```{admonition} Parameters for the *summarize_hed_tags* operation.
---
class: tip
---
|  Parameter   | Type | Description | 
| ------------ | ---- | ----------- | 
| *summary_name* | str | A unique name used to identify this summary.| 
| *summary_filename* | str | A unique file basename to use for saving this summary. |
| *tags* | dict | Dictionary with category title keys and tags in that category as values. |  
| *append_timecode* | bool | (**Optional**: Default false) If true, append a time code to filename. |  
| *include_context* | bool | (**Optional**: Default true) If true, expand the event context to <br/>account for onsets and offsets. |  
| *remove_types* | list | (**Optional**) A list of types such as <br/>`Condition-variable` and `Task` to remove. |  
| *replace_defs* | bool | (**Optional**: Default true) If true, the `Def` tags are replaced with the<br/>contents of the definition (no `Def` or `Def-expand`). |
```

The *tags* dictionary has keys that specify how the user wishes the tags to be categorized for display. Note that these keys are titles designating display categories, not HED tags.

The *tags* dictionary values are lists of actual HED tags (or their children) that should be listed under the respective display categories.

If the optional parameter *include_context* is true, the counts include tags contributing to the event context in events intermediate between onsets and offsets.

If the optional parameter *replace_defs* is true, the tag counts include tags contributed by contents of the definitions.

(summarize-hed-tags-example-anchor)=

## Example

The following remodeling command specifies that the tag counts should be grouped under the titles: *Sensory events*, *Agent actions*, and *Objects*. Any leftover tags will appear under the title "Other tags".

````{admonition} A JSON file with a single *summarize_hed_tags* summarization operation.
---
class: tip
---
```json
[{
   "operation": "summarize_hed_tags",
   "description": "Summarize the HED tags in the dataset.",
   "parameters": {
       "summary_name": "summarize_hed_tags",
       "summary_filename": "summarize_hed_tags",
       "tags": {
           "Sensory events": ["Sensory-event", "Sensory-presentation",
                              "Task-stimulus-role", "Experimental-stimulus"],
           "Agent actions": ["Agent-action", "Agent", "Action", "Agent-task-role",
                             "Task-action-type", "Participant-response"],
           "Objects": ["Item"]
         }
     }
}]
```
````

## Results

The results of executing this operation on the [**sample remodel event file**](sample-remodel-event-file-anchor) are shown below.

````{admonition} Text summary of *summarize_hed_tags* operation on the sample remodel file.
---
class: tip
---
```text
Summary name: summarize_hed_tags
Summary type: hed_tag_summary
Summary filename: summarize_hed_tags

Overall summary:
Dataset: Total events=1200 Total files=6
	Main tags[events,files]:
		Sensory events:
			Sensory-presentation[6,1] Visual-presentation[6,1] Auditory-presentation[3,1]
		Agent actions:
			Incorrect-action[2,1] Correct-action[1,1]
		Objects:
			Image[6,1]
	Other tags[events,files]:
		Label[6,1] Def[6,1] Delay[3,1]

Individual files:

aomic_sub-0013_excerpt_events.tsv:    
Total events=6 
   Main tags[events,files]:
       Sensory events:
          Sensory-presentation[6,1] Visual-presentation[6,1] Auditory-presentation[3,1]
       Agent actions:
          Incorrect-action[2,1] Correct-action[1,1]
       Objects:
          Image[6,1]
   Other tags[events,files]:
       Label[6,1] Def[6,1] Delay[3,1]

```
````

The HED tag *Task-action-type* was specified in the "Agent actions" category. *Incorrect-action* and *Correct-action*, which are children of *Task-action-type* in the [**HED schema**](https://www.hedtags.org/hed-schema-browser/), will appear with counts in the list under this category.

The sample events file had 6 events, including 1 correct action and 2 incorrect actions. Since only one file was processed, the information for *Dataset* was similar to that presented under *Individual files*.

For a more extensive example, see the [**text**](../../_static/data/summaries/FacePerception_hed_tag_summary.txt) and [**JSON**](../../_static/data/summaries/FacePerception_hed_tag_summary.json) format summaries of the sample dataset [**ds003645s_hed**](https://github.com/hed-standard/hed-examples/tree/main/datasets/eeg_ds003645s_hed) using the [**summarize_hed_tags_rmdl.json**](../../_static/data/summaries/summarize_hed_tags_rmdl.json) remodeling file.

## Notes

- **Requires HED schema**: You must specify a HED schema version
- **Requires sidecar**: Usually needs JSON sidecar with HED annotations
- Child tags automatically included under parent categories
- Counts show [events, files] format
- Use `tags` dictionary to organize output into meaningful categories
- Set `include_context` to include tags from temporal context
- Set `replace_defs` to expand definitions and count their contents
- "Other tags" category automatically created for uncategorized tags

## Related operations

- [Summarize HED type](summarize_hed_type.md) - Extract experimental design
- [Summarize HED validation](summarize_hed_validation.md) - Validate annotations first
- [Factor HED tags](../transformations/factor_hed_tags.md) - Create factors from tag queries
