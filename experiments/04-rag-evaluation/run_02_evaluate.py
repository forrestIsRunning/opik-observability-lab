"""
入口 2: 在评测集上跑评测（生成 Experiment，即 dashboard 数据来源）
===================================================================
evaluate() 做的事:
  1. 遍历数据集每一条 item
  2. 对每条 item 调用 task(item) → 得到 {output, context}（这里就是跑一次 RAG）
  3. 用 scoring_metrics 给每条结果打分
  4. 把所有结果汇总成一个 Experiment，写回 Opik

task 函数签名固定为 task(dataset_item: dict) -> dict。
返回的 dict 会和 dataset_item 合并后喂给每个 metric 的 score(...)。

运行:
    # 默认：只跑离线指标，无需任何 LLM Key
    uv run python experiments/04-rag-evaluation/run_02_evaluate.py

    # 可选：额外启用 LLM 裁判指标（需要 LLM Key）
    RAG_EVAL_USE_LLM_METRICS=1 OPENAI_API_KEY=sk-... \
        uv run python experiments/04-rag-evaluation/run_02_evaluate.py

看结果（这就是 "dashboard"）:
    Opik UI → Experiments → 找到本次 experiment → 看每条样本的分数、平均分、趋势
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from opik import evaluate  # noqa: E402

from rag_eval import dataset as dataset_module  # noqa: E402
from rag_eval import metrics as metrics_module  # noqa: E402
from rag_eval import pipeline, settings  # noqa: E402


def rag_task(dataset_item: dict[str, Any]) -> dict[str, Any]:
    """评测任务：对一条数据集样本跑一次 RAG。

    dataset_item 含 input / expected_output；我们只用 input 去跑系统，
    返回 output + context 供指标打分（expected_output 由引擎自动并入）。
    """
    result = pipeline.rag_agent(dataset_item["input"])
    return {"output": result["output"], "context": result["context"]}


def main() -> None:
    print("=" * 60)
    print("[入口 2] 运行 RAG 评测实验")
    print("=" * 60)

    # 确保连接 + 数据集就绪（make_client 内部 set_global_client，evaluate 会复用）
    settings.make_client()
    dataset = dataset_module.build_dataset()

    metrics = metrics_module.build_metrics()
    print(f"  [指标] {[m.name for m in metrics]}")
    print(f"  [LLM裁判] {'已启用' if settings.settings.use_llm_metrics else '未启用（仅离线指标）'}")

    result = evaluate(
        dataset=dataset,
        task=rag_task,
        scoring_metrics=metrics,
        experiment_name=f"rag-eval-{datetime.now():%Y%m%d-%H%M%S}",
        experiment_config={
            "system": "mock-rag-agent",
            "retriever": "keyword-overlap",
            "generator": "template",
        },
        project_name=settings.settings.project,
        task_threads=1,  # 单线程，输出顺序稳定，方便 demo 观察
    )

    # evaluate 在 verbose=1 时已打印每条样本汇总表；这里再给跳转信息
    print(f"  [完成] 实验已生成: {result.experiment_name}")
    if result.experiment_url:
        print(f"  [dashboard] {result.experiment_url}")
    print("  [dashboard] 或打开 Opik UI → Experiments 查看分数与趋势\n")


if __name__ == "__main__":
    main()
