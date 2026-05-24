# 02 — Opik 核心概念

> 基于真实文档更新。新增：Threads、Metrics、Optimization、Evaluation

## 概念体系

| 概念 | 定义（文档原文） |
|------|------------------|
| **Trace** | "A complete execution path for a single interaction with an LLM or agent" |
| **Span** | "Individual operations or steps within a trace — hierarchical structure" |
| **Thread** | "A collection of related traces that form a coherent conversation or workflow" |
| **Metric** | "Quantitative measurements that provide objective assessments of your AI models' performance" |
| **Optimization** | "The systematic process of refining and evaluating LLM prompts and configurations" |
| **Evaluation** | "A framework for systematically testing your prompts and models against datasets" |

## Span 类型

- `general` — 通用步骤
- `llm` — LLM 调用
- `tool` — 工具/函数调用
- `guardrail` — 安全/内容过滤

## Core API 映射

```python
client = opik.Opik(project_name=..., host=...)
client.trace(name=..., input=..., thread_id=..., tags=...)
  ├── .span(name=..., type=..., model=..., provider=...)
  │   ├── .end(output=..., usage=...)
  │   ├── .log_feedback_score(name=..., value=...)
  │   └── .span(...)  # 嵌套子 span
  ├── .end(output=..., metadata=...)
  └── .log_feedback_score(name=..., value=..., reason=...)

client.log_traces_feedback_scores([{id, name, value, reason}])
client.search_traces(project_name=..., filter_string=...)
client.get_trace_content(id)
client.end()  # 确保数据刷新
```