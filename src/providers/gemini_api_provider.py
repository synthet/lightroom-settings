import logging
from pathlib import Path
from typing import Optional
import os

from google import genai
from google.genai import types

from .base import ProviderBase
from ..models import LightroomSettings

logger = logging.getLogger(__name__)

class GeminiAPIProvider(ProviderBase):
    """
    Provider that invokes the Google Gemini API directly using the google-genai library.
    Requires GOOGLE_API_KEY environment variable or config.json.
    """
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-2.0-flash"):
        # Prioritize constructor arg, then config.json, then env var
        self.api_key = api_key
        
        if not self.api_key:
            config_path = Path("config.json")
            if config_path.exists():
                try:
                    import json
                    config = json.loads(config_path.read_text())
                    self.api_key = config.get("GOOGLE_API_KEY")
                except Exception as e:
                    logger.warning(f"Failed to load config.json: {e}")

        if not self.api_key:
            self.api_key = os.environ.get("GOOGLE_API_KEY")

        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY must be provided, set in config.json, or in environment.")
        
        # Configure client with automatic retries for rate limits (429)
        # The new SDK handles this via HttpRetryOptions
        retry_config = types.HttpRetryOptions(
            attempts=5,
            initial_delay=2.0,
            max_delay=60.0,
            exp_base=2.0,
            http_status_codes=[429, 500, 503]
        )
        
        self.client = genai.Client(
            api_key=self.api_key,
            http_options=types.HttpOptions(retry_options=retry_config)
        )
        self.model = model

    async def process(self, image_path: Path, xmp_path: Optional[Path] = None) -> LightroomSettings:
        prompt = (
            "You are an expert professional photographer and color grader. "
            "Analyze the provided image and suggest Adobe Lightroom develop settings to "
            "make it look stunning, perfectly exposed, and beautifully color-graded. "
            "Output your highly tuned settings in JSON format.\n"
        )
        
        if xmp_path and xmp_path.exists():
            xmp_content = xmp_path.read_text(encoding="utf-8")
            prompt += f"\n\nHere are the current XMP settings for reference (they may be sub-optimal or zeroed):\n```xml\n{xmp_content}\n```\n"

        logger.info(f"Invoking Gemini API ({self.model}) for {image_path.name}")
        
        try:
            # Load the image
            with open(image_path, "rb") as f:
                image_bytes = f.read()
            
            # Prepare image part
            image_part = types.Part.from_bytes(
                data=image_bytes,
                mime_type="image/jpeg" if image_path.suffix.lower() in [".jpg", ".jpeg"] else "image/png"
            )

            # Generate content with structured output
            response = self.client.models.generate_content(
                model=self.model,
                contents=[prompt, image_part],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=LightroomSettings,
                )
            )

            if not response.parsed:
                logger.error(f"Gemini raw response text: {response.text}")
                raise ValueError("Gemini failed to return parsed structured settings.")
                
            return response.parsed
            
        except Exception as e:
            # Log the raw text if possible to help debugging
            if 'response' in locals() and hasattr(response, 'text'):
                logger.error(f"Gemini raw response text on error: {response.text}")
            logger.exception(f"Gemini API Provider error: {e}")
            raise e
