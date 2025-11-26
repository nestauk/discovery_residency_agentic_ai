# Evaluating AI Agents: A Hands-On Workshop

A practical workshop for learning how to design evaluations for AI agents, covering objective metrics, LLM-as-judge patterns, and human review workflows.

## Why This Matters

Evaluating AI agents is harder than evaluating traditional software - there's no simple "expected output" to compare against. This workshop provides a practical framework for thinking about agent evaluation across two dimensions:
- **Objective vs Subjective**: Can we measure it automatically, or do we need judgment?
- **With vs Without Ground Truth**: Do we know the "right" answer?

## Key Takeaways

- How to design **objective evaluations** (SQL correctness, domain checks, keyword coverage)
- When and how to use **LLM-as-judge** patterns with structured rubrics
- Integrating **human review** into evaluation pipelines
- Building **composite evaluation pipelines** that combine multiple approaches

## Technologies

`Python` `OpenAI` `DuckDB` `Tavily Search` `aisuite` `JupyterLab`

---

## Overview

This workshop teaches **component-level evaluation** of AI agents through two example agents:

1. **SQL Agent** - Answers questions about a product nutrition database using natural language → SQL
2. **Research Agent** - Searches the web, academic papers, and Wikipedia to research topics

## The Evaluation Framework

Evaluations are organised along two axes:

|                | With Ground Truth | Without Ground Truth |
|----------------|-------------------|----------------------|
| **Objective**  | SQL result matching | Query executes, no errors |
| **Subjective** | LLM-as-judge with rubric | Human quality rating |

## Project Structure

```
workshop.ipynb          # Main workshop notebook - start here!
tools/                  # Agent capabilities
   sql_tools.py         # SQL execution (DuckDB)
   research_tools.py    # Web search (Tavily, arXiv, Wikipedia)
utils/                  # Utility modules
   helpers.py           # Tool wrappers, text processing
   display.py           # Jupyter display functions
   evaluators.py        # Evaluation logic (LLM-as-judge, ground truth)
assets/                 # Supporting materials
   two-axes-of-evaluation.png
.env.example            # Environment variables template
```

## Setup

### 1. Install dependencies

```bash
uv sync
```

### 2. Configure environment

Copy `.env.example` to `.env` and fill in the API keys:

```bash
cp .env.example .env
```

Required keys:
- `OPENAI_API_KEY` - OpenAI API key
- `TAVILY_API_KEY` - Tavily search API key

### 3. Run the workshop

```bash
uv run jupyter lab workshop.ipynb
```

## Workshop Sections

1. **SQL Agent** - Objective evaluation with ground truth
2. **Research Agent** - Tool-using agent introduction
3. **Objective Evaluations** - Domain checks, keyword coverage
4. **LLM-as-Judge** - Rubric-based subjective scoring
5. **Human Review** - Structured human feedback patterns
6. **Combined Pipeline** - Putting it all together

## Key Utilities

### `make_verbose_tool(tool_func, name)`
Wraps a tool to print arguments and results (useful for seeing SQL queries).

### `evaluate_sql_result(actual, expected, comparison)`
Objective evaluation comparing agent output to ground truth.

### `evaluate_tavily_results(domains, output, min_ratio)`
Checks if research sources come from trusted domains.

### `llm_judge(output, rubric)`
Uses another LLM to score output against a multi-dimension rubric.

### `check_keywords(output, keywords, min_ratio)`
Verifies expected keywords appear in output.

## Dependencies

- **aisuite** - Unified LLM client abstraction
- **duckdb** - In-memory SQL database
- **tavily** - Web search API
- **wikipedia** - Wikipedia summaries
- **jupyterlab-rise** - Presentation mode for notebooks
