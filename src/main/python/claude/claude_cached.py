#!/usr/bin/env -S poetry run python

import asyncio
import json
import os
from typing import ClassVar

import boto3
from botocore.response import StreamingBody
import dotenv
import uvicorn
import uvloop
import anthropic
from main.python.claude.claude import REGION_NAME
import traceback


class AnthropicClient:
    REGION_NAME: ClassVar[str] = "us-east-1"

    def __init__(self) -> None:
        dotenv.load_dotenv("/app/.env")
        self.region = REGION_NAME
        # Initialize Anthropic client with an API key from .env file
        self.anthropic_client = anthropic.AsyncAnthropicBedrock(
            aws_secret_key=os.getenv("AWS_SECRET_KEY"),
            aws_access_key=os.getenv("AWS_ACCESS_KEY"),
            aws_region=REGION_NAME,
        )

    async def call_claude_anthropic(self, prompt: str) -> str:
        result: str = ""

        try:
            message = await self.anthropic_client.messages.create(
                model="anthropic.claude-3-haiku-20240307-v1:0",
                max_tokens=12,
                messages=[{"role": "user", "content": prompt}],
            )
            print(message.content)

        except Exception as e:
            print(f"ERROR: {e}")
            traceback.print_exc()

        return result


class Client:
    cli: ClassVar[AnthropicClient] = AnthropicClient()


async def main() -> None:

    # Call the model and print the result
    result = await Client.cli.call_claude_anthropic("What is the capital of France?")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
