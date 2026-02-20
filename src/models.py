from pydantic import BaseModel, Field
from typing import Optional

class LightroomSettings(BaseModel):
    # Basic Tone
    exposure: Optional[float] = Field(None, description="Exposure2012 (e.g. -5.0 to 5.0)")
    contrast: Optional[int] = Field(None, description="Contrast2012 (e.g. -100 to 100)")
    highlights: Optional[int] = Field(None, description="Highlights2012 (e.g. -100 to 100)")
    shadows: Optional[int] = Field(None, description="Shadows2012 (e.g. -100 to 100)")
    whites: Optional[int] = Field(None, description="Whites2012 (e.g. -100 to 100)")
    blacks: Optional[int] = Field(None, description="Blacks2012 (e.g. -100 to 100)")
    
    # Presence
    texture: Optional[int] = Field(None, description="Texture (e.g. -100 to 100)")
    clarity: Optional[int] = Field(None, description="Clarity2012 (e.g. -100 to 100)")
    dehaze: Optional[int] = Field(None, description="Dehaze (e.g. -100 to 100)")
    vibrance: Optional[int] = Field(None, description="Vibrance (e.g. -100 to 100)")
    saturation: Optional[int] = Field(None, description="Saturation (e.g. -100 to 100)")
    
    # Color
    color_temp: Optional[int] = Field(None, description="Temperature (e.g. 2000 to 50000)")
    tint: Optional[int] = Field(None, description="Tint (e.g. -150 to 150)")

    class Config:
        json_schema_extra = {
            "example": {
                "exposure": 0.5,
                "contrast": 10,
                "highlights": -20,
                "shadows": 30,
                "whites": 15,
                "blacks": -10,
                "color_temp": 5500,
                "tint": 5
            }
        }
