---
description: How to use the Serena MCP Server
---

# Serena MCP Workflow

This workflow documents how to interact with the `serena` MCP server for code navigation, searching, and structural edits.

## Finding and Analyzing Code
When you need to find where something is defined or used:
1. `find_symbol`: Retrieve information on symbols (classes, methods). Use `name_path_pattern` to describe what you're looking for.
2. `get_symbols_overview`: Pass a `relative_path` to get a high-level table of contents for a file.
3. `find_referencing_symbols`: Find all places in the codebase that use a particular symbol.
4. `search_for_pattern`: Flexibly search for strings/patterns if you don't know the exact symbol name.

## Editing Code structurally
Serena excels at safely editing code structure without needing full file replacements:
1. `insert_after_symbol` / `insert_before_symbol`: Great for adding new methods or imports.
2. `replace_symbol_body`: Selectively replace the contents of a known method or class.
3. `rename_symbol`: Safely rename a symbol across the entire codebase.

## Managing Project State
Use `activate_project` to make `d:/Projects/lightroom-gemini` the active target for all subsequent Serena commands.
