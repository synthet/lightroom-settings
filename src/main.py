import os
import shutil
import tempfile
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Header, Form
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel

from .models import LightroomSettings
from .providers.gemini_cli import GeminiCLIProvider

app = FastAPI(title="Lightroom AI Settings Service")

# Currently hardcoded to use Gemini CLI
# This can be made dynamic via injection or configuration
provider = GeminiCLIProvider(cli_path=os.environ.get("GEMINI_CLI_PATH", "gemini"))

@app.post("/analyze", response_model=LightroomSettings)
async def analyze_image(
    image: UploadFile = File(...),
    xmp: Optional[UploadFile] = File(None),
    accept: str = Header(default="application/json")
):
    """
    Analyze an uploaded image (and optional XMP sidecar), returning suggested Lightroom settings.
    By default returns JSON, but can return `.xmp` if Accept header is 'application/rdf+xml'.
    """
    # Create temp directory for incoming files
    with tempfile.TemporaryDirectory() as tempdir:
        temp_dir_path = Path(tempdir)
        
        # Save image
        image_ext = Path(image.filename).suffix if image.filename else ".jpg"
        image_path = temp_dir_path / f"image{image_ext}"
        with image_path.open("wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
            
        # Save XMP if provided
        xmp_path = None
        if xmp:
            xmp_path = temp_dir_path / "settings.xmp"
            with xmp_path.open("wb") as buffer:
                shutil.copyfileobj(xmp.file, buffer)
                
        try:
            settings: LightroomSettings = await provider.process(image_path, xmp_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Provider failed: {str(e)}")
            
        # Handle content negotiation
        if accept == "application/rdf+xml" or accept == "text/xml" or accept == "application/xmp":
            # Generate XMP output
            from .xmp_utils import generate_xmp
            xmp_str = generate_xmp(settings, xmp_path.read_text() if xmp_path else None)
            
            output_xmp_path = temp_dir_path / "output.xmp"
            output_xmp_path.write_text(xmp_str, encoding="utf-8")
            
            return FileResponse(
                path=output_xmp_path,
                filename="suggested_settings.xmp",
                media_type="application/rdf+xml"
            )
            
        # Default behavior is JSON response
        return JSONResponse(content=settings.model_dump())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
