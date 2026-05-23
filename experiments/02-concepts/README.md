# 02 — Opik 核心概念

## 概念体系

| 概念 | 说明 |
|------|------|
| **Trace** | 一次完整请求/操作的端到端记录。包含 input、output、metadata、tags |
| **Span** | Trace 内的一个步骤单元。支持嵌套（子 span）形成调用树 |
| **Span 类型** | `general`、`llm`、`tool`、`guardrail` — UI 中按类型过滤和着色 |
| **Project** | Trace 和 Span 的容器。用于隔离不同应用/环境的数据 |
| **Feedback Score** | 对 Trace/Span 的质量评分（数值或分类），用于评估 |
| **Dataset** | 数据集，用于评估测试 |
| **Prompt** | 可版本管理的 Prompt 模板 |
| **Thread** | 通过 `thread_id` 将多个 Trace 关联为一次多轮对话 |

## 核心 API 映射

```
opik.Opik(project_name=..., host=..., workspace=...)
  ├── .trace(...)       → Trace 对象
  │   ├── .span(...)    → Span 对象（子 span 容器）
  │   ├── .end(...)     → 结束 Trace
  │   └── .log_feedback_score(...) → 打分
  ├── .span(...)        → 独立 Span（直接配属到 Trace）
  ├── .flush(...)       → 强制刷新
  ├── .end(...)         → 关闭客户端
  ├── .get_trace_content(id)  → 读取 Trace
  └── .get_span_content(id)   → 读取 Span
```