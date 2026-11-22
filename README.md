# Token Budget Router

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![AI Skill](https://img.shields.io/badge/AI-Skill-0f766e)](https://github.com/qasimrazamalik-coder/token-budget-router)

> Agent stacks overspend by routing every step to a frontier model without measuring task complexity.

Provider-neutral AI skill for Claude Code, Codex, ChatGPT, Claude, Gemini, Grok and custom agent runtimes. It combines concise agent instructions with a deterministic Python execution path.

## Quick answer

**Token Budget Router** is an open-source, provider-neutral AI agent skill that route AI tasks across model classes and context strategies using explicit quality, latency, privacy and token-cost constraints. Use when an agent system needs a deterministic model-selection plan instead of always choosing the largest model. It runs locally, requires no API key, and works with Claude Code, Codex, ChatGPT, Gemini, Grok, MCP-compatible agents, and custom runtimes.

## What it does

Route AI tasks across model classes and context strategies using explicit quality, latency, privacy and token-cost constraints. Use when an agent system needs a deterministic model-selection plan instead of always choosing the largest model.

## Architecture

```text
User/Agent → SKILL.md → input contract → deterministic runner → validated JSON result
```

## Install

Copy `skill/` into your agent's skills directory, or reference `skill/SKILL.md` from an agent configuration. No API key or network access is required.

## Demo

```bash
python skill/scripts/run.py examples/input.json --mode router
pytest -q
```

![Workflow preview](assets/workflow-preview.svg)

## Compatibility

| Runtime | Method |
|---|---|
| Codex / ChatGPT | Install or reference `skill/` |
| Claude Code | Add `skill/SKILL.md` to project instructions or a command wrapper |
| Gemini / Grok | Supply `SKILL.md` as system/project context and expose the runner as a tool |
| MCP agents | Wrap the runner as a stdio tool with the documented JSON contract |

## Safety

See [SECURITY.md](SECURITY.md) and [docs/GUARDRAILS.md](docs/GUARDRAILS.md). The skill does not bypass access controls or transmit input data.

## Common questions

### What is Token Budget Router?

Route AI tasks across model classes and context strategies using explicit quality, latency, privacy and token-cost constraints. Use when an agent system needs a deterministic model-selection plan instead of always choosing the largest model.

### Which AI tools can use it?

Claude Code, Codex, ChatGPT, Gemini, Grok, MCP-compatible agents, and custom agent runtimes can use the instructions and deterministic runner.

### Does it require an API key or cloud service?

No. The reference workflow runs locally with Python and uses no external dependency or network call.

### Is commercial use allowed?

Yes. The project is released under the permissive [MIT License](LICENSE), including commercial use, modification, and redistribution subject to the license notice.

### Where are the installation and safety instructions?

See [Installation](docs/INSTALLATION.md), [Guardrails](docs/GUARDRAILS.md), and [Security](SECURITY.md).

## Discovery keywords

token, budget, router, AI agent skill, agentic workflow, Claude Code skill, Codex skill, ChatGPT skill, Gemini skill, Grok skill, MCP, Python automation, open source AI tooling

## License

MIT © 2026 Qasim Raza Malik. See [LICENSE](LICENSE).
