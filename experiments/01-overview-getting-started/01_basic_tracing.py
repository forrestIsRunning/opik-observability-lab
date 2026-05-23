"""
实验 01: Tracing Overview & Getting Started
=============================================
Opik 可观测性的核心 API 使用最佳实践。

本实验假设 Opik 服务已在本地运行（docker compose up -d）。

运行方式:
    uv run python experiments/01-overview-getting-started/01_basic_tracing.py

SDK 参考:
    - opik.Opik.trace()
    - opik.Trace.end()
    - opik.Trace.span()
    - opik.Span.end()
    - opik.Opik.flush()
    - opik.Opik.end()
"""

import datetime
import uuid
from typing import Any, Dict

import opik
from opik import LLMProvider


def demonstrate_basic_trace():
    """
    Trace 全生命周期:
    1. 创建 Trace
    2. 添加子 Span
    3. 结束 Span
    4. 结束 Trace
    """
    print("=" * 60)
    print("[实验 1.1] Basic Trace 生命周期")
    print("=" * 60)

    client = opik.Opik(
        project_name="opik-ob-experiment-01",
        host="http://localhost:5173",
        workspace="default",
    )

    # Step 1: 创建一个 Trace (代表一次用户请求)
    trace = client.trace(
        name="user_query",
        input={"question": "What is the capital of France?"},
        metadata={
            "user_id": "user_001",
            "session_id": f"session_{uuid.uuid4().hex[:8]}",
            "environment": "development",
        },
        tags=["experiment", "basic-tracing", "v1"],
    )
    print(f"  [创建] Trace ID: {trace.id}")

    # Step 2: 创建一个 LLM Span (代表一次 LLM 调用)
    llm_span = trace.span(
        name="llm_call_gpt4",
        type="llm",
        input={"model": "gpt-4", "messages": [{"role": "user", "content": "What is the capital of France?"}]},
        model="gpt-4",
        provider=LLMProvider.OPENAI,
        metadata={"temperature": 0.7, "max_tokens": 100},
        tags=["llm-call"],
    )
    print(f"  [创建] LLM Span ID: {llm_span.id}")

    # Step 3: 结束 LLM Span
    llm_span.end(
        output={"content": "The capital of France is Paris."},
        usage={
            "prompt_tokens": 15,
            "completion_tokens": 8,
            "total_tokens": 23,
        },
        model="gpt-4",
        provider=LLMProvider.OPENAI,
    )
    print("  [结束] LLM Span")

    # Step 4: 结束 Trace
    trace.end(
        output={"answer": "The capital of France is Paris."},
        metadata={"total_duration_ms": 450},
    )
    print("  [结束] Trace")

    client.end()
    print("  [完成] 数据已刷新\n")


def demonstrate_nested_spans():
    """
    多层 Span 嵌套:
    Trace
    ├── Span: retrieve (检索)
    │   ├── Span: embedding (向量化)
    │   └── Span: vector_search (向量搜索)
    └── Span: generate (生成)
    """
    print("=" * 60)
    print("[实验 1.2] 嵌套 Span (RAG 模式)")
    print("=" * 60)

    client = opik.Opik(
        project_name="opik-ob-experiment-01",
        host="http://localhost:5173",
        workspace="default",
    )

    trace = client.trace(
        name="rag_query",
        input={"question": "What is Opik observability?"},
        tags=["rag", "nested-spans"],
    )
    print(f"  [创建] Trace ID: {trace.id}")

    # --- 检索阶段 ---
    retrieve_span = trace.span(name="retrieve", type="tool", input={"question": "What is Opik observability?"})

    # 子步骤: embedding
    embed_span = retrieve_span.span(
        name="embedding", type="llm",
        input={"text": "What is Opik observability?"},
        model="text-embedding-ada-002",
        provider=LLMProvider.OPENAI,
    )
    embed_span.end(output={"embedding_dim": 1536}, usage={"total_tokens": 10})
    print("  [结束] embedding span")

    # 子步骤: vector search
    search_span = retrieve_span.span(
        name="vector_search", type="tool",
        input={"query": "What is Opik observability?"},
    )
    search_span.end(output={"results_count": 3, "top_result": "Opik observability doc"})
    print("  [结束] vector_search span")

    retrieve_span.end(output={"context": "Opik is an observability platform..."})
    print("  [结束] retrieve span")

    # --- 生成阶段 ---
    generate_span = trace.span(
        name="generate", type="llm",
        input={"messages": [{"role": "user", "content": "What is Opik observability?"}]},
        model="gpt-4",
        provider=LLMProvider.OPENAI,
    )
    generate_span.end(
        output={"content": "Opik is an open-source LLM observability platform..."},
        usage={"prompt_tokens": 50, "completion_tokens": 30, "total_tokens": 80},
    )
    print("  [结束] generate span")

    trace.end(output={"answer": "Opik is an open-source LLM observability platform..."})
    print("  [结束] Trace")

    client.end()
    print("  [完成] 数据已刷新\n")


