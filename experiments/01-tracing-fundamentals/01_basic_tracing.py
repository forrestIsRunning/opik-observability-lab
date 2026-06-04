"""
实验 01: Tracing Fundamentals — 生命周期 + 嵌套 + thread_id
=============================================================
运行方式:
    uv run python experiments/01-tracing-fundamentals/01_basic_tracing.py
"""

import traceback
import uuid

import opik
from opik import LLMProvider

CLIENT_KWARGS = dict(
    project_name="opik-ob-experiment-01",
    host="http://localhost:5173/api",
    workspace="default",
)


def basic_trace():
    """Trace + LLM Span 完整生命周期."""
    print("=" * 60)
    print("[1.1] Trace / Span 生命周期")
    print("=" * 60)

    client = opik.Opik(**CLIENT_KWARGS)

    trace = client.trace(
        name="user_query",
        input={"question": "What is the capital of France?"},
        metadata={"user_id": "user_001", "environment": "development"},
        tags=["basic-tracing"],
    )
    print(f"  Trace ID: {trace.id}")

    span = trace.span(
        name="llm_call",
        type="llm",
        input={"messages": [{"role": "user", "content": "What is the capital of France?"}]},
        model="gpt-4",
        provider=LLMProvider.OPENAI,
    )
    span.end(
        output={"content": "The capital of France is Paris."},
        usage={"prompt_tokens": 15, "completion_tokens": 8, "total_tokens": 23},
    )

    trace.end(output={"answer": "The capital of France is Paris."})
    client.end(timeout=30, flush=True)
    print("  ✓ done\n")


def nested_spans():
    """RAG 模式: Trace → retrieve(embed + vector_search) → generate."""
    print("=" * 60)
    print("[1.2] 嵌套 Span (RAG 模式)")
    print("=" * 60)

    client = opik.Opik(**CLIENT_KWARGS)
    question = "What is Opik observability?"

    trace = client.trace(name="rag_query", input={"question": question}, tags=["rag"])
    print(f"  Trace ID: {trace.id}")

    retrieve = trace.span(name="retrieve", type="tool", input={"question": question})

    embed = retrieve.span(
        name="embedding",
        type="llm",
        input={"text": question},
        model="text-embedding-ada-002",
        provider=LLMProvider.OPENAI,
    )
    embed.end(output={"embedding_dim": 1536}, usage={"total_tokens": 10})

    search = retrieve.span(name="vector_search", type="tool", input={"query": question})
    search.end(output={"results_count": 3})

    retrieve.end(output={"context": "Opik is an observability platform..."})

    generate = trace.span(
        name="generate",
        type="llm",
        input={"messages": [{"role": "user", "content": question}]},
        model="gpt-4",
        provider=LLMProvider.OPENAI,
    )
    generate.end(
        output={"content": "Opik is an open-source LLM observability platform..."},
        usage={"prompt_tokens": 50, "completion_tokens": 30, "total_tokens": 80},
    )

    trace.end(output={"answer": "Opik is an open-source LLM observability platform..."})
    client.end(timeout=30, flush=True)
    print("  ✓ done\n")


def thread_traces():
    """同一 thread_id 把多轮对话 Trace 归组."""
    print("=" * 60)
    print("[1.3] 多轮对话 thread_id 关联")
    print("=" * 60)

    client = opik.Opik(**CLIENT_KWARGS)
    thread_id = f"thread_{uuid.uuid4().hex[:12]}"
    print(f"  thread_id = {thread_id}")

    turns = [
        ("Hello, who are you?", "I am an AI assistant."),
        ("What can you do?", "I can help with various tasks."),
        ("Tell me about Opik.", "Opik is an LLM observability platform..."),
    ]

    for i, (user_msg, assistant_msg) in enumerate(turns, 1):
        trace = client.trace(
            name=f"turn_{i}",
            input={"message": user_msg},
            thread_id=thread_id,
            tags=["conversation"],
        )
        trace.end(output={"response": assistant_msg})
        print(f"  [轮次 {i}] ✓")

    client.end(timeout=30, flush=True)
    print(f"  ✓ 3 轮对话通过 thread_id={thread_id} 关联\n")


def error_tracking():
    """error_info 记录失败的 Trace 和 Span."""
    print("=" * 60)
    print("[1.4] 错误追踪")
    print("=" * 60)

    client = opik.Opik(**CLIENT_KWARGS)
    trace = client.trace(name="failed_query", input={"question": "Unknown topic"}, tags=["error"])

    span = trace.span(name="llm_call", type="llm", input={"question": "Unknown topic"})
    try:
        raise ValueError("API rate limit exceeded")
    except ValueError as e:
        tb = traceback.format_exc()
        err = {"exception_type": "ValueError", "message": str(e), "traceback": tb}
        span.end(error_info=err)
        trace.end(error_info=err)
        print("  ✓ 异常已记录到 Trace 和 Span")

    client.end(timeout=30, flush=True)
    print("  ✓ done\n")


if __name__ == "__main__":
    basic_trace()
    nested_spans()
    thread_traces()
    error_tracking()
