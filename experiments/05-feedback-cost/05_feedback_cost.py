"""
实验 05: User Feedback & Cost Tracking
=======================================
用户反馈评分 + LLM 调用成本追踪。

运行方式:
    uv run python experiments/05-feedback-cost/05_feedback_cost.py
"""

import uuid
import opik
from opik import LLMProvider
from opik.types import BatchFeedbackScoreDict


def demonstrate_feedback_scoring():
    """
    用户反馈评分: 单个打分 + 批量打分。
    """
    print("=" * 60)
    print("[实验 5.1] 用户反馈评分")
    print("=" * 60)

    client = opik.Opik(
        project_name="opik-ob-experiment-05",
        host="http://localhost:5173/api",
        workspace="default",
    )

    # --- 单条打分 (在 Trace 对象上直接打分) ---
    trace = client.trace(
        name="feedback_demo",
        input={"question": "What is Opik?"},
        tags=["feedback-demo"],
    )

    span = trace.span(
        name="llm_response", type="llm",
        input={"question": "What is Opik?"},
        model="gpt-4",
        provider=LLMProvider.OPENAI,
    )
    span.end(output={"answer": "Opik is..."}, usage={"total_tokens": 50})
    trace.end(output={"answer": "Opik is..."})

    # 对 Trace 打分 (可以在任意时间点，不依赖 Trace 对象存在)
    trace.log_feedback_score(
        name="helpfulness",
        value=5,
        category_name="excellent",
        reason="Accurate and concise answer",
    )
    print(f"  [打分] Trace: helpfulness=5 (excellent)")

    # 对 Span 打分
    span.log_feedback_score(
        name="response_quality",
        value=0.95,
        reason="High quality LLM response",
    )
    print(f"  [打分] Span: response_quality=0.95")

    client.end()
    print("  [完成] 单条打分\n")

    # --- 批量打分 ---
    print("=" * 60)
    print("[实验 5.2] 批量反馈评分")
    print("=" * 60)

    client2 = opik.Opik(
        project_name="opik-ob-experiment-05",
        host="http://localhost:5173/api",
        workspace="default",
    )

    # 先创建一批 Trace
    trace_ids = []
    for i in range(3):
        t = client2.trace(
            name=f"batch_demo_{i}",
            input={"query": f"query_{i}"},
            tags=["batch-feedback"],
        )
        t.end(output={"result": f"result_{i}"})
        trace_ids.append(t.id)
        print(f"  [创建] Trace {i}: {t.id}")

    # 批量打分
    scores: list[BatchFeedbackScoreDict] = [
        {"id": tid, "name": "accuracy", "value": 0.95, "reason": "Correct output"}
        for tid in trace_ids
    ]
    client2.log_traces_feedback_scores(scores)
    print(f"  [批量] 为 {len(trace_ids)} 条 Trace 打 accuracy 分")

    client2.end()
    print("  [完成] 批量打分\n")


def demonstrate_cost_tracking():
    """
    LLM 调用成本追踪。
    """
    print("=" * 60)
    print("[实验 5.3] LLM 成本追踪")
    print("=" * 60)

    client = opik.Opik(
        project_name="opik-ob-experiment-05",
        host="http://localhost:5173/api",
        workspace="default",
    )

    trace = client.trace(
        name="cost_tracking_demo",
        input={"task": "multi_model_demo"},
        tags=["cost-tracking"],
    )

    # 1. OpenAI GPT-4 — Opik 自动算成本
    span1 = trace.span(
        name="gpt4_call",
        type="llm",
        input={"prompt": "Explain quantum computing"},
        model="gpt-4",
        provider=LLMProvider.OPENAI,
    )
    span1.end(
        output={"text": "Quantum computing..."},
        usage={"prompt_tokens": 100, "completion_tokens": 200, "total_tokens": 300},
    )
    print("  [成本] GPT-4: 100 prompt + 200 completion tokens (自动算成本)")

    # 2. Anthropic Claude
    span2 = trace.span(
        name="claude_call",
        type="llm",
        input={"prompt": "Explain neural networks"},
        model="claude-sonnet-4-20250514",
        provider=LLMProvider.ANTHROPIC,
    )
    span2.end(
        output={"text": "Neural networks..."},
        usage={"prompt_tokens": 50, "completion_tokens": 150, "total_tokens": 200},
    )
    print("  [成本] Claude: 50 prompt + 150 completion tokens (自动算成本)")

    # 3. 手动指定 total_cost — 覆盖自动计算
    span3 = trace.span(
        name="custom_model",
        type="llm",
        input={"prompt": "Hello"},
        model="my-custom-model",
        provider="custom_provider",
    )
    span3.end(
        output={"text": "Hi there"},
        usage={"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
        total_cost=0.005,  # 手动指定，覆盖自动计算
    )
    print("  [成本] custom model: total_cost=0.005 USD (手动指定)")

    trace.end(output={"summary": "cost tracking demo complete"})
    client.end()
    print("  [完成] 成本追踪\n")


if __name__ == "__main__":
    demonstrate_feedback_scoring()
    demonstrate_cost_tracking()