# Opik LLM Observability — Hands-on Experiments

> **探索 Opik 可观测性最佳实践的完整实验集**  
> 15 篇官方文档 → 8 个模块 → 100% 覆盖 → 零错误运行

[![Opik](https://img.shields.io/badge/Opik-2.0.46-blue)](https://github.com/comet-ml/opik)
[![Python](https://img.shields.io/badge/Python-3.11%2B-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 项目简介

本项目是对 [Opik](https://www.comet.com/docs/opik/) LLM 可观测性平台的**深度实践探索**，包含：

- ✅ **15 篇官方文档**完整提取（`_docs_extracted/`）
- ✅ **8 个实验模块**覆盖所有核心功能
- ✅ **可运行代码**对接本地 Opik Docker 栈
- ✅ **最佳实践**注释和架构说明

**适合人群**：
- LLM 应用开发者（需要可观测性）
- MLOps 工程师（生产监控）
- AI Agent 开发者（调试复杂调用链）

---

## 快速开始

### 1. 启动 Opik 服务

```bash
# 使用 Docker Compose 启动本地 Opik 栈
docker compose -f docker-compose.opik.yml up -d

# 验证服务健康
curl http://localhost:5173/api/is-alive/ping
# 预期输出: {"message":"Healthy Server","healthy":true}
```

### 2. 安装依赖

```bash
# 使用 uv 包管理器（推荐）
uv sync

# 或使用 pip
pip install opik>=2.0.46
```

### 3. 运行实验

```bash
# 运行单个实验
uv run python experiments/01-overview-getting-started/01_basic_tracing.py

# 运行所有实验
for f in experiments/*/0*.py; do uv run python "$f"; done
```

---

## 实验模块

| 模块 | 覆盖文档 | 核心内容 | 代码 |
|------|----------|----------|------|
| **01. Overview & Getting Started** | Overview, Getting Started | Trace/Span 生命周期、嵌套、thread_id | [01_basic_tracing.py](experiments/01-overview-getting-started/01_basic_tracing.py) |
| **02. Concepts** | Concepts | Trace-Span 关系、4 种 Span 类型、Project/Dataset | [02_concepts.py](experiments/02-concepts/02_concepts.py) |
| **03. Conversations & Media** | Log Conversations, Log Media | 多轮对话、Attachment API（3 种方式） | [03_conversations_media.py](experiments/03-conversations-media/03_conversations_media.py) |
| **04. Agent Graphs & Distributed** | Log Agent Graphs, Distributed Traces | Agent 调用图、Mermaid 可视化、W3C baggage | [04_agent_graphs_distributed.py](experiments/04-agent-graphs-distributed/04_agent_graphs_distributed.py) |
| **05. Feedback & Cost** | User Feedback, Cost Tracking | 反馈评分（单条/批量）、LLM 成本追踪 | [05_feedback_cost.py](experiments/05-feedback-cost/05_feedback_cost.py) |
| **06. Export & Config & Offline** | Export Data, SDK Config, Offline Fallback | OQL 导出、SDK 配置、SQLite 离线缓存 | [06_export_config_offline.py](experiments/06-export-config-offline/06_export_config_offline.py) |
| **07. Dashboards & Monitoring** | Dashboards, Production Monitoring | `@track` 装饰器、生产监控 API | [07_dashboards_monitoring.py](experiments/07-dashboards-monitoring/07_dashboards_monitoring.py) |
| **08. Debug with Ollie** | Debugging with Ollie | Ollie AI 调试助手、Debug-Fix-Verify 循环 | [08_debug_ollie.py](experiments/08-debug-ollie/08_debug_ollie.py) |

---

## 项目结构

```
opik-for-ob/
├── experiments/              # 8 个实验模块
│   ├── 01-overview-getting-started/
│   │   ├── README.md        # 理论 + 最佳实践
│   │   └── 01_basic_tracing.py
│   ├── 02-concepts/
│   ├── 03-conversations-media/
│   ├── 04-agent-graphs-distributed/
│   ├── 05-feedback-cost/
│   ├── 06-export-config-offline/
│   ├── 07-dashboards-monitoring/
│   └── 08-debug-ollie/
├── _docs_extracted/          # 15 篇官方文档 Markdown
│   ├── 01-overview.md
│   ├── 02-getting-started.md
│   └── ...
├── pyproject.toml            # uv 项目配置
├── .gitignore
└── README.md                 # 本文件
```

---

## 核心 API 速查

### Trace & Span

```python
import opik

client = opik.Opik(
    project_name="my-project",
    host="http://localhost:5173/api",
)

# 创建 Trace
trace = client.trace(
    name="user_query",
    input={"question": "What is Opik?"},
    tags=["demo"],
)

# 创建 Span
span = trace.span(
    name="llm_call",
    type="llm",
    model="gpt-4",
    provider=opik.LLMProvider.OPENAI,
)

# 结束 Span
span.end(
    output={"answer": "Opik is..."},
    usage={"total_tokens": 50},
)

# 结束 Trace
trace.end(output={"answer": "Opik is..."})
client.end()
```

### 装饰器（生产推荐）

```python
from opik import track

@track(name="my_function", type="llm")
def call_llm(prompt: str) -> str:
    # 自动追踪
    return "response"
```

### 多轮对话

```python
thread_id = "chat_abc123"

for turn in conversation:
    trace = client.trace(
        name=f"turn_{turn}",
        input={"message": turn["user"]},
        thread_id=thread_id,  # 关联多轮
    )
    trace.end(output={"response": turn["assistant"]})
```

---

## 技术栈

- **Opik SDK**: 2.0.46
- **Python**: 3.11-3.12
- **包管理**: uv
- **Opik 后端**: Docker Compose (MySQL 8.4, Redis 7.2, ClickHouse, MinIO)

---

## 文档来源

所有实验基于 Opik 官方文档（2026-05-24 版本）：

- [Opik Documentation](https://www.comet.com/docs/opik/)
- [Opik GitHub](https://github.com/comet-ml/opik)

文档提取使用 [Defuddle](https://github.com/danny-avila/defuddle) 工具。

---

## 贡献

欢迎提交 Issue 和 PR！

如果你发现：
- 实验代码有 bug
- 文档覆盖有遗漏
- 最佳实践可以改进

请直接提 Issue 或 PR。

---

## License

MIT License

---

## 致谢

- [Opik](https://github.com/comet-ml/opik) 团队提供的优秀可观测性平台
- [Defuddle](https://github.com/danny-avila/defuddle) 提供的文档提取工具

---

**⭐ 如果这个项目对你有帮助，请给个 Star！**
