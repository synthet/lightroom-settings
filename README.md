# Lightroom Gemini

An AI-powered tool for evaluating, scoring, and culling photos in Lightroom.

## Architecture

This project is built using Python and provides both a REST API (using FastAPI) and a CLI (using Typer). The goal is to evaluate images and process Lightroom XMP sidecar data through an AI model (like Gemini) to output perfect Lightroom development settings.

**Directory Structure:**
- `/src/core`: Core application logic, configuration, and shared utilities.
- `/src/models`: Data models, Pydantic schemas, and database interactions.
- `/tests`: Unit and integration test suites.
- `/mailbox`: Designated Agent Mailbox directory for communicating with external workflows (e.g., secondary agent in Cursor).

**Design Patterns & Standards:**
- Maintains a modular architecture with strict separation of concerns.
- Uses Dependency Injection for provider services.
- Emphasizes clean, self-documenting code with comprehensive error logging.

## Integrations

- **MCP Servers**: The project utilizes the Model Context Protocol (MCP) to seamlessly integrate specialized capabilities:
    - **Filesystem**: Read/write local configs, logs, and metadata.
    - **GitHub**: Source control and issue management.
    - **Brave Search**: Real-time documentation querying.
    - **Lightroom**: Direct interaction with Adobe Lightroom Classic for read/write of Develop Settings.

## Getting Started

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate the environment:
   - Windows: `venv\Scripts\activate`
   - Linux/macOS: `source venv/bin/activate`
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the API server:
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000
   ```
