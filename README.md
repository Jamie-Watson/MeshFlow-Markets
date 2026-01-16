# Solace Agent Mesh Hackathon Quickstart

A hackathon quickstart template for building and deploying [Solace Agent Mesh](https://github.com/SolaceLabs/solace-agent-mesh) (SAM) applications with custom agents.

## Getting Started

1. [Get LLM API access](docs/llm-setup.md) (free options available)
2. Choose a [run method](#run--deploy)
3. Set up [Vibe Coding](docs/vibe-coding.md)
4. Explore the [demo examples](#demo-examples)

## Run & Deploy

| Platform | Guide                                           | When to Use                              |
| -------- | ----------------------------------------------- | ---------------------------------------- |
| Docker   | [Run with Docker](docs/deployment/docker.md)    | Quick start, no Python setup needed      |
| CLI      | [Run with CLI](docs/deployment/cli.md)          | Local dev, faster iteration (no rebuild) |
| Railway  | [Deploy to Railway](docs/deployment/railway.md) | Public deployment, sharing               |

For persistent storage across restarts, see [Persistent Storage with Supabase](docs/persistence.md).

---

## AI-Assisted Development

Pre-configured for [Google Antigravity](https://antigravity.google/), [Gemini CLI](https://github.com/google-gemini/gemini-cli), and [Claude Code](https://claude.ai/code) with [Context7](https://context7.com) for up-to-date SAM docs.

See [Vibe Coding Guide](docs/vibe-coding.md) for setup and known limitations.

## Demo Examples

Agents showing progressive complexity:

| Level    | Agent                                                               | What It Does                                                            |
| -------- | ------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Basic    | [`changelog-basic.yaml`](configs/agents/changelog-basic.yaml)       | Instruction-only, no tools                                              |
| Enriched | [`changelog-enriched.yaml`](configs/agents/changelog-enriched.yaml) | Adds built-in artifact tools to save files                              |
| Advanced | [`changelog-github.yaml`](configs/agents/changelog-github.yaml)     | Custom Python tools ([`git_tools.py`](src/git_tools.py)) for GitHub API |
| Advanced | [`docs-agent.yaml`](configs/agents/docs-agent.yaml)                 | MCP integration (Context7) for live documentation lookup                |

### Demo: Google Antigravity + Changelog GitHub Agent

https://github.com/user-attachments/assets/a699e77f-7796-442e-8684-bf6679422a60

Try: _"Generate a changelog for SolaceLabs/solace-agent-mesh"_ or _"Look up the Next.js App Router docs"_

---

## Resources

- [Solace Agent Mesh Documentation](https://solacelabs.github.io/solace-agent-mesh/docs/documentation/getting-started/introduction/)
