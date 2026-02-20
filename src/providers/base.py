from abc import ABC, abstractmethod
from typing import Optional
from pathlib import Path

from ..models import LightroomSettings

class ProviderBase(ABC):
    """
    Abstract base class for all AI providers.
    A provider takes an image path and optional XMP path,
    and returns suggested Lightroom settings.
    """
    
    @abstractmethod
    async def process(self, image_path: Path, xmp_path: Optional[Path] = None) -> LightroomSettings:
        """
        Analyze the image and optionally its current XMP settings,
        and return suggested new settings.
        
        Args:
            image_path: Path to the image file.
            xmp_path: Path to the existing XMP sidecar file (if any).
        
        Returns:
            A LightroomSettings object with the suggested values.
        """
        pass
