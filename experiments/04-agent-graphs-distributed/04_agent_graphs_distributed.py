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


def demonstrate_distributed_tracing():
    """
    模拟分布式追踪: 服务 A → 服务 B → 服务 C
    通过 get_distributed_trace_headers() 传播上下文。
    """
    print("=" * 60)
    print("[实验 4.2] 分布式追踪 (模拟)")
    print("=" * 60)

    client = opik.Opik(
        project_name="opik-ob-experiment-04",
        host="http://localhost:5173",
        workspace="default",
    )

    # ----- 服务 A: API Gateway -----
    trace = client.trace(
        name="api_gateway",
        input={"request": "GET /api/report"},
        tags=["distributed-trace"],
    )
    span_a = trace.span(name="service_a:auth", type="tool", input={"token": "valid"})
    span_a.end(output={"user_id": "user_001"})

    # 获取分布式追踪 headers (模拟传给服务 B)
    span_b = trace.span(name="service_a:call_service_b", type="tool", input={"endpoint": "/internal/b"})
    headers = span_b.get_distributed_trace_headers()
    print(f"  [传播] Trace ID: {headers['opik_trace_id']}")
    print(f"  [传播] Parent Span ID: {headers['opik_parent_span_id']}")
    span_b.end(output={"service_b_response": "ok"})

    trace.end(output={"response": "200 OK"})
    print("  [完成] 分布式追踪 headers 已生成")

    # headers 可以序列化后通过 HTTP/gRPC 传给下游服务
    print(f"  下游服务收到 headers: {dict(headers)}")

    client.end()


if __name__ == "__main__":
    demonstrate_agent_graph()
    demonstrate_distributed_tracing()