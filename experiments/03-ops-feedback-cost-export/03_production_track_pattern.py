"""
03_production_track_pattern.py — @track 装饰器 + 生产反馈闭环

@track 把函数调用自动记录为 Span，适合生产代码无侵入接入。
opik_context.update_current_trace / update_current_span 仅在 @track 函数内有效。

运行方式:
    uv run python experiments/03-ops-feedback-cost-export/03_production_track_pattern.py
"""

import os
import time
import opik
from opik import LLMProvider, track, opik_context

OPIK_PROJECT = os.getenv("OPIK_PROJECT", "ops-demo")


# @track 嵌套时外层自动成为父 Span
@track(name="llm_call", type="llm")
def call_llm(prompt: str) -> str:
    time.sleep(0.01)  # 模拟网络延迟
    total_tokens = len(prompt) + 20
    opik_context.update_current_span(
        usage={"prompt_tokens": len(prompt), "completion_tokens": 20, "total_tokens": total_tokens},
        model="gpt-4",
        provider=LLMProvider.OPENAI,
        output={"response": "Simulated response"},
    )
    return "Simulated response"


@track(name="process_query")
def process_query(query: str) -> str:
    return call_llm(query)


def track_decorator_demo() -> None:
    print("=" * 60)
    print("[3.1] @track 装饰器自动追踪")
    print("=" * 60)

    client = opik.Opik(
        project_name=OPIK_PROJECT,
        host="http://localhost:5173/api",
        workspace="default",
    )

    result = process_query("What is AI?")
    print(f"  [结果] {result}")

    client.end(timeout=30, flush=True)
    print("  [完成] @track 装饰器演示\n")


def production_feedback_loop() -> None:
    """
    生产反馈闭环：记录请求 → 事后批量打分。
    实际场景：search_traces 拉取未评分 Trace，评估后 log_traces_feedback_scores 写回。
    """
    print("=" * 60)
    print("[3.2] 生产反馈闭环")
    print("=" * 60)

    client = opik.Opik(
        project_name=OPIK_PROJECT,
        host="http://localhost:5173/api",
        workspace="default",
    )

    trace_ids: list[str] = []
    for i in range(3):
        trace = client.trace(
            name=f"prod_request_{i}",
            input={"query": f"query_{i}"},
            metadata={"environment": "production", "request_id": f"req_{i}"},
            tags=["production"],
        )
        span = trace.span(
            name="llm_call", type="llm",
            input={"query": f"query_{i}"},
            model="gpt-4", provider=LLMProvider.OPENAI,
        )
        span.end(
            output={"response": f"answer_{i}"},
            usage={"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
        )
        trace.end(output={"response": f"answer_{i}"})
        trace_ids.append(trace.id)
        print(f"  [请求 {i}] 已记录 trace_id={trace.id}")

    # 批量写回评分（实际场景下分数由评估模型或人工标注生成）
    scores = [{"id": tid, "name": "quality", "value": 0.9} for tid in trace_ids]
    client.log_traces_feedback_scores(scores)
    print(f"  [评分] 已为 {len(trace_ids)} 条 Trace 写回 quality=0.9")

    client.end(timeout=30, flush=True)
    print("  [完成] 生产反馈闭环\n")


def main() -> None:
    track_decorator_demo()
    production_feedback_loop()


if __name__ == "__main__":
    main()
