# 04 — Agent Graphs & Distributed Traces

## Agent Graphs (Agent 图)

Agent 应用中多个 Agent 协同工作形成调用图。Opik 的 Span 嵌套天然支持图结构。

### 最佳实践

| 实践 | 说明 |
|------|------|
| **Span 树 = Agent 调用图** | 每个 Agent 调用作为一个 Span，父子关系构成图 |
| **Span type = tool** | Agent 调用用 `type="tool"` |
| **name 清晰标识** | Span name 用 `agent:xxx` 命名空间 |
| **metadata 传 Agent 状态** | 在 metadata 中记录 Agent 的思考过程 |

## Distributed Traces (分布式追踪)

跨服务的 Trace 传播通过 `get_distributed_trace_headers()` 实现。

### 核心 API

```python
# 服务 A (调用方)
headers = span.get_distributed_trace_headers()
# 将 headers 通过 RPC/HTTP 传给服务 B

# 服务 B (被调用方)
# 需要手动提取 headers 并传给 opik_context
from opik import opik_context
headers = DistributedTraceHeadersDict(opik_trace_id=..., opik_parent_span_id=...)
```

### 最佳实践

| 实践 | 说明 |
|------|------|
| **自动传播** | HTTP headers 或 RPC metadata 传递 |
| **opik_trace_id 不变** | 同一 Trace 的所有服务共享 opik_trace_id |
| **opik_parent_span_id** | 指向调用方的 span |
| **兼容 OpenTelemetry** | Opik 提供 OpenTelemetry 集成 (`opik.integrations.otel`) |