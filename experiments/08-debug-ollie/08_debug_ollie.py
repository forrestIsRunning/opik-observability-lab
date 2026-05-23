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
    按 Ollie 调试 Agent 的最佳实践来准备数据。
    关键点: 完整 Span 树 + 思维链 metadata + 错误追踪。
    """
    print("=" * 60)
    print("[实验 8.1] Agent 调试数据准备")
    print("=" * 60)

    client = opik.Opik(
        project_name="opik-ob-experiment-08",
        host="http://localhost:5173",
        workspace="default",
    )

    trace = client.trace(
        name="ollie_debug_agent",
        input={"task": "Book a flight ticket from NYC to London"},
        metadata={
            "agent_version": "v2.1.0",
            "prompt_version": "2026-05-01",
            "session_id": "sess_abc123",
        },
        tags=["ollie-debug", "agent", "flight-booking"],
    )

    # Step 1: Agent 思考 (thought)
    thought_span = trace.span(
        name="agent:thought",
        type="general",
        input={"task": "Book a flight ticket from NYC to London"},
        metadata={
            "reasoning": "Need to: 1) Search flights 2) Find best option 3) Book",
            "plan": ["search_flights", "select_option", "book_ticket"],
        },
    )
    thought_span.end(output={"plan": ["search_flights", "select_option", "book_ticket"]})
    print("  [Step 1] Agent 已规划")

    # Step 2: 工具调用 — 搜索航班
    search_span = trace.span(
        name="tool:search_flights",
        type="tool",
        input={"from": "NYC", "to": "London", "date": "2026-06-15"},
        metadata={"api_endpoint": "/api/flights/search", "retry_count": 0},
    )
    # 模拟搜索结果
    search_span.end(output={
        "flights": [
            {"flight": "AA100", "price": 450, "duration": "7h"},
            {"flight": "BA200", "price": 520, "duration": "6.5h"},
        ],
        "total_options": 2,
    })
    print("  [Step 2] 航班搜索完成")

    # Step 3: LLM 分析结果
    analysis_span = trace.span(
        name="llm:analyze_options",
        type="llm",
        input={"options": "AA100 $450 7h, BA200 $520 6.5h", "criteria": "best value"},
        model="gpt-4",
        provider=LLMProvider.OPENAI,
    )
    analysis_span.end(
        output={"selected": "AA100", "reason": "Best price with reasonable duration"},
        usage={"prompt_tokens": 80, "completion_tokens": 30, "total_tokens": 110},
    )
    print("  [Step 3] LLM 已选择最优")

    # Step 4: 预订操作
    booking_span = trace.span(
        name="tool:book_flight",
        type="tool",
        input={"flight": "AA100", "passenger": "John Doe"},
        metadata={"booking_api": "/api/bookings/create"},
    )
    booking_span.end(output={
        "booking_id": "BK-12345",
        "status": "confirmed",
        "total_price": 450.00,
    })
    print("  [Step 4] 航班已预订")

    trace.end(output={
        "result": "Booked AA100 NYC→London",
        "booking_ref": "BK-12345",
        "total_cost": 450.00,
    })
    print("  [完成] Agent 调试数据已准备\n")

    client.end()


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