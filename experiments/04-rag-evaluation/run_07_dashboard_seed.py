"""
入口 7: 项目级 Dashboard 自定义（数据准备 + UI 配置指南）
=========================================================
重要认知：Opik 的 Dashboard / Insights 是在 **UI 里配置**的（没有建 widget 的 SDK）。
SDK 的职责是**喂数据**：把 trace 的 metadata / tags / feedback_scores 结构化地打上，
UI 的 widget 才能按这些维度做"自定义"图表（按 model 分组、按 tag 过滤、看 quality 趋势）。

本脚本做两件事:
  1. 造一批结构规整的 trace（多种 model / route / env + 多个 feedback 分 + 偶发错误）
  2. 打印"在 UI 里如何配置自定义 widget"的对照清单

涉及 API:
    client.trace(metadata=..., tags=...)               维度数据
    trace.span(... usage=...)                          token / cost
    client.log_traces_feedback_scores([...])           feedback 分（趋势/分布）

运行:
    uv run python experiments/04-rag-evaluation/run_07_dashboard_seed.py

看结果:
    Opik UI → 项目 rag-agent-eval → Insights 标签 → Add new 自建视图，
    按下方打印的"widget 配方"添加 Time series / Single metric 等 widget。
"""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rag_eval import pipeline, settings  # noqa: E402

MODELS = ["mock-llm-v1", "mock-llm-pro"]
ROUTES = ["feishu", "web", "api"]
ENVS = ["production", "staging"]
QUESTIONS = [
    "什么是 Opik 可观测性平台?",
    "Trace 和 Span 是什么关系?",
    "Opik 有哪些 RAG 指标?",
    "dataset 和 experiment 怎么配合?",
    "怎么把多轮对话归到一条 thread?",
]


def main() -> None:
    print("=" * 60)
    print("[入口 7] 项目级 Dashboard 自定义（造数据 + UI 指南）")
    print("=" * 60)

    client = settings.make_client()
    rng = random.Random(42)  # 固定种子，结果可复现

    n = 24
    print(f"  [造数] 生成 {n} 条带维度的 trace ...")
    for i in range(n):
        q = rng.choice(QUESTIONS)
        model = rng.choice(MODELS)
        route = rng.choice(ROUTES)
        env = rng.choice(ENVS)

        trace = client.trace(
            name="dashboard_request",
            input={"question": q},
            metadata={"model": model, "route": route, "environment": env},
            tags=[route, env, model],
        )

        ctx = pipeline._retrieve_passages(q)
        ans = pipeline._generate_answer(q, ctx)

        span = trace.span(
            name="generate", type="llm", input={"q": q}, model=model,
        )
        # 偶发错误，方便演示 "Has error" 维度
        is_error = rng.random() < 0.15
        if is_error:
            span.end(error_info={"exception_type": "TimeoutError", "message": "judge timeout",
                                  "traceback": "..."})
            trace.end(output={"answer": ""}, error_info={"exception_type": "TimeoutError",
                                                          "message": "timeout", "traceback": "..."})
        else:
            span.end(
                output={"answer": ans},
                usage={"prompt_tokens": rng.randint(20, 80),
                       "completion_tokens": rng.randint(10, 60),
                       "total_tokens": rng.randint(40, 140)},
            )
            trace.end(output={"answer": ans})

        # 三个 feedback 分：quality / groundedness / latency_ok
        if not is_error:
            client.log_traces_feedback_scores([
                {"id": trace.id, "name": "quality", "value": round(rng.uniform(0.6, 1.0), 2)},
                {"id": trace.id, "name": "groundedness", "value": round(rng.uniform(0.5, 1.0), 2)},
                {"id": trace.id, "name": "latency_ok", "value": 1.0 if rng.random() > 0.2 else 0.0},
            ])

    client.flush()
    print(f"  [完成] 已写入 {n} 条 trace（含 metadata/tags/usage/feedback）\n")

    print("  ┌─ 如何在 UI 配置自定义 widget（项目 Insights → Add new）──────────")
    print("  │ 1) Time series：Metric=Trace feedback scores，选 quality，")
    print("  │    Breakdown=Metadata key → model  ⇒ 看不同模型的质量趋势")
    print("  │ 2) Time series：Metric=Estimated cost，Breakdown=Tags ⇒ 各 route 成本")
    print("  │ 3) Single metric：Average feedback scores → groundedness ⇒ 关键 KPI 卡")
    print("  │ 4) Time series：Metric=Number of traces，Breakdown=Has error ⇒ 错误率")
    print("  │ 5) 过滤器：metadata.environment = \"production\" ⇒ 只看线上")
    print("  └────────────────────────────────────────────────────────────────")
    print()


if __name__ == "__main__":
    main()
