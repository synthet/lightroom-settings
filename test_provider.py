import asyncio
from pathlib import Path
from src.providers.gemini_cli import GeminiCLIProvider

async def main():
    provider = GeminiCLIProvider(cli_path="gemini.cmd")
    image_path = Path("D:/Projects/lightroom-mcp/preview_tests/DSC_5498.NEF")
    print(f"Analyzing {image_path}...")
    try:
        result = await provider.process(image_path)
        print("Success:", result)
    except Exception as e:
        print("Error:", e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
