"""
Evaluation functions for assessing agent outputs.
"""
import json
from typing import Any

from aisuite import Client

from .helpers import clean_json_block


# Shared client for LLM-as-judge evaluations
_judge_client = Client()


def llm_judge(
    prompt: str,
    rubric: dict[str, str],
    model: str = "azure:gpt-5-mini",
) -> dict[str, Any]:
    """
    Use an LLM to evaluate output against a rubric with multiple dimensions.

    This is a "LLM-as-judge" evaluation where another LLM scores the output
    on subjective criteria that are hard to check with code.

    Args:
        prompt: The full prompt to send to the judge LLM
        rubric: Dict mapping dimension names to descriptions (used for parsing)
        model: The LLM model to use as judge

    Returns:
        Dict with scores and explanations:
        {
            "scores": {"relevance": 4, "recency": 3, ...},
            "explanations": {"relevance": "The sources are...", ...},
            "overall": 3.5,  # average score
            "raw_response": "..."  # the judge's full response
        }
    """

    try:
        response = _judge_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.choices[0].message.content

        # Parse JSON from response
        cleaned = clean_json_block(raw)
        result = json.loads(cleaned)

        # Calculate overall average
        scores = result.get("scores", {})
        overall = sum(scores.values()) / len(scores) if scores else 0

        return {
            "scores": scores,
            "explanations": result.get("explanations", {}),
            "overall": round(overall, 2),
            "raw_response": raw
        }

    except json.JSONDecodeError as e:
        return {
            "scores": {},
            "explanations": {},
            "overall": 0,
            "raw_response": raw,
            "error": f"Failed to parse JSON: {e}"
        }
    except Exception as e:
        return {
            "scores": {},
            "explanations": {},
            "overall": 0,
            "raw_response": "",
            "error": str(e)
        }


def evaluate_sql_result(actual: Any, expected: Any, comparison: str = "exact") -> tuple[bool, str]:
    """
    Evaluate SQL query result against expected ground truth.

    This is an objective evaluation with ground truth - we know the exact answer
    and check if the agent's response matches.

    Args:
        actual: The result from the SQL agent (usually a string answer)
        expected: The expected ground truth value
        comparison: "exact" for exact match, "contains" for substring match

    Returns:
        tuple[bool, str]: (passed, markdown_report)
    """
    actual_str = str(actual) if actual is not None else ""
    expected_str = str(expected)

    if comparison == "exact":
        passed = actual_str.strip() == expected_str.strip()
    elif comparison == "contains":
        passed = expected_str.lower() in actual_str.lower()
    else:
        passed = actual_str == expected_str

    status = "PASS" if passed else "FAIL"
    report = f"""
### Evaluation - SQL Result (Ground Truth)
- Status: **{status}**
- Comparison: {comparison}

**Expected:** `{expected}`

**Actual:** `{actual}`
"""
    return passed, report
