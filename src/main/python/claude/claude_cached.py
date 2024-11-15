#!/usr/bin/env -S poetry run python

import asyncio
import json
import os
import time
import traceback
from typing import ClassVar

import anthropic
from anthropic.types.message import Message
import dotenv
import uvicorn
import uvloop
import vcr  # type:ignore


class AnthropicClient:
    REGION_NAME: ClassVar[str] = "us-east-1"

    def __init__(self) -> None:
        dotenv.load_dotenv("/app/.env")
        self.region = self.REGION_NAME
        # Initialize Anthropic client with an API key from .env file
        self.anthropic_client = anthropic.AsyncAnthropicBedrock(
            aws_secret_key=os.getenv("AWS_SECRET_KEY"),
            aws_access_key=os.getenv("AWS_ACCESS_KEY"),
            aws_region=self.REGION_NAME,
        )

    @vcr.use_cassette(
        "/tmp/cassettes/claude_responses.yml",
        match_on=["uri", "body"],
        record_mode=vcr.record_mode.RecordMode.NEW_EPISODES,
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


def took_ms(start_ns: int) -> int:
    return (time.time_ns() - start_ns) // 1_000_000


async def main() -> None:
    for _ in range(10):
        start: int = time.time_ns()
        result = await Client.cli.call_claude_anthropic("What is the capital of Italy?")
        print(result, took_ms(start), "ms")
        start = time.time_ns()
        result = await Client.cli.call_claude_anthropic(
            "What is the capital of Germany?"
        )
        print(result, took_ms(start), "ms")


if __name__ == "__main__":
    asyncio.run(main())