def demonstrate_thread_traces():
    """
    用 thread_id 关联多轮对话的多个 Trace.
    """
    print("=" * 60)
    print("[实验 1.3] 多轮对话 thread_id 关联")
    print("=" * 60)

    client = opik.Opik(
        project_name="opik-ob-experiment-01",
        host="http://localhost:5173",
        workspace="default",
    )

    thread_id = f"thread_{uuid.uuid4().hex[:12]}"
    print(f"  [线程] thread_id = {thread_id}")

    # 第一轮
    trace1 = client.trace(
        name="conversation_turn_1",
        input={"message": "Hello, who are you?"},
        thread_id=thread_id,
        tags=["conversation"],
    )
    trace1.end(output={"response": "I am an AI assistant."})
    print("  [轮次 1] Trace 已创建并结束")

    # 第二轮
    trace2 = client.trace(
        name="conversation_turn_2",
        input={"message": "What can you do?"},
        thread_id=thread_id,
        tags=["conversation"],
    )
    trace2.end(output={"response": "I can help with various tasks."})
    print("  [轮次 2] Trace 已创建并结束")

    # 第三轮
    trace3 = client.trace(
        name="conversation_turn_3",
        input={"message": "Tell me about Opik."},
        thread_id=thread_id,
        tags=["conversation"],
    )
    trace3.end(output={"response": "Opik is an LLM observability platform..."})
    print("  [轮次 3] Trace 已创建并结束")

    client.end()
    print(f"  [完成] 3 轮对话已通过 thread_id={thread_id} 关联\n")


def demonstrate_error_tracking():
    """
    error_info 的使用: 记录失败的 Trace
    """
    print("=" * 60)
    print("[实验 1.4] 错误追踪")
    print("=" * 60)

    client = opik.Opik(
        project_name="opik-ob-experiment-01",
        host="http://localhost:5173",
        workspace="default",
    )

    trace = client.trace(
        name="failed_query",
        input={"question": "Unknown topic"},
        tags=["error-demo"],
    )

    llm_span = trace.span(name="llm_call", type="llm", input={"question": "Unknown topic"})

    try:
        # 模拟一个失败
        raise ValueError("API rate limit exceeded")
    except ValueError as e:
        import traceback
        llm_span.end(
            error_info={
                "exception_type": "ValueError",
                "message": str(e),
                "traceback": traceback.format_exc(),
            }
        )
        trace.end(
            error_info={
                "exception_type": "ValueError",
                "message": str(e),
                "traceback": traceback.format_exc(),
            }
        )
        print("  [错误] 异常已记录到 Trace 和 Span")

    client.end()
    print("  [完成] 错误追踪数据已刷新\n")


if __name__ == "__main__":
    demonstrate_basic_trace()
    demonstrate_nested_spans()
    demonstrate_thread_traces()
    demonstrate_error_tracking()