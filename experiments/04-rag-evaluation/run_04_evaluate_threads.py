"""
入口 4: 会话级（Thread）评测
=============================
前面 run_02 评测的是"单条问答对"；这里评测的是"整条多轮对话"质量，
比如对话是否连贯、用户是否表现出沮丧。这类指标作用在一整条 thread 上。

⚠️ 会话级指标都是 LLM 裁判，必须配置 LLM Key/模型，否则无法运行。
   故本脚本要求 RAG_EVAL_USE_LLM_METRICS=1，并提供可用的 judge 模型。

前置：先跑 run_03_feishu_threads.py 产生 thread 数据。

运行:
    RAG_EVAL_USE_LLM_METRICS=1 OPENAI_API_KEY=sk-... \
        uv run python experiments/04-rag-evaluation/run_04_evaluate_threads.py

看结果:
    Opik UI → Threads → 每条 thread 上会多出 coherence / frustration 反馈分
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from opik.evaluation import evaluate_threads  # noqa: E402
from opik.evaluation.metrics import (  # noqa: E402
    ConversationalCoherenceMetric,
    UserFrustrationMetric,
)

from rag_eval import settings  # noqa: E402


def main() -> None:
    print("=" * 60)
    print("[入口 4] 会话级 (Thread) 评测")
    print("=" * 60)

    if not settings.settings.use_llm_metrics:
        print("  [跳过] 会话级指标需要 LLM 裁判。")
        print("  请设置 RAG_EVAL_USE_LLM_METRICS=1 并配置 LLM Key 后重跑。")
        print("  例: RAG_EVAL_USE_LLM_METRICS=1 OPENAI_API_KEY=sk-... uv run python <本脚本>\n")
        return

    # 确保全局 client 指向本地 Opik（evaluate_threads 用 get_global_client）
    settings.make_client()

    judge_model = settings.settings.judge_model
    metrics = [
        ConversationalCoherenceMetric(model=judge_model),
        UserFrustrationMetric(model=judge_model),
    ]

    # filter_string=None → 评测该 project 下所有 thread。
    # 也可以用 OQL 精确指定，例如:
    #   filter_string='id = "feishu:oc_chat_alpha:om_root_alpha"'
    results = evaluate_threads(
        project_name=settings.settings.project,
        filter_string=None,
        eval_project_name=settings.settings.eval_project,
        metrics=metrics,
        # 把我们 feishu trace 的 input/output 结构抽成纯文本喂给指标
        trace_input_transform=lambda x: x["message"],
        trace_output_transform=lambda x: x["response"],
    )

    print(f"  [完成] 会话级评测结束: {results}")
    print(f"  [dashboard] Opik UI → Threads（评测结果写入 project: {settings.settings.eval_project}）\n")


if __name__ == "__main__":
    main()
