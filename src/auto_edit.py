import asyncio
import tempfile
from pathlib import Path

from .lrc_client import LightroomMCPClient
from .providers.gemini_cli import GeminiCLIProvider
import typer
import logging

app = typer.Typer(help="Lightroom MCP Auto-Editor Workflow")
logger = logging.getLogger(__name__)

async def auto_edit_workflow(provider_name: str = "gemini"):
    """
    End-to-end workflow:
    1. Connect to Lightroom via MCP Broker
    2. Get currently selected photo preview
    3. Run it through the chosen AI Provider
    4. Automatically apply settings in Lightroom
    """
    lrc = LightroomMCPClient()
    
    typer.echo("Fetching selected photos from Lightroom...")
    photos = await lrc.get_selected_photos()
    if not photos:
        typer.echo("No photos selected in Lightroom.")
        return

    photo = photos[0]
    typer.echo(f"Processing photo: {photo.get('filename')}")
    
    typer.echo("Fetching photo preview...")
    preview_bytes = await lrc.get_photo_preview(photo.get("localId"))
    
    if not preview_bytes:
        typer.echo("Failed to get photo preview from Lightroom.")
        return

    # Initialize the provider
    if provider_name.lower() == "openai":
        from .providers.openai_provider import OpenAIProvider
        provider = OpenAIProvider()
    else:
        provider = GeminiCLIProvider()

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir) / "preview.jpg"
        tmp_path.write_bytes(preview_bytes)
        
        typer.echo(f"Invoking {provider.__class__.__name__} to calculate settings...")
        
        # We can also fetch existing settings from LRC to pass as context via get_all_metadata,
        # but for now we'll do cold generation.
        settings = await provider.process(tmp_path)
        
    typer.echo("Suggested Settings:")
    typer.echo(settings.model_dump_json(indent=2))
    
    typer.echo("Applying settings back to Lightroom...")
    result = await lrc.apply_develop_settings(settings)
    typer.echo(f"Lightroom response: {result}")
    
    typer.echo("Auto-edit complete!")

@app.command()
def auto_edit(provider: str = typer.Option("gemini", help="Provider to use (gemini or openai)")):
    """Run the auto-editor on the active Lightroom selection."""
    logging.basicConfig(level=logging.INFO)
    asyncio.run(auto_edit_workflow(provider))

if __name__ == "__main__":
    app()
