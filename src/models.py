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

    model_config = {
        "json_schema_extra": {
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
    }

class MaskSettings(BaseModel):
    exposure: Optional[float] = None
    contrast: Optional[int] = None
    highlights: Optional[int] = None
    shadows: Optional[int] = None
    whites: Optional[int] = None
    blacks: Optional[int] = None
    texture: Optional[int] = None
    clarity: Optional[int] = None
    dehaze: Optional[int] = None
    vibrance: Optional[int] = None
    saturation: Optional[int] = None
    color_temp: Optional[int] = None
    tint: Optional[int] = None

class Mask(BaseModel):
    type: str = Field(description="E.g. 'Subject Mask', 'Background Mask'")
    creation_instructions: str = Field(description="How to create the mask in Lightroom")
    settings: MaskSettings = Field(description="Settings to apply to the mask")

class PerImageAdjustment(BaseModel):
    image_index: int = Field(description="1-based index of the image")
    settings: LightroomSettings = Field(description="Adjustments differing from global base")

class LightroomResponse(BaseModel):
    clarification_needed: Optional[str] = Field(None, description="Set this if the LLM needs clarification (like missing White Balance)")
    analysis: Optional[str] = Field(None, description="Brief analysis of the photos")
    global_settings: Optional[LightroomSettings] = Field(None, description="Global base settings applied to all images")
    masks: Optional[list[Mask]] = Field(default_factory=list, description="List of masks to apply")
    per_image_adjustments: Optional[list[PerImageAdjustment]] = Field(default_factory=list, description="List of per-image adjustments")
