"""
Pure utility functions for tool wrapping and text processing.
"""
import functools
import os
import re
from typing import Callable


def check_api_keys() -> str | None:
    """
    Validate that required API keys are set and provide guidance if missing.

    Returns:
        The model string to use (e.g., "openai:gpt-5-mini"), or None if keys missing.
    """
    issues = []
    model = None

    # Check Tavily API key (for web search)
    tavily_key = os.getenv("TAVILY_API_KEY")
    if not tavily_key:
        issues.append("""
❌ **TAVILY_API_KEY** not found
   → Get a free API key at: https://tavily.com
""")
    else:
        print("✅ TAVILY_API_KEY found")

    # Check LLM provider (Azure preferred, OpenAI as fallback)
    azure_key = os.getenv("AZURE_API_KEY")
    azure_url = os.getenv("AZURE_BASE_URL")
    openai_key = os.getenv("OPENAI_API_KEY")

    if azure_key and azure_url:
        model = "azure:gpt-5-mini"
        print(f"✅ AZURE keys found → using {model}")
    elif openai_key:
        model = "openai:gpt-5-mini"
        print(f"✅ OPENAI_API_KEY found → using {model}")
    else:
        issues.append("""
❌ **No LLM provider configured**
   → Option 1: Set AZURE_API_KEY + AZURE_BASE_URL (ask Simon)
   → Option 2: Set OPENAI_API_KEY (get at https://platform.openai.com/api-keys)
""")

    if issues:
        print("\n" + "="*60)
        print("⚠️  MISSING API KEYS - Please fix before continuing")
        print("="*60)
        for issue in issues:
            print(issue)
        print("""
📝 **Setup Instructions:**
1. Copy .env.example to .env:  cp .env.example .env
2. Edit .env and add your API keys
3. Restart the kernel and run this cell again
""")
        return None

    print("\n✅ All API keys configured! You're ready to go.")
    return model


def make_verbose_tool(tool_func: Callable, name: str) -> Callable:
    """
    Wrap a tool to print progress and arguments when it's called.

    This is useful for debugging and demonstrating what the agent is doing.
    For SQL tools, it will print the query being executed.

    Args:
        tool_func: The tool function to wrap
        name: A display name for the tool (e.g., "database", "web")

    Returns:
        Wrapped function that prints before/after execution
    """
    @functools.wraps(tool_func)
    def wrapper(*args, **kwargs):
        print(f"  [{name}] Calling tool...")

        # Print the arguments (useful for seeing SQL queries, search terms, etc.)
        if args:
            for i, arg in enumerate(args):
                arg_str = str(arg)
                # Truncate long arguments but show SQL queries in full
                if len(arg_str) > 200 and "SELECT" not in arg_str.upper():
                    arg_str = arg_str[:200] + "..."
                print(f"  [{name}] arg[{i}]: {arg_str}")
        if kwargs:
            for key, val in kwargs.items():
                val_str = str(val)
                if len(val_str) > 200 and "SELECT" not in val_str.upper():
                    val_str = val_str[:200] + "..."
                print(f"  [{name}] {key}: {val_str}")

        result = tool_func(*args, **kwargs)

        # Print result summary
        if isinstance(result, list):
            print(f"  [{name}] Returned {len(result)} results")
        else:
            print(f"  [{name}] Done")

        return result
    return wrapper


def clean_json_block(raw: str) -> str:
    """
    Extract JSON from a markdown code block if present.

    Args:
        raw: Raw string that may contain ```json ... ``` wrapper

    Returns:
        Cleaned JSON string
    """
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\n?", "", raw)
        raw = re.sub(r"\n?```$", "", raw)
    return raw.strip()
