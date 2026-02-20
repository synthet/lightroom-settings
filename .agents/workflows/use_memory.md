---
description: How to use the Memory MCP Server
---

# Memory MCP Workflow

This workflow documents how to interact with the `memory` MCP server to maintain a structured Knowledge Graph of the project architecture and important details.

## Creating Concepts (Entities)
When you discover or define a new system component, API, or rule:
1. Call `create_entities` to add it to the graph. 
   - `name`: E.g., `LightroomAIService`, `GeminiCLIProvider`
   - `entityType`: E.g., `Service`, `Architecture`, `Dependency`
   - `observations`: Bullet points describing what it does.

## Connecting Concepts (Relations)
When you establish how components interact:
1. Call `create_relations`.
   - `from`: `LightroomAIService`
   - `to`: `GeminiCLIProvider`
   - `relationType`: `uses`

## Retrieving History
If you return to a project or need to recall how a system was designed:
1. Call `search_nodes` with a related query to pull up the graph data and see all related components and their observations.
