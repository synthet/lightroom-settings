import asyncio
import json
from pathlib import Path
from typing import Optional
import typer

from .providers.gemini_cli import GeminiCLIProvider
from .xmp_utils import generate_xmp

app = typer.Typer(help="Lightroom AI Settings CLI Service")

@app.command()
def process(
    image_path: Path = typer.Argument(..., help="Path to the image you want to analyze."),
    xmp_path: Optional[Path] = typer.Option(None, "--xmp", "-x", help="Path to an existing XMP sidecar."),
    output_xmp: Optional[Path] = typer.Option(None, "--output-xmp", "-o", help="A file path to output the generated XMP."),
    gemini_bin: str = typer.Option("gemini", help="Path to the gemini CLI executable.")
):
    """
    Process an image and generate suggested Lightroom settings via the configured AI model.
    """
    if not image_path.exists():
        typer.echo(f"Error: Image {image_path} does not exist.", err=True)
        raise typer.Exit(code=1)

    provider = GeminiCLIProvider(cli_path=gemini_bin)
    
    # Run async function in a sync wrapper
    settings = asyncio.run(provider.process(image_path, xmp_path))
    
    if output_xmp:
        # Load the original content if it was provided
        original_xmp_content = None
        if xmp_path and xmp_path.exists():
            original_xmp_content = xmp_path.read_text(encoding="utf-8")
        
        # Generate the new XMP
        xmp_str = generate_xmp(settings, original_xmp_content)
        output_xmp.write_text(xmp_str, encoding="utf-8")
        typer.echo(f"Saved generated XMP to {output_xmp}")
    else:
        # Just output the JSON to stdout
        typer.echo(settings.model_dump_json(indent=2))

if __name__ == "__main__":
    app()
