import pytest
from src.core.parser import extract_json_from_text, parse_llm_response
from src.models import LightroomResponse

def test_extract_json_from_text_with_markdown():
    text = """Here is your response:
```json
{"global_settings": {"exposure": 0.5}}
```
Enjoy!"""
    json_str = extract_json_from_text(text)
    assert json_str == '{"global_settings": {"exposure": 0.5}}'

def test_extract_json_from_text_raw():
    text = '{"global_settings": {"exposure": 0.5}}'
    json_str = extract_json_from_text(text)
    assert json_str == '{"global_settings": {"exposure": 0.5}}'

def test_parse_llm_response_valid():
    text = """
    ```json
    {
      "analysis": "Great photo.",
      "global_settings": {
        "exposure": 0.30,
        "contrast": -5,
        "highlights": -35,
        "shadows": 25,
        "whites": 10,
        "blacks": -12,
        "color_temp": 5500,
        "tint": 5,
        "vibrance": 10,
        "saturation": -2,
        "texture": 15,
        "clarity": 10,
        "dehaze": 0,
        "sharpening": 40,
        "noise_reduction_luminance": 15
      },
      "masks": [
        {
          "type": "Subject Mask",
          "creation_instructions": "Select Subject",
          "settings": {
            "exposure": 0.1,
            "texture": 15
          }
        }
      ],
      "per_image_adjustments": []
    }
    ```
    """
    response = parse_llm_response(text)
    assert isinstance(response, LightroomResponse)
    assert response.analysis == "Great photo."
    assert response.global_settings is not None
    assert response.global_settings.exposure == 0.30
    assert response.global_settings.contrast == -5
    assert len(response.masks) == 1
    assert response.masks[0].type == "Subject Mask"
    assert response.masks[0].settings.texture == 15
    assert len(response.per_image_adjustments) == 0

def test_parse_llm_response_invalid_json():
    with pytest.raises(ValueError, match="Failed to decode JSON"):
        parse_llm_response("Not JSON at all")

def test_parse_llm_response_invalid_schema():
    with pytest.raises(ValueError, match="Failed to validate data"):
        parse_llm_response('{"global_settings": "Not an object"}')
