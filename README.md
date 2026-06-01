# Opik LLM Observability — Hands-on Experiments

> 15 篇官方文档 + 1 个扩展示例，整理成 9 个可运行实验模块

[![Python](https://img.shields.io/badge/Python-3.11%2B-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 项目简介

本项目是对 [Opik](https://www.comet.com/docs/opik/) LLM 可观测性平台的实践合集，包含：

- 15 篇官方文档提取到 `_docs_extracted/`
- 9 个实验模块，覆盖 tracing、对话、媒体、agent graph、反馈、成本、导出、配置、离线、dashboard、调试与评测
- 可直接运行的本地 Opik Docker 栈
- 按模块组织的代码与说明，便于单独复用

适合：

- LLM 应用开发者
- MLOps 工程师
- Agent / RAG 系统开发者

---

## 快速开始

### 1. 启动本地 Opik

```bash
docker compose -f docker-compose.opik.yml up -d
curl http://localhost:5173/api/is-alive/ping
```

### 2. 安装依赖

```bash
uv sync
```

### 3. 运行实验

```bash
# 运行单个实验
uv run python experiments/01-overview-getting-started/01_basic_tracing.py

# 运行 09 号模块的评测入口
uv run python experiments/09-rag-agent-evaluation/run_02_evaluate.py
```

---

## 实验模块

| 模块 | 覆盖内容 | 代码 |
|---|---|---|
| **01. Overview & Getting Started** | Trace / Span 生命周期、嵌套、thread_id | [01_basic_tracing.py](experiments/01-overview-getting-started/01_basic_tracing.py) |
| **02. Concepts** | Trace-Span 关系、Span 类型、Project / Dataset | [02_concepts.py](experiments/02-concepts/02_concepts.py) |
| **03. Conversations & Media** | 多轮对话、Attachment API | [03_conversations_media.py](experiments/03-conversations-media/03_conversations_media.py) |
| **04. Agent Graphs & Distributed** | Agent 调用图、Mermaid 可视化、分布式 Trace | [04_agent_graphs_distributed.py](experiments/04-agent-graphs-distributed/04_agent_graphs_distributed.py) |
| **05. Feedback & Cost** | 反馈评分、批量打分、成本追踪 | [05_feedback_cost.py](experiments/05-feedback-cost/05_feedback_cost.py) |
| **06. Export & Config & Offline** | OQL 导出、SDK 配置、离线缓存 | [06_export_config_offline.py](experiments/06-export-config-offline/06_export_config_offline.py) |
| **07. Dashboards & Monitoring** | `@track`、反馈闭环、生产监控 | [07_dashboards_monitoring.py](experiments/07-dashboards-monitoring/07_dashboards_monitoring.py) |
| **08. Debug with Ollie** | Ollie 调试助手、Debug-Fix-Verify 流程 | [08_debug_ollie.py](experiments/08-debug-ollie/08_debug_ollie.py) |
| **09. RAG / Agent Evaluation** | 数据集、Experiment dashboard、thread 映射、标注队列 | [README.md](experiments/09-rag-agent-evaluation/README.md) |

---

## 项目结构

```text
opik-observability-lab/
├── experiments/
│   ├── 01-overview-getting-started/
│   ├── 02-concepts/
│   ├── 03-conversations-media/
│   ├── 04-agent-graphs-distributed/
│   ├── 05-feedback-cost/
│   ├── 06-export-config-offline/
│   ├── 07-dashboards-monitoring/
│   ├── 08-debug-ollie/
│   └── 09-rag-agent-evaluation/
├── _docs_extracted/
├── docker-compose.opik.yml
├── pyproject.toml
├── README.md
└── LICENSE
```

---

## 核心 API 速查

### Trace & Span

```python
import opik

client = opik.Opik(
    project_name="my-project",
    host="http://localhost:5173/api",
    workspace="default",
)

trace = client.trace(
    name="user_query",
    input={"question": "What is Opik?"},
    tags=["demo"],
)

span = trace.span(
    name="llm_call",
    type="llm",
    model="gpt-4",
    provider=opik.LLMProvider.OPENAI,
)

span.end(
    output={"answer": "Opik is..."},
    usage={"total_tokens": 50},
)

trace.end(output={"answer": "Opik is..."})
client.end()
```

### 生产推荐的装饰器

```python
from opik import track

@track(name="my_function", type="llm")
def call_llm(prompt: str) -> str:
    return "response"
```

### 多轮对话

```python
thread_id = "chat_abc123"

for turn in conversation:
    trace = client.trace(
        name=f"turn_{turn}",
        input={"message": turn["user"]},
        thread_id=thread_id,
    )
    trace.end(output={"response": turn["assistant"]})
```

---

## 技术栈

- Opik SDK: `opik>=1.0.0`
- Python: 3.11-3.12
- 包管理: `uv`
- 本地 Opik 后端: Docker Compose（MySQL、Redis、ClickHouse、MinIO）

---

## 文档来源

前 8 个实验模块基于 Opik 官方文档整理，`09-rag-agent-evaluation` 是基于同一套 SDK 和 UI 流程做的扩展示例。

- [Opik Documentation](https://www.comet.com/docs/opik/)
- [Opik GitHub](https://github.com/comet-ml/opik)

文档提取使用 [Defuddle](https://github.com/danny-avila/defuddle)。

---

## 贡献

欢迎提交 Issue 和 PR。

如果你发现：

- 实验代码有 bug
- 文档覆盖有遗漏
- 最佳实践可以改进

请直接提 Issue 或 PR。

---

## License

MIT License
