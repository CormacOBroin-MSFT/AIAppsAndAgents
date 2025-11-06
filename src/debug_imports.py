#!/usr/bin/env python3
import sys

# Add debug output for imports
print("Starting imports...")

try:
    print("Importing standard libraries...")
    import asyncio
    import logging
    import os
    from collections.abc import AsyncIterable
    from enum import Enum
    from typing import TYPE_CHECKING, Annotated, Any, Literal
    print("Standard libraries imported successfully")

    print("Importing httpx...")
    import httpx
    print("httpx imported successfully")

    print("Importing openai...")
    import openai
    print("openai imported successfully")

    print("Importing Azure identity...")
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    print("Azure identity imported successfully")

    print("Importing dotenv...")
    from dotenv import load_dotenv
    print("dotenv imported successfully")

    print("Importing pydantic...")
    from pydantic import BaseModel
    print("pydantic imported successfully")

    print("Importing semantic kernel agents...")
    from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
    print("semantic kernel agents imported successfully")

    print("Importing semantic kernel connectors...")
    from semantic_kernel.connectors.ai.open_ai import (
        AzureChatCompletion,
        OpenAIChatCompletion,
        OpenAIChatPromptExecutionSettings,
    )
    print("semantic kernel connectors imported successfully")

    print("Importing semantic kernel contents...")
    from semantic_kernel.contents import (
        FunctionCallContent,
        FunctionResultContent,
        StreamingChatMessageContent,
        StreamingTextContent,
    )
    print("semantic kernel contents imported successfully")

    print("Importing semantic kernel functions...")
    from semantic_kernel.functions import KernelArguments, kernel_function
    print("semantic kernel functions imported successfully")

    print("All imports successful - now loading the actual module...")

    # Now import the actual module
    import a2a.agent.product_management_agent as pm_module
    print(f"Module loaded, attributes: {dir(pm_module)}")

except Exception as e:
    print(f"Error during import: {e}")
    import traceback
    traceback.print_exc()
