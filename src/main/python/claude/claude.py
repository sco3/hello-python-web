#!/usr/bin/env -S poetry run python

import uvicorn
import asyncio
import uvloop

import boto3
import json
import dotenv
import os
from botocore.response import StreamingBody
from typing import ClassVar

REGION_NAME: str = "us-east-1"


class BedrockClient:
    def __init__(self) -> None:
        dotenv.load_dotenv("/app/.env")
        # Initialize Bedrock client using boto3
        self.bedrock_client = boto3.client(
            "bedrock-runtime",
            region_name=REGION_NAME,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),  # Use None as default
            aws_secret_access_key=os.getenv(
                "AWS_SECRET_ACCESS_KEY"
            ),  # Use None as default
        )

    def call_claude_bedrock(self, prompt: str) -> str:
        result: str = ""
        try:
            model_id: str = "anthropic.claude-3-haiku-20240307-v1:0"

            data: dict = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 512,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0,
                "top_p": 0,
            }

            request: str = json.dumps(data)

            response: dict = self.bedrock_client.invoke_model(
                modelId=model_id, body=request
            )
            response_body_stream: StreamingBody = response["body"]
            response_data: str = response_body_stream.read().decode("utf-8")
            out_data: dict = json.loads(response_data)
            for item in out_data.get("content", []):
                text: str = item.get("text", "")
                # print(text)
                result += text + " "

        except Exception as e:
            print(f"ERROR: {e}")

        return result


class AnthropicClient:
    def __init__(self) -> None:
        dotenv.load_dotenv("/app/.env")
        self.region = REGION_NAME
        # Initialize Anthropic client with an API key from .env file
        self.anthropic_client = AnthropicApiClient(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

    def call_claude_anthropic(self, prompt: str, max_tokens: int = 512) -> str:
        result: str = ""
        try:
            # Log or handle region-specific actions (if needed)
            print(f"Using Anthropic API in region: {self.region}")

            # Request to Anthropic Claude
            response = self.anthropic_client.completions.create(
                model="claude-3",  # or your preferred Claude model
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
            )

            # Process the response to extract the content
            result = response.completion

        except Exception as e:
            print(f"ERROR: {e}")

        return result


class Client:
    client: ClassVar[BedrockClient] = BedrockClient()


def main() -> None:
    # Call the model and print the result
    result = Client.client.call_claude_bedrock("What is the capital of France?")
    print(result)
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    uvicorn.run(
        "claude:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="error",
    )


async def app(scope, receive, send):
    assert scope["type"] == "http"
    path: str = scope.get("path", "/")
    status: int = 200
    result: str = "ok"
    try:
        result = Client.client.call_claude_bedrock("What is the capital of France?")
    except Exception as e:
        status = 500
        result = str(e)

    await send(
        {
            "type": "http.response.start",
            "status": status,
            "headers": [
                [b"content-type", b"text/plain"],
            ],
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": result.encode(),
        }
    )


if __name__ == "__main__":
    main()
