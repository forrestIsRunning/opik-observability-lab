# 01 — Tracing Fundamentals

> "skill 教 SDK 怎么用；本模块教 trace + thread + attachment 组合在一起的 production 形态"

基础 API 参考见 `.agents/skills/opik/SKILL.md`，本模块不重复 SDK 文档。

## 本模块内容

| 文件 | 内容 |
|------|------|
| `01_basic_tracing.py` | Trace/Span 生命周期 · 嵌套 Span（RAG 模式） · thread_id 多轮对话 · error_info 错误追踪 |
| `02_attachments.py` | 3 种 Attachment 上传方式：span 参数 / client.span() / @track + opik_context |

## 核心模式

### Trace → Span 嵌套（RAG 模式）

```
Trace: rag_query
├── Span: retrieve (tool)
│   ├── Span: embedding (llm)
│   └── Span: vector_search (tool)
└── Span: generate (llm)
```

### thread_id 多轮对话

同一 `thread_id` 将多个 Trace 归组为对话线程，在 Project → Threads tab 可视化。

```python
trace = client.trace(name="turn_1", thread_id=thread_id, ...)
```

### Attachment 上传方式对比

| 方式 | 适用场景 |
|------|---------|
| `trace.span(attachments=[...])` | 创建时已知附件内容 |
| `client.span(trace_id=..., attachments=[...])` | 需要跨函数边界显式关联 trace |
| `@track` + `opik_context.update_current_trace(attachments=[...])` | 生产推荐，装饰器自动管理上下文 |

## 运行

```bash
uv run python experiments/01-tracing-fundamentals/01_basic_tracing.py
uv run python experiments/01-tracing-fundamentals/02_attachments.py
```

前提: 本地 Opik 服务已启动（`docker compose -f docker-compose.opik.yml up -d`）。
结果在 http://localhost:5173 查看。
