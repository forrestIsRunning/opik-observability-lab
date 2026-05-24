"""
实验 08: Debugging Agents with Ollie
=====================================
按 Ollie 调试 Agent 的最佳实践准备数据。

运行方式:
    uv run python experiments/08-debug-ollie/08_debug_ollie.py
"""

import opik
from opik import LLMProvider


def demonstrate_agent_debugging():
    """
    Ollie Debug-Fix-Verify 循环 (文档原文):
    1. Find a failing trace
    2. Ask Ollie what went wrong
    3. Let Ollie fix your code
    4. Verify with a test suite
    """
    print("=" * 60)
    print("[实验 8.1] Debug-Fix-Verify 循环 — 数据准备")
    print("=" * 60)

    # Ollie 能读取的内容:
    # - 完整 Span 树 (input/output/latency/tokens/feedback)
    # - 跨 Trace 对比
    # - 项目级聚合分析
    # 所以数据的关键是: 完整的 Span 树 + 清晰的 metadata

    client = opik.Opik(
        project_name="opik-ob-experiment-08",
        host="http://localhost:5173",
        workspace="default",
    )

    # 模拟一个失败的 Trace (Ollie 调试入口)
    trace = client.trace(
        name="failing_agent",
        input={"task": "Book a flight ticket from NYC to London"},
        metadata={
            "agent_version": "v2.1.0",
            "prompt_version": "2026-05-01",
            "session_id": "sess_abc123",
        },
        tags=["ollie-debug", "failing"],
    )

    # Agent 思考
    thought = trace.span(name="agent:thought", type="general",
                         input={"task": "Book flight NYC→London"},
                         metadata={"reasoning": "Need search then book"})
    thought.end(output={"plan": ["search", "select", "book"]})

    # 工具调用 — 可能失败的地方
    search = trace.span(name="tool:search_flights", type="tool",
                        input={"from": "NYC", "to": "London", "date": "2026-06-15"})
    search.end(output={"flights": [{"flight": "AA100", "price": 450}], "total": 1})

    # LLM 调用
    llm = trace.span(name="llm:analyze", type="llm",
                     input={"options": "AA100 $450"},
                     model="gpt-4", provider=opik.LLMProvider.OPENAI)
    llm.end(output={"selected": "AA100", "reason": "Best price"},
             usage={"prompt_tokens": 80, "completion_tokens": 30, "total_tokens": 110})

    # 预订 — 模拟失败
    import traceback as tb
    try:
        raise ConnectionError("Booking API timeout after 5s")
    except ConnectionError as e:
        booking = trace.span(name="tool:book_flight", type="tool",
                             input={"flight": "AA100", "booking_api": "/api/bookings"})
        booking.end(error_info={
            "exception_type": "ConnectionError",
            "message": str(e),
            "traceback": tb.format_exc(),
        })
        trace.end(error_info={
            "exception_type": "ConnectionError",
            "message": str(e),
            "traceback": tb.format_exc(),
        })
        print("  [失败] Booking API timeout — 完整的 Span 树已记录")

    client.end()
    print("  [完成] Ollie 可以读取此 Trace 并分析根因\n")


def demonstrate_error_recovery():
    """
    Agent 错误恢复场景: 第一次调用失败, 重试后成功。
    这是 Ollie 调试的核心场景之一。
    """
    print("=" * 60)
    print("[实验 8.2] Agent 错误恢复")
    print("=" * 60)

    client = opik.Opik(
        project_name="opik-ob-experiment-08",
        host="http://localhost:5173",
        workspace="default",
    )

    trace = client.trace(
        name="agent_with_retry",
        input={"query": "Get weather in Tokyo"},
        tags=["ollie-debug", "retry", "error-recovery"],
    )

    # 第一次尝试 — 失败
    import traceback as tb
    try:
        raise ConnectionError("Weather API timeout after 5s")
    except ConnectionError as e:
        attempt1 = trace.span(
            name="tool:get_weather",
            type="tool",
            input={"city": "Tokyo", "attempt": 1},
            metadata={"max_retries": 3, "timeout": 5},
        )
        attempt1.end(
            error_info={
                "exception_type": "ConnectionError",
                "message": str(e),
                "traceback": tb.format_exc(),
            },
        )
        print("  [尝试 1] 失败: ConnectionError")

    # 第二次尝试 — 成功
    attempt2 = trace.span(
        name="tool:get_weather",
        type="tool",
        input={"city": "Tokyo", "attempt": 2},
        metadata={"retry_delay_ms": 1000, "circuit_breaker": False},
    )
    attempt2.end(output={
        "city": "Tokyo",
        "temperature_c": 22,
        "condition": "Sunny",
    })
    print("  [尝试 2] 成功: 已重试")

    trace.end(output={"weather": "Tokyo: 22°C Sunny"})
    print("  [完成] Agent 错误恢复场景\n")

    client.end()


if __name__ == "__main__":
    demonstrate_agent_debugging()
    demonstrate_error_recovery()