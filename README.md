# Agentic AI Residency Portfolio

A collection of projects exploring agentic AI systems, developed during my [AI Agents Residency](https://www.nesta.org.uk/project-updates/nesta-welcomes-ai-agents-resident/) at [Nesta](https://www.nesta.org.uk/).

## About the Residency

This residency focuses on [showing the practical value of agentic AI for driving impact](https://www.nesta.org.uk/project/showing-the-practical-value-of-agentic-ai-for-driving-impact/), with a specific application to [challenges facing heat pump installers with DNO applications](https://www.nesta.org.uk/project-updates/the-challenges-of-distribution-network-operator-applications-for-heat-pump-installers/).

## Projects

| Project | Description | Key Topics |
|---------|-------------|------------|
| [Evaluating AI Agents](./discovery_residency_agentic_ai/evals_deep_dive/) | Hands-on workshop on designing evaluations for AI agents | LLM-as-judge, objective metrics, human review |

## Repository Structure

Each project is self-contained with its own:
- `README.md` - Project overview and setup instructions
- `pyproject.toml` - Dependencies (install with `uv sync`)
- Environment requirements (`.env.example` where needed)

```
discovery_residency_agentic_ai/
├── evals_deep_dive/     # Agent evaluation workshop
├── ...                  # Future projects
```

## Quick Start

Navigate to a project folder and follow its README:

```bash
cd discovery_residency_agentic_ai/evals_deep_dive
uv sync
# Follow project-specific setup...
```

## Tools

This repository uses:
- [`uv`](https://docs.astral.sh/uv/) - Fast Python package manager
- [`direnv`](https://direnv.net/) - Automatic environment variable loading (optional)

---

<small><p>Project based on <a target="_blank" href="https://github.com/nestauk/ds-cookiecutter">Nesta's data science project template</a>
(<a href="http://nestauk.github.io/ds-cookiecutter">Read the docs here</a>).
</small>
