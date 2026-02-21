import json
import logging
import asyncio
from pathlib import Path
from typing import Optional

from .base import ProviderBase
from ..models import LightroomSettings

logger = logging.getLogger(__name__)

class GeminiCLIProvider(ProviderBase):
    """
    Provider that invokes the `gemini` CLI tool.
    Assumes syntax like: gemini ask "prompt" --image <file>
    """
    def __init__(self, cli_path: str = "gemini"):
        self.cli_path = cli_path

    async def process(self, image_path: Path, xmp_path: Optional[Path] = None) -> LightroomSettings:
        prompt = (
            "You are an expert professional photographer and color grader. "
            "Analyze the provided image and suggest Adobe Lightroom develop settings to "
            "make it look stunning, perfectly exposed, and beautifully color-graded. "
            "You MUST output ONLY valid JSON matching this JSON schema:\n"
            + json.dumps(LightroomSettings.model_json_schema())
        )

        if xmp_path and xmp_path.exists():
            xmp_content = xmp_path.read_text(encoding="utf-8")
            prompt += f"\n\nHere are the current XMP settings for reference (they may be sub-optimal or zeroed):\n{xmp_content}"

        prompt += f"\n\nCRITICAL INSTRUCTION: You MUST evaluate the attached image and output the final JSON immediately. DO NOT use any tools to search files, do not read code. Just look at the image and output the raw JSON!\nImage file: {image_path}"

        # We assume the CLI accepts a prompt and an image file
        # This argument structure might need to be adjusted based on the actual CLI syntax
        cmd = [self.cli_path, "-p", prompt, "--yolo"]

        logger.info(f"Invoking Gemini CLI: {' '.join(cmd)}")

        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()

            if proc.returncode != 0:
                error_msg = stderr.decode().strip()
                logger.error(f"Gemini CLI error: {error_msg}")
                raise RuntimeError(f"Gemini CLI failed: {error_msg}")

            raw_output = stdout.decode().strip()

            # Extract JSON if the model wrapped it in markdown code blocks
            if "```json" in raw_output:
                json_str = raw_output.split("```json")[1].split("```")[0].strip()
            elif "```" in raw_output:
                json_str = raw_output.split("```")[1].split("```")[0].strip()
            else:
                json_str = raw_output

            # Remove any leading/trailing text outside the JSON object
            json_begin = json_str.find('{')
            json_end = json_str.rfind('}')
            if json_begin != -1 and json_end != -1:
                json_str = json_str[json_begin:json_end+1]

            data = json.loads(json_str)
            return LightroomSettings(**data)

        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON from Gemini CLI output: {raw_output}")
            raise e
        except Exception as e:
            logger.exception("Provider error")
            raise e
