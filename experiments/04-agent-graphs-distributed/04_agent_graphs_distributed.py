"""
实验 04: Agent Graphs & Distributed Traces
==========================================
演示 Agent 调用图和分布式追踪。

运行方式:
    uv run python experiments/04-agent-graphs-distributed/04_agent_graphs_distributed.py
"""

import uuid
import opik
from opik import opik_context


def demonstrate_agent_graph():
    """
    模拟 Agent 调用图:
    Trace: orchestrator (编排器)
    ├── Span: agent:planner (规划 Agent, type=tool)
    │   └── Span: llm:plan (LLM 规划, type=llm)
    ├── Span: agent:researcher (研究 Agent, type=tool)
    │   ├── Span: tool:web_search (搜索工具, type=tool)
    │   └── Span: llm:summarize (总结, type=llm)
    └── Span: agent:writer (写作 Agent, type=tool)
        └── Span: llm:generate (生成, type=llm)
    """
    print("=" * 60)
    print("[实验 4.1] Agent 调用图")
    print("=" * 60)

    client = opik.Opik(
        project_name="opik-ob-experiment-04",
        host="http://localhost:5173",
        workspace="default",
    )

    trace = client.trace(
        name="agent_orchestrator",
        input={"task": "Write a report about AI observability trends"},
        tags=["agent-graph", "multi-agent"],
    )
    print(f"  [创建] orchestrator trace: {trace.id}")

    # Agent 1: Planner
    planner = trace.span(
        name="agent:planner",
        type="tool",
        input={"task": "Write a report about AI observability trends"},
        metadata={"agent_role": "planner", "model": "gpt-4"},
    )
    plan_llm = planner.span(
        name="llm:plan",
        type="llm",
        input={"task": "Create a plan for the report"},
        model="gpt-4",
        provider=opik.LLMProvider.OPENAI,
    )
    plan_llm.end(
        output={"plan": "1. Research trends 2. Structure 3. Write"},
        usage={"total_tokens": 100},
    )
    planner.end(output={"plan": "1. Research trends 2. Structure 3. Write"})
    print("  [完成] agent:planner")

    # Agent 2: Researcher
    researcher = trace.span(
        name="agent:researcher",
        type="tool",
        input={"plan": "Research AI observability trends"},
        metadata={"agent_role": "researcher"},
    )
    web_search = researcher.span(
        name="tool:web_search",
        type="tool",
        input={"query": "AI observability trends 2026"},
    )
    web_search.end(output={"results_count": 5, "sources": ["opik docs", "blog"]})

    summarize_llm = researcher.span(
        name="llm:summarize",
        type="llm",
        input={"findings": "market growing, new tools emerging"},
        model="gpt-4",
        provider=opik.LLMProvider.OPENAI,
    )
    summarize_llm.end(
        output={"summary": "AI observability is rapidly evolving..."},
        usage={"total_tokens": 200},
    )
    researcher.end(output={"research": "AI observability trends data"})
    print("  [完成] agent:researcher")

    # Agent 3: Writer
    writer = trace.span(
        name="agent:writer",
        type="tool",
        input={"research": "all findings", "plan": "report structure"},
        metadata={"agent_role": "writer"},
    )
    write_llm = writer.span(
        name="llm:generate",
        type="llm",
        input={"draft": "Write final report"},
        model="gpt-4",
        provider=opik.LLMProvider.OPENAI,
    )
    write_llm.end(
        output={"report": "## AI Observability Trends Report\n..."},
        usage={"total_tokens": 500},
    )
    writer.end(output={"report": "## AI Observability Trends Report\n..."})
    print("  [完成] agent:writer")

    trace.end(output={"report": "Completed: AI Observability Trends Report"})
    print("  [完成] 完整 Agent 调用图\n")

    client.end()


def demonstrate_mermaid_agent_graph():
    """
    文档原文支持的 Agent Graph 方式:
    在 metadata 中嵌入 Mermaid 图定义，UI 渲染为可视化图表。
    """
    print("=" * 60)
    print("[实验 4.2] Mermaid Agent Graph (文档推荐方式)")
    print("=" * 60)

    client = opik.Opik(
        project_name="opik-ob-experiment-04",
        host="http://localhost:5173",
        workspace="default",
    )

    trace = client.trace(
        name="mermaid_agent_graph",
        input={"query": "What's the weather in Tokyo?"},
        metadata={
            "_opik_graph_definition": {
                "format": "mermaid",
                "data": (
                    "graph TD;"
                    "U[User]-->A[Agent];"
                    "A-->L[LLM];"
                    "L-->|generate|R[Response];"
                    "A-->T[Tool: WeatherAPI];"
                    "T-->L;"
                    "L-->A;"
                    "A-->U;"
                ),
            }
        },
        tags=["agent-graph", "mermaid"],
    )
    trace.end(output={"response": "Tokyo: 22°C, Sunny"})
    print("  [完成] Mermaid Agent Graph 已记录到 metadata")
    print("  [提示] 在 UI 中点击 'Show Agent Graph' 查看可视化")

    client.end()


def demonstrate_distributed_tracing():
    """
    文档原文的分布式追踪 API:
    - 客户端: opik_context.get_distributed_trace_headers()
    - 服务端: opik_distributed_trace_headers=request.headers
    """
    print("=" * 60)
    print("[实验 4.3] 分布式追踪 (文档 API)")
    print("=" * 60)

    # 模拟客户端调用
    # 文档原文:
    # headers = {}
    # headers.update(opik_context.get_distributed_trace_headers())
    # response = requests.post("http://.../generate", headers=headers)

    client = opik.Opik(
        project_name="opik-ob-experiment-04",
        host="http://localhost:5173",
        workspace="default",
    )

    trace = client.trace(
        name="distributed_request",
        input={"request": "GET /api/report"},
        tags=["distributed-trace"],
    )
    span_a = trace.span(name="service_a:auth", type="tool", input={"token": "valid"})
    span_a.end(output={"user_id": "user_001"})

    # 获取分布式追踪 headers (文档 API)
    from opik import opik_context
    headers = {}
    headers.update(opik_context.get_distributed_trace_headers())
    print(f"  [客户端] opik_trace_id={headers.get('opik_trace_id')}")
    print(f"  [客户端] opik_parent_span_id={headers.get('opik_parent_span_id')}")
    print(f"  [传播] Headers 通过 HTTP 传给下游服务")

    trace.end(output={"response": "200 OK"})
    print("  [完成] 分布式追踪")

    client.end()


if __name__ == "__main__":
    demonstrate_agent_graph()
    demonstrate_mermaid_agent_graph()
    demonstrate_distributed_tracing()