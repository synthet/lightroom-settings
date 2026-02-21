import os
import time
import base64
import httpx
import logging
from typing import Any, Dict, Optional, List
from pathlib import Path

from .models import LightroomSettings

logger = logging.getLogger(__name__)

BROKER_URL = os.environ.get("LRC_BROKER_URL", "http://127.0.0.1:8085")

class LightroomMCPClient:
    """
    Client for interacting with the Lightroom MCP Broker.
    Provides methods to fetch current selection, get image previews,
    and apply new develop settings.
    """
    
    def __init__(self, broker_url: str = BROKER_URL):
        self.broker_url = broker_url
        self._request_id = 0
        self.client = httpx.AsyncClient(timeout=30.0)
        
    async def send_command(self, method: str, params: Optional[Dict[str, Any]] = None) -> Any:
        self._request_id += 1
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
            "id": self._request_id
        }

        try:
            response = await self.client.post(
                f"{self.broker_url}/request",
                json=request
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to communicate with Lightroom Broker: {e}")
            raise e

    async def get_selected_photos(self) -> List[Dict[str, Any]]:
        """Return metadata for currently selected photos."""
        res = await self.send_command("get_selection")
        if "photos" in res:
            return res["photos"]
        return []

    async def get_photo_preview(self, photo_id: Optional[str] = None) -> Optional[bytes]:
        """Fetch a JPEG preview of a photo. Defaults to current selection."""
        params = {"width": 1024, "height": 1024}
        if photo_id:
            params["photo_id"] = photo_id
            
        res = await self.send_command("get_photo_preview", params)
        if "photos" in res and len(res["photos"]) > 0:
            b64_str = res["photos"][0].get("jpegBase64")
            if b64_str:
                return base64.b64decode(b64_str)
        return None

    async def apply_develop_settings(self, settings: LightroomSettings) -> str:
        """Apply a LightroomSettings object directly to Lightroom."""
        # Convert our model names to Lightroom SDK parameter names
        mapping = {
            "exposure": "Exposure2012",
            "contrast": "Contrast2012",
            "highlights": "Highlights2012",
            "shadows": "Shadows2012",
            "whites": "Whites2012",
            "blacks": "Blacks2012",
            "texture": "Texture",
            "clarity": "Clarity2012",
            "dehaze": "Dehaze",
            "vibrance": "Vibrance",
            "saturation": "Saturation",
            "color_temp": "Temperature",
            "tint": "Tint",
        }
        
        lrc_settings = {}
        for field, crs_attr in mapping.items():
            val = getattr(settings, field)
            if val is not None:
                lrc_settings[crs_attr] = val
                
        if not lrc_settings:
            return "No settings to apply"

        res = await self.send_command("set_develop_settings", {"settings": lrc_settings})
        return str(res)
