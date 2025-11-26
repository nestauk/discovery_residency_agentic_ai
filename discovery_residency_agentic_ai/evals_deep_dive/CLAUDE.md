# AI Assistant Instructions

This is a workshop project for teaching AI agent evaluation patterns.

## Project Context

- **Purpose**: Hands-on workshop teaching evaluation design for AI agents
- **Primary file**: `workshop.ipynb` - the main workshop notebook
- **Audience**: Data scientists learning to evaluate agentic AI systems

## Architecture

### Agents
- **SQL Agent**: Natural language → SQL → answer (in `workshop.ipynb`)
- **Research Agent**: Orchestrates web/academic search tools (in `workshop.ipynb`)

### Tools (`tools/`)
- `sql_tools.py` - DuckDB query execution
- `research_tools.py` - Tavily, arXiv, Wikipedia search

### Utilities (`utils/`)
- `helpers.py` - Tool wrappers (`make_verbose_tool`), text processing (`clean_json_block`)
- `display.py` - Jupyter display functions (`print_html`, `display_rubric_scores`, `display_test_results`)
- `evaluators.py` - Evaluation logic (`llm_judge`, `evaluate_sql_result`)

## Conventions

### Adding New Tools
Follow the pattern in `tools/research_tools.py`:
```python
def my_tool(param: str) -> list[dict]:
    """Execute operation, return structured result."""
    ...
    return results

my_tool_def = {
    "type": "function",
    "function": {
        "name": "my_tool",
        "description": "...",
        "parameters": {...}
    }
}
```

### Adding New Evaluations
Follow the pattern in `utils/evaluators.py`:
```python
def evaluate_X(output, criteria) -> tuple[bool, str]:
    """Check output against criteria."""
    passed = ...
    report = f"### Evaluation\n..."
    return passed, report
```

### Notebook Cells
- Use markdown headers with `---` separators between sections
- Code cells should have clear `# ===` section headers
- Use `print_html()` for styled output display

## LLM Configuration

- Default model: `openai:gpt-5-mini`
- Client: `aisuite.Client()` (initialized in setup cell)
- Tool calling: `tool_choice="auto"`, `max_turns=N`

## Testing Changes

After modifying code, restart the kernel and run all cells in `workshop.ipynb` to verify:
1. Setup cell runs without errors
2. SQL agent test cases pass (at least 2/3)
3. Research agent returns results with URLs
4. All evaluation functions return `(bool, str)` tuples

## Environment

Requires `.env` with:
- `OPENAI_API_KEY`
- `TAVILY_API_KEY`
