# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`opik-observability-lab` — 基于 Comet Opik 的 LLM 可观测性最佳实践实验项目。

## Conventions

- **Python**: >=3.11, <3.13
- **Package manager**: `uv` (uv sync, uv run)
- **Linter**: `ruff` (line-length=100, target-version="py311")
- **SDK**: `opik>=2.0.46` — LLM 评估与可观测性 SDK
  - `opik.Opik(project_name=..., host="http://localhost:5173/api", workspace="default")`
  - `client.trace(...)` / `trace.span(...)` / `span.end()` / `trace.end()`
  - `client.log_traces_feedback_scores(...)`
  - `client.search_traces(filter_string=...)` — OQL 查询
  - `client.end(timeout=30, flush=True)`
  - `@opik.track` — 装饰器自动追踪（生产推荐）
  - `opik_context.update_current_trace(...)` — 仅在 @track 内有效
- **Local Opik stack**: Docker Compose
  - `docker compose -f docker-compose.opik.yml up -d`
  - Frontend: http://localhost:5173
  - API: http://localhost:5173/api
- **GitHub**: https://github.com/forrestIsRunning/opik-observability-lab

## Gitignore Rules

以下目录/文件不应提交到 git:
- `.idea/` — JetBrains IDE 配置
- `.venv/` — Python 虚拟环境
- `.omc/` — oh-my-claudecode 状态
- `_docs/` — 原始 HTML 抓取缓存
- `.env` — 环境变量（含密钥）

## Current Structure

```
opik-observability-lab/
├── experiments/              # 8 个实验模块（每个含 README + .py）
├── _docs_extracted/          # 15 篇官方文档 Markdown（已提交）
├── docker-compose.opik.yml   # 本地 Opik 服务
├── pyproject.toml            # uv 项目配置
├── README.md                 # 项目说明（面向 GitHub）
├── LICENSE                   # MIT
└── CLAUDE.md                 # 本文件
```
