"""
实验 07: Dashboards & Production Monitoring
============================================
生产环境监控最佳实践：数据质量决定 Dashboard 价值。

运行方式:
    uv run python experiments/07-dashboards-monitoring/07_dashboards_monitoring.py
"""

import random
import uuid
import opik
from opik import LLMProvider
from opik import track


def demonstrate_track_decorator():
    """
    @track 装饰器: 自动追踪函数调用，生产环境推荐用法。
    """
    print("=" * 60)
    print("[实验 7.1] @track 装饰器")
    print("=" * 60)

    client = opik.Opik(
        project_name="opik-ob-experiment-07",
        host="http://localhost:5173",
        workspace="default",
    )

    # @track 会自动把函数调用记录为 Span
    @track(name="llm_call", type="llm")
    def call_llm(prompt: str) -> str:
        # 模拟 LLM 调用
        import time
        time.sleep(0.01)
        # 更新 span 数据
        opik_context.update_current_span(
            usage={"prompt_tokens": len(prompt), "completion_tokens": 20, "total_tokens": len(prompt) + 20},
            model="gpt-4",
            provider=LLMProvider.OPENAI,
            output={"response": "Simulated response"},
        )
        return "Simulated response"

    @track(name="process_query")
    def process_query(query: str) -> str:
        # 这个函数会被追踪为 span
        result = call_llm(query)
        return result

    # 执行
    result = process_query("What is AI?")
    print(f"  [结果] {result}")
    print("  [完成] @track 装饰器自动追踪\n")

    client.end()


def demonstrate_production_monitoring():
    """
    生产环境监控: 模拟高流量场景, 包含错误追踪、性能监控、成本监控。
    """
    print("=" * 60)
    print("[实验 7.2] 生产监控 (模拟)")
    print("=" * 60)

    client = opik.Opik(
        project_name="opik-ob-experiment-07",
        host="http://localhost:5173",
        workspace="default",
    )

    # 模拟 5 个生产请求
    scenarios = [
        {"query": "What is Opik?", "model": "gpt-4", "should_fail": False},
        {"query": "Explain tracing", "model": "gpt-3.5-turbo", "should_fail": False},
        {"query": "Long running query", "model": "gpt-4", "should_fail": False},
        {"query": "Error case", "model": "gpt-4", "should_fail": True},
        {"query": "Quick answer", "model": "gpt-3.5-turbo", "should_fail": False},
    ]

    for i, scenario in enumerate(scenarios):
        trace = client.trace(
            name=f"production_request_{i}",
            input={"query": scenario["query"]},
            metadata={
                "environment": "production",
                "region": "us-west-2",
                "user_tier": random.choice(["free", "pro", "enterprise"]),
                "request_id": uuid.uuid4().hex[:8],
            },
            tags=["production", scenario["model"]],
        )

        span = trace.span(
            name="llm_call",
            type="llm",
            input={"query": scenario["query"]},
            model=scenario["model"],
            provider=LLMProvider.OPENAI,
        )

        if scenario["should_fail"]:
            import traceback
            try:
                raise ValueError("Rate limit exceeded")
            except ValueError as e:
                span.end(
                    error_info={
                        "exception_type": "ValueError",
                        "message": str(e),
                        "traceback": traceback.format_exc(),
                    },
                )
                trace.end(
                    error_info={
                        "exception_type": "ValueError",
                        "message": str(e),
                        "traceback": traceback.format_exc(),
                    },
                )
                print(f"  [请求 {i}] 失败 (已记录 error_info)")
        else:
            import time
            latency = random.uniform(0.1, 1.5)
            time.sleep(0.01)
            span.end(
                output={"response": f"Answer about {scenario['query']}"},
                usage={
                    "prompt_tokens": len(scenario["query"]),
                    "completion_tokens": random.randint(20, 100),
                    "total_tokens": len(scenario["query"]) + random.randint(20, 100),
                },
                metadata={"latency_seconds": latency},
            )
            trace.end(
                output={"response": f"Answer about {scenario['query']}"},
                metadata={"latency_seconds": latency},
            )
            print(f"  [请求 {i}] 成功 ({latency:.2f}s)")

    client.end()
    print("  [完成] 生产监控数据\n")


if __name__ == "__main__":
    demonstrate_track_decorator()
    # demonstrate_production_monitoring()  # 取消注释以运行