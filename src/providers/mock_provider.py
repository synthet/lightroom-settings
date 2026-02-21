import asyncio
import logging
from pathlib import Path
from typing import Optional

from .base import ProviderBase
from ..models import LightroomSettings

logger = logging.getLogger(__name__)

class MockProvider(ProviderBase):
    """
    Mock provider for testing the MCP flow without needing API keys.
    Returns hardcoded Lightroom settings.
    """
    async def process(self, image_path: Path, xmp_path: Optional[Path] = None) -> LightroomSettings:
        logger.info(f"Mock analyzing image: {image_path}")
        await asyncio.sleep(1) # Simulate some processing time

        return LightroomSettings(
            Exposure=0.35,
            Contrast=15,
            Highlights=-20,
            Shadows=10,
            Whites=5,
            Blacks=-5,
            Clarity=10,
            Vibrance=15,
            Saturation=5
        )
