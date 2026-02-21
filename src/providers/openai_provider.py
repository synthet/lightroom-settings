import json
import logging
import base64
from pathlib import Path
from typing import Optional

from pydantic import ValidationError
from openai import AsyncOpenAI

from .base import ProviderBase
from ..models import LightroomSettings

logger = logging.getLogger(__name__)

class OpenAIProvider(ProviderBase):
    """
    Provider that invokes the OpenAI API directly (using gpt-4o for vision).
    Requires OPENAI_API_KEY environment variable.
    """
    def __init__(self, api_key: Optional[str] = None):
        # AsyncOpenAI falls back to OPENAI_API_KEY env var if api_key is None
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = "gpt-4o"

    async def process(self, image_path: Path, xmp_path: Optional[Path] = None) -> LightroomSettings:
        prompt = (
            "You are an expert professional photographer and color grader. "
            "Analyze the provided image and suggest Adobe Lightroom develop settings to "
            "make it look stunning, perfectly exposed, and beautifully color-graded. "
            "Output your highly tuned settings. Focus on bringing out the best light, contrast, and color mood.\n"
        )
        
        if xmp_path and xmp_path.exists():
            xmp_content = xmp_path.read_text(encoding="utf-8")
            prompt += f"\n\nHere are the current XMP settings for reference (they may be sub-optimal or zeroed):\n```xml\n{xmp_content}\n```\n"

        # Read and encode image
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            
        mime_type = "image/jpeg"
        if image_path.suffix.lower() == ".png":
            mime_type = "image/png"

        messages = [
            {
                "role": "system",
                "content": "You are a professional Lightroom master editor."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
        
        logger.info(f"Invoking OpenAI API ({self.model})")
        
        try:
            # We use Structured Outputs via response_format parsing
            completion = await self.client.beta.chat.completions.parse(
                model=self.model,
                messages=messages,
                response_format=LightroomSettings,
            )
            
            settings = completion.choices[0].message.parsed
            if not settings:
                raise ValueError("OpenAI failed to return structured settings.")
                
            return settings
            
        except ValidationError as e:
            logger.error(f"Failed to parse OpenAPI JSON structure: {e}")
            raise e
        except Exception as e:
            logger.exception("OpenAI Provider error")
            raise e
