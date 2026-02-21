import os
import asyncio
from pathlib import Path
from typing import Optional
from mcp.server.fastmcp import FastMCP

from src.providers.gemini_cli import GeminiCLIProvider
from src.models import LightroomSettings

# Initialize FastMCP server
mcp = FastMCP("Lightroom Settings MCP Server")

# Initialize provider
provider = GeminiCLIProvider(cli_path=os.environ.get("GEMINI_CLI_PATH", "gemini.cmd" if os.name == 'nt' else "gemini"))

@mcp.tool()
async def analyze_image(image_path: str, xmp_path: Optional[str] = None) -> str:
    """
    Analyze an image and return suggested Lightroom Develop settings as a JSON string.

    Args:
        image_path: Absolute path to the original image file.
        xmp_path: Optional absolute path to an existing XMP sidecar file for context.
                  This should be provided if the image already has some manual edits.
    """
    img_p = Path(image_path)
    if not img_p.exists():
        return f"Error: Image path {image_path} does not exist."

    xmp_p = Path(xmp_path) if xmp_path else None
    if xmp_p and not xmp_p.exists():
        return f"Error: XMP path {xmp_path} does not exist."

    try:
        settings: LightroomSettings = await provider.process(img_p, xmp_p)
        return settings.model_dump_json(indent=2)
    except Exception as e:
        return f"Error analyzing image: {str(e)}"

if __name__ == "__main__":
    mcp.run()
