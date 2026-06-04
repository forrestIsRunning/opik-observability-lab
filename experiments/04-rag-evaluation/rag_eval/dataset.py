"""
构建评测集（Evaluation Dataset）
=================================
评测集 = 一组"黄金样本"。每条样本至少要有:
    input            用户问题
    expected_output  标准答案（人工/专家给定）

注意：我们**故意不**在样本里放 context。
原因：检索到的 context 是"被评测对象"产出的（见 pipeline.retrieve），
应该由评测时的 task 实时产生，而不是写死在数据集里。
这样 ContextPrecision/Recall 才能真正衡量"你的检索好不好"。

复用方式：把 GOLDEN_ITEMS 换成你自己的问答对，或改 build_dataset 从 CSV/JSON 读。
"""

from __future__ import annotations

from typing import Any

from . import settings

DATASET_NAME = "rag-agent-golden-qa"

# 黄金问答对。answer 来自 pipeline 知识库，保证 mock 系统"应当答对"。
GOLDEN_ITEMS: list[dict[str, Any]] = [
    {
        "input": "什么是 Opik 可观测性平台?",
        "expected_output": "Opik 是 Comet 开源的 LLM 可观测性平台，用于追踪、评测和监控 LLM 应用。",
        "category": "concept",
    },
    {
        "input": "Trace 和 Span 是什么关系?",
        "expected_output": "Trace 代表一次端到端请求，Span 是 Trace 内部嵌套的步骤。",
        "category": "concept",
    },
    {
        "input": "怎么把多轮对话归到一条 thread?",
        "expected_output": "给多个 Trace 传同一个 thread_id，就能把它们归到同一条对话线程。",
        "category": "howto",
    },
    {
        "input": "dataset 和 experiment 怎么配合?",
        "expected_output": "Opik Dataset 存放黄金样本，evaluate() 在其上运行任务并生成一个 Experiment。",
        "category": "howto",
    },
    {
        "input": "Opik 有哪些 RAG 指标?",
        "expected_output": (
            "Opik 内置 ContextPrecision、ContextRecall、AnswerRelevance、"
            "Hallucination 等 RAG 指标。"
        ),
        "category": "concept",
    },
]


def build_dataset(items: list[dict[str, Any]] | None = None):
    """创建（或复用）评测集并写入样本。

    - get_or_create_dataset 是幂等的：脚本重复跑不会报错。
    - dataset.insert 内部按内容哈希去重：同样的样本不会插两遍。
    返回 Dataset 对象，供 evaluate() 使用。
    """
    client = settings.make_client()
    dataset = client.get_or_create_dataset(
        name=DATASET_NAME,
        description="RAG/Agent 评测黄金问答集（demo）",
    )
    dataset.insert(items if items is not None else GOLDEN_ITEMS)
    return dataset
