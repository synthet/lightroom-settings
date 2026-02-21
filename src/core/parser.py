import json
import re
from typing import Dict, Any

from src.models import LightroomResponse

def extract_json_from_text(text: str) -> str:
    """
    Extracts JSON from a string that might be wrapped in ```json ... ``` markdown blocks.
    """
    # Attempt to find a ```json block
    match = re.search(r'```(?:json)?\s*(.*?)\s*```', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # Otherwise attempt to find the first { and last }
    start_idx = text.find('{')
    end_idx = text.rfind('}')
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        return text[start_idx:end_idx + 1]
        
    return text.strip()

def parse_llm_response(text: str) -> LightroomResponse:
    """
    Parses the raw text output from the LLM into a validated LightroomResponse object.
    
    Args:
        text (str): The raw string output from the LLM (could include markdown).
        
    Returns:
        LightroomResponse: A validated pedantic model.
        
    Raises:
        ValueError: If JSON cannot be parsed or validation fails.
    """
    json_str = extract_json_from_text(text)
    
    try:
        data: Dict[str, Any] = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to decode JSON from LLM response: {e}\nExtracted string:\n{json_str}")
        
    try:
        # Use Pydantic's validation to instantiatate the nested model
        return LightroomResponse.model_validate(data)
    except Exception as e:
        raise ValueError(f"Failed to validate data against LightroomResponse schema: {e}")
