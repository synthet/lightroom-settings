# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- **Core Models**: Implemented Pydantic models for Lightroom settings, including Light, Color, Presence, Effects, Detail, and Lens Corrections.
- **AI Providers**:
    - `OpenAIProvider`: Support for image analysis and settings generation using GPT-4o.
    - `GeminiCLIProvider`: Support for image analysis using Gemini via CLI.
    - `MockProvider`: For testing and development without API calls.
- **XMP Logic**: Developed a robust XMP parser and generator to handle Adobe Lightroom Classic sidecar files.
- **Lightroom Classic Integration**:
    - `LRCClient`: A client to interact with the Lightroom Classic MCP server.
    - `MCP Server`: A FastAPI-based MCP server providing tools for image analysis and automated editing.
- **Automation**: `auto_edit.py` for batch processing and automated applying of AI-suggested settings.
- **Testing Suite**:
    - Unit tests for API endpoints (`tests/test_api.py`).
    - Unit tests for XMP parsing and generation (`tests/test_xmp.py`).
    - Logic tests for the parser (`tests/test_parser.py`).
- **Documentation**:
    - Updated `README.md` with project overview and setup instructions.
    - `GEMINI_CLI_ISSUE.md` documenting troubleshooting for Gemini CLI integration.
    - Automation scripts in `scripts/`.
