# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`opik-for-ob` — 基于 Comet Opik 的 LLM 可观测性实验项目。尚未初始化。

## Conventions (from sibling project `gen3deval-replication`)

- **Python**: >=3.11, <3.13
- **Package manager**: `uv` (uv sync, uv run)
- **Linter**: `ruff` (line-length=100, target-version="py311")
- **SDK**: `opik>=1.0.0` — LLM 评估与可观测性 SDK
  - `opik.configure(url_override=..., use_local=True, workspace=...)`
  - `opik.Opik(project_name=..., workspace=..., host=...)`
  - `client.trace(...)` / `trace.span(...)` / `span.end()` / `trace.end()`
  - `client.log_traces_feedback_scores(...)`
  - `client.end(timeout=30, flush=True)`
- **Local Opik stack**: Docker Compose (MySQL 8.4, Redis 7.2, ClickHouse, MinIO, opik-backend, opik-frontend on :5173)
  - `docker compose --env-file .env.opik -f docker-compose.opik.yml up -d`
- **Web framework** (if needed): FastAPI + uvicorn

## Current Structure

```
.                         # 空项目，尚未初始化
├── .claude/
│   └── settings.local.json
└── .omc/
    └── state/
```