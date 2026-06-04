# opik-observability-lab

> Skill 教你怎么用 Opik；本仓库教你 production 里那些 corner cases 和组合模式。

[![Python](https://img.shields.io/badge/Python-3.11%2B-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

[opik-skills](https://github.com/comet-ml/opik-skills) 覆盖了 SDK 基础用法、Framework integrations、Prompt Library API、Local Runner 概念。本仓库**不重复那些**——它展示的是 skill 没涉及的生产级组合场景：多轮对话 + Attachment 联动、跨服务 trace 头传播、机器评分 → Annotation Queue 完整管道、Prompt 演进 V1→V2→V3 回滚工作流，以及 skill 强调但容易踩坑的 LiteLLM 孤儿 trace / entrypoint primitives 约束的可运行演示。

---

## 快速决策表

| 我想做什么 | 看哪里 |
|-----------|--------|
| 学 `@opik.track` 基础用法 | [opik-skills: instrument/SKILL.md](.agents/skills/instrument/SKILL.md) |
| 学 Prompt Library API（`client.create_prompt` 等） | [opik-skills: opik/SKILL.md](.agents/skills/opik/SKILL.md) |
| 学 `opik connect` / Local Runner 概念 | opik-skills: opik/SKILL.md §Local Runner |
| 看 thread_id + Attachment 组合的生产形态 | [01-tracing-fundamentals](experiments/01-tracing-fundamentals/) |
| 看跨服务 trace 头传播 + Mermaid agent graph | [02-distributed-tracing](experiments/02-distributed-tracing/) |
| 看 feedback scoring + OQL 搜索 + `@track` 生产模式 | [03-ops-feedback-cost-export](experiments/03-ops-feedback-cost-export/) |
| 看 RAG eval + Feishu thread 映射 + 机器评分队列 | [04-rag-evaluation](experiments/04-rag-evaluation/) |
| 看 Prompt V1→V2→V3 演进 + 回滚工作流 | [05-prompt-library](experiments/05-prompt-library/) |
| 复现 LiteLLM 孤儿 trace bug + 修复 / entrypoint primitives | [06-local-runner-and-pitfalls](experiments/06-local-runner-and-pitfalls/) |

---

## 模块清单

| # | 模块 | 核心价值 | 入口脚本 |
|---|------|----------|----------|
| 01 | [Tracing Fundamentals](experiments/01-tracing-fundamentals/) | trace/span 生命周期 + thread_id 多轮对话 + 3 种 Attachment 上传模式 | `01_basic_tracing.py` |
| 02 | [Distributed Tracing](experiments/02-distributed-tracing/) | Mermaid agent graph 嵌入 metadata + 跨服务 trace 头传播 | `run_distributed.py` |
| 03 | [Ops: Feedback / Cost / Export](experiments/03-ops-feedback-cost-export/) | feedback scoring + multi-provider cost + OQL 搜索 + `@track` 生产模式 | `01_feedback_and_cost.py` |
| 04 | [RAG Evaluation](experiments/04-rag-evaluation/) | 端到端 RAG eval pipeline + Feishu thread 映射 + 机器评分 → Annotation Queue | `run_02_evaluate.py` |
| 05 | [Prompt Library](experiments/05-prompt-library/) | Prompt 版本演进 V1→V2→V3 + 回滚工作流 + pin commit 生产模式 | `run_03_prompt_evolution.py` |
| 06 | [Local Runner & Pitfalls](experiments/06-local-runner-and-pitfalls/) | entrypoint primitives 约束 + LiteLLM 孤儿 trace 复现与修复 | `run_02_litellm_orphan_fix.py` |

---

## 快速开始

```bash
# 1. 启动本地 Opik 服务
docker compose -f docker-compose.opik.yml up -d
curl http://localhost:5173/api/is-alive/ping   # 预期: {"healthy":true}

# 2. 安装依赖
uv sync

# 3. 跑一个最有代表性的实验（RAG eval，无需 LLM API key）
uv run python experiments/04-rag-evaluation/run_02_evaluate.py

# 前往 http://localhost:5173 查看 trace 和 evaluation 结果
```

其余实验的运行方式见各模块 `README.md`。

---

## 与 opik-skills 的关系

```
┌──────────────────────────┐         ┌──────────────────────────────────┐
│      opik-skills          │  互补   │   opik-observability-lab          │
│ ─────────────────────     │ ◀─────▶ │ ──────────────────────────────   │
│ • Tracing 101             │         │ • thread_id + Attachment 组合     │
│ • Framework integrations  │         │ • 跨服务 trace 头传播              │
│ • Prompt Library API      │         │ • Prompt 演进 V1→V2→V3 + 回滚     │
│ • Test Suites             │         │ • RAG eval + 机器评分队列           │
│ • opik connect 概念       │         │ • LiteLLM 孤儿 trace 可运行演示     │
│ • entrypoint 约束说明     │         │ • entrypoint primitives 代码示例    │
│                           │         │ • Feishu thread 映射方案           │
└──────────────────────────┘         └──────────────────────────────────┘
```

**使用建议**：先用 opik-skills 建立 SDK 心智模型，再来本仓库看生产模式。两者不重复，各有侧重。

---

## 贡献回上游

在研究 opik-skills 过程中发现了若干改进点，已整理在 [`.omc/skill-feedback.md`](.omc/skill-feedback.md)，按 P0/P1/P2 分级，包含复现步骤和建议改法，待后续分批提 PR 到 `comet-ml/opik-skills`。

---

## 环境要求

| 工具 | 要求 |
|------|------|
| Python | >=3.11, <3.13 |
| uv | 最新版 |
| Docker | 启动本地 Opik stack |
| opik | >=2.0.46 |

本地 Opik 服务：Frontend `http://localhost:5173` · API `http://localhost:5173/api`

---

## License

MIT License
