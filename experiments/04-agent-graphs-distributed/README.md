# 04 — Agent Graphs & Distributed Traces

> 基于真实文档更新

## Agent Graphs

Opik 支持三种方式记录 Agent 图：

1. **LangGraph** — `OpikTracer(graph=app.get_graph(xray=True))`
2. **Google ADK** — 自动生成，无需额外配置
3. **Manual Tracking** — 在 metadata 中嵌入 Mermaid 图定义：

```python
opik_context.update_current_trace(
    metadata={
        "_opik_graph_definition": {
            "format": "mermaid",
            "data": "graph TD; U[User]-->A[Agent]; A-->L[LLM]; L-->A;"
        }
    }
)
```

## Distributed Traces

### 核心 API（来自文档）

**客户端**（发送方）:
```python
from opik import track, opik_context

@track()
def my_client_function(prompt: str) -> str:
    headers = {}
    headers.update(opik_context.get_distributed_trace_headers())
    response = requests.post("http://.../generate", headers=headers, json={"prompt": prompt})
    return response.json()
```

**服务端**（接收方）:
```python
@track()
def my_llm_application():
    pass

@app.post("/generate")
def generate_llm_response(request: Request) -> str:
    return my_llm_application(opik_distributed_trace_headers=request.headers)
```

**Context Manager 方式**（更明确的控制）:
```python
from opik.decorator.context_manager import distributed_headers

with distributed_headers(headers, flush=False):
    result = my_llm_application()
```

### OpenTelemetry 桥接

```python
from opik.integrations.otel import OpikSpanProcessor, distributed_trace

provider.add_span_processor(OpikSpanProcessor())
# ...
distributed_trace.attach_to_parent(span, dict(request.headers))
```