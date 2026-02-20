---
description: How to use the Lightroom MCP Server
---

# Lightroom MCP Workflow

This workflow documents how to interact with the `lightroom` MCP server.
The server has several tools for analyzing and modifying photos in Adobe Lightroom Classic.

## Checking Status
Before interacting with photos, use the `get_studio_info` tool to ensure that the Lightroom catalog is connected and available.

## Reading Metadata
You can fetch details about the currently selected photos in Lightroom.
- `get_selection`: Retrieves the currently selected photos, their IDs, ratings, labels, titles, and pick flags.
- `get_develop_settings`: Retrieves the precise slider values (Exposure, Contrast, Hue/Saturation, etc.) applied to the photos.
- `get_all_metadata`: Combines EXIF, IPTC, XMP, and Lightroom data into a single request.

## Applying Changes
When an agent or user wants to modify a photo's appearance:
1. Generate the desired JSON settings format.
2. Call `set_develop_settings` with those specific settings (e.g. `{"Exposure": 0.5, "Contrast": 10}`).
3. Use `apply_develop_preset` to run an existing preset if requested.

## Setting Ratings and Flags
- `set_rating`: Sets the star rating (0-5)
- `set_label`: Sets the color label
- `set_pick_flag`: Selects "pick", "reject", or "none"

**Note**: You do not need to provide a target photo ID for most mutation operations, as they apply to the *currently selected photos* in the user's Lightroom UI.
