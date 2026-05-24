"""
实验 07: Dashboards & Production Monitoring
============================================
生产环境监控最佳实践：数据质量决定 Dashboard 价值。

运行方式:
    uv run python experiments/07-dashboards-monitoring/07_dashboards_monitoring.py
"""

import opik
from opik import LLMProvider
from opik import track, opik_context


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
    生产监控 (文档原文):
    - update_current_trace(feedback_scores=[...])
    - search_traces → log_traces_feedback_scores 闭环
    """
    print("=" * 60)
    print("[实验 7.2] 生产监控 (文档 API)")
    print("=" * 60)

    client = opik.Opik(
        project_name="opik-ob-experiment-07",
        host="http://localhost:5173",
        workspace="default",
    )

    # 模拟生产请求并记录反馈分数
    # 文档原文: update_current_trace(feedback_scores=[...])
    print("  [生产] 记录 Trace 并附加反馈分数")

    for i in range(3):
        trace = client.trace(
            name=f"prod_request_{i}",
            input={"query": f"query_{i}"},
            metadata={"environment": "production", "request_id": f"req_{i}"},
            tags=["production"],
        )

        span = trace.span(name="llm_call", type="llm",
                          input={"query": f"query_{i}"},
                          model="gpt-4", provider=opik.LLMProvider.OPENAI)
        span.end(output={"response": f"answer_{i}"},
                  usage={"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15})
        trace.end(output={"response": f"answer_{i}"})

        # 文档原文: 在 Trace 中附加反馈分数
        from opik import opik_context
        # 注意: 在 @track 装饰器函数内用 update_current_trace
        # 低层 API 也可以事后用 log_traces_feedback_scores
        print(f"  [请求 {i}] 已记录")

    # 批量更新反馈分数 (文档原文的方式)
    print("  [评分] 批量更新反馈分数")
    # 在实际场景中这里会 search_traces 然后打分
    # 文档原文:
    # traces = opik_client.search_traces(project_name="Default Project")
    # for trace in traces:
    #     opik_client.log_traces_feedback_scores(scores=[{
    #         "id": trace.id, "name": "quality", "value": 0.95
    #     }])

    client.end()
    print("  [完成] 生产监控\n")


if __name__ == "__main__":
    demonstrate_track_decorator()
    # demonstrate_production_monitoring()  # 取消注释以运行