(summarize-definitions-anchor)=

# Summarize definitions

The summarize definitions operation provides a summary of the `Def-expand` tags found across the dataset, noting any ambiguous or erroneous ones. If working on a BIDS dataset, it will initialize with the known definitions from the sidecar, reporting any deviations from the known definitions as errors.

## Purpose

Use this operation to:

- Verify consistency of HED definitions across dataset
- Identify ambiguous or conflicting definition expansions
- Extract and document all definitions used
- Validate definition usage without requiring original definition sources

**NOTE: This summary is still under development**

(summarize-definitions-parameters-anchor)=

## Parameters

```{admonition} Parameters for the *summarize_definitions* operation.
---
class: tip
---
|  Parameter   | Type | Description | 
| ------------ | ---- | ----------- | 
| *summary_name* | str | A unique name used to identify this summary.| 
| *summary_filename* | str | A unique file basename to use for saving this summary. |
| *append_timecode* | bool | (**Optional**: Default false) If true, append a time code to filename. |
```

The *summarize_definitions* is mainly meant for verifying consistency in unknown `Def-expand` tags. This comes up where you have an assembled dataset, but no longer have the definitions stored (or never created them to begin with).

(summarize-definitions-example-anchor)=

## Example

The following example shows the JSON for including this operation in a remodeling file.

````{admonition} A JSON file with a single *summarize_definitions* summarization operation.
---
class: tip
---
```json
[{
   "operation": "summarize_definitions",
   "description": "Summarize the definitions used in this dataset.",
   "parameters": {
       "summary_name": "HED_column_definition_summary",
       "summary_filename": "HED_column_definition_summary"
   }
}]
```
````

## Results

A text format summary of the results of executing this operation on a HED-annotated dataset shows three sections:

1. **Known Definitions**: Definitions found and their contents
1. **Ambiguous Definitions**: Definitions with placeholder patterns that can't be uniquely resolved
1. **Errors**: Conflicting expansions for the same definition

````{admonition} Sample *summarize_definitions* operation results showing clean definitions.
---
class: tip
---
```text
Summary name: HED_column_definition_summary
Summary type: definitions
Summary filename: HED_column_definition_summary

Overall summary:
   Known Definitions: 3 items
      cross-only: 2 items
         description: A white fixation cross on a black background.
         contents: (Visual-presentation,(Background-view,Black))
      face-image: 2 items
         description: A face image with fixation cross.
         contents: (Visual-presentation,(Foreground-view,(Face,Image)))
      initialize-recording: 2 items
         description: 
         contents: (Recording)
   Ambiguous Definitions: 0 items
   Errors: 0 items
```
````

When there are errors or ambiguities:

````{admonition} Sample showing ambiguous/erroneous definitions.
---
class: tip
---
```text
Summary name: HED_column_definition_summary
Summary type: definitions
Summary filename: HED_column_definition_summary

Overall summary:
   Known Definitions: 1 items
      initialize-recording: 2 items
         description: 
         contents: (Recording)
   Ambiguous Definitions: 1 items
      specify-age/#: (Age/#,Item-count/#)
   Errors: 1 items
      initialize-recording:
         (Event,Recording)
```
````

It is assumed the first definition encountered is the correct definition, unless the first one is ambiguous. Thus, it finds (`Def-expand/Initialize-recording`,(`Recording`) and considers it valid, before encountering (`Def-expand/Initialize-recording`,(`Recording`, `Event`)), which is now deemed an error.

## Notes

- **Requires HED schema**: You must specify a HED schema version
- **Requires sidecar**: BIDS datasets use sidecar definitions as baseline
- Ambiguous definitions use placeholders (#) that can't be uniquely resolved
- Errors indicate conflicting expansions for the same definition name
- First occurrence sets the baseline; subsequent conflicts are flagged
- Currently does not generate individual file summaries (may change)
- Useful for datasets where original definitions are lost or unknown

## Related operations

- [Summarize HED validation](summarize_hed_validation.md) - Validate overall HED annotations
- [Summarize HED tags](summarize_hed_tags.md) - Analyze tag usage patterns
- [Factor HED type](../transformations/factor_hed_type.md) - Use definitions in analysis
