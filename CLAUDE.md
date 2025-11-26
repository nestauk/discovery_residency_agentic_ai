# AI Assistant Instructions

This is a portfolio repository for the Nesta AI Agents Residency, containing multiple independent projects.

## Repository Structure

```
discovery_residency_agentic_ai/
├── evals_deep_dive/     # Agent evaluation workshop
├── ...                  # Future projects
```

## Key Principles

- **Each subfolder is independent** - has its own README, pyproject.toml, and potentially its own CLAUDE.md/AGENTS.md (these should be symlinked together)
- **Use `uv`** for dependency management (`uv sync` in each project folder)
- **Check project-specific CLAUDE.md/AGENTS.md** when working in a subfolder for detailed conventions

## Working in This Repo

1. **Identify which project** you're working in
2. **Read that project's README and CLAUDE.md/AGENTS.md** for specific conventions
3. **Stay within the project boundary** - don't mix dependencies across projects

## Common Conventions

- Python formatting: `ruff`
- Package management: `uv`
- Environment variables: `.env` files (gitignored)
- Virtual environments: `.venv/` in each project folder (gitignored)
