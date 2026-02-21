import asyncio
import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

import logging
logging.basicConfig(level=logging.INFO)

from src.providers.gemini_api_provider import GeminiAPIProvider

async def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/test_gemini_direct.py <image_path> [model_name]")
        return

    image_path = Path(sys.argv[1])
    model_name = sys.argv[2] if len(sys.argv) > 2 else None
    if not image_path.exists():
        print(f"Error: {image_path} not found.")
        return

    print(f"Testing Gemini API with image: {image_path}")
    
    # Check for API key
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY environment variable not set.")
        return

    provider = GeminiAPIProvider(api_key=api_key, model=model_name) if model_name else GeminiAPIProvider(api_key=api_key)
    
    try:
        settings = await provider.process(image_path)
        print("\n--- Suggested Lightroom Settings ---")
        print(settings.model_dump_json(indent=2))
        print("------------------------------------\n")
        print("Success!")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
