"""
一个零依赖的 mock RAG Agent
=============================
没有真实向量库/LLM，用一个小知识库 + 关键词检索 + 模板生成来"假装"一次 RAG。
目的：让评测流程能端到端跑起来，且每一步都用 @track 埋点，在 Opik 里呈现为:

    Trace: rag_agent
    ├── Span: retrieve   (type=tool)  检索
    └── Span: generate   (type=llm)   生成

返回的 dict 同时包含 output（答案）和 context（命中片段），
正好喂给 metrics.py 里的 ContextPrecision/Hallucination 等指标。

把这个文件换成你真实的 retrieve()/generate() 即可复用整套评测。
"""

from __future__ import annotations

from typing import Any

from opik import opik_context, track

# 极小知识库：每条用一组「有区分度」的关键词命中（故意不放 "opik"，
# 因为几乎每个问题都含 opik，放进去会污染匹配）。
_KNOWLEDGE_BASE: list[dict[str, Any]] = [
    {
        "keywords": ["可观测性", "平台", "observability"],
        "passage": (
            "Opik is an open-source LLM observability platform by Comet "
            "for tracing, evaluating and monitoring LLM apps."
        ),
        "answer": "Opik 是 Comet 开源的 LLM 可观测性平台，用于追踪、评测和监控 LLM 应用。",
    },
    {
        "keywords": ["trace", "span", "关系"],
        "passage": (
            "A Trace represents one end-to-end request; Spans are the "
            "nested steps inside a Trace."
        ),
        "answer": "Trace 代表一次端到端请求，Span 是 Trace 内部嵌套的步骤。",
    },
    {
        "keywords": ["thread", "多轮", "对话"],
        "passage": (
            "Passing the same thread_id to multiple traces groups them "
            "into one conversation thread."
        ),
        "answer": "给多个 Trace 传同一个 thread_id，就能把它们归到同一条对话线程。",
    },
    {
        "keywords": ["dataset", "experiment", "评测集"],
        "passage": (
            "An Opik Dataset holds golden items; evaluate() runs a task "
            "over it and creates an Experiment."
        ),
        "answer": "Opik Dataset 存放黄金样本，evaluate() 在其上运行任务并生成一个 Experiment。",
    },
    {
        "keywords": ["指标", "rag", "metric"],
        "passage": (
            "Opik ships RAG metrics like ContextPrecision, ContextRecall, "
            "AnswerRelevance and Hallucination."
        ),
        "answer": "Opik 内置 ContextPrecision、ContextRecall、AnswerRelevance、Hallucination 等 RAG 指标。",
    },
]


# ── 纯逻辑（无埋点）──────────────────────────────────────────────
# 抽出来是为了让两种调用方式都能复用同一套检索/生成逻辑：
#   1) 下面的 @track 包装版本（evaluate 场景，自动建 span）
#   2) feishu_thread.py 里手动建 span 的版本（飞书回调场景）


def _retrieve_passages(question: str, top_k: int = 2) -> list[str]:
    """玩具检索器：按"关键词是否作为子串出现在问题里"打分，返回命中片段。

    用子串匹配（而非按空白切词）是因为中文不靠空格分词，
    "指标" 这种关键词要能命中 "Opik有哪些RAG指标" 这类问题。
    """
    q = question.lower()

    scored: list[tuple[int, str]] = []
    for entry in _KNOWLEDGE_BASE:
        hits = sum(1 for kw in entry["keywords"] if kw.lower() in q)
        if hits > 0:
            scored.append((hits, entry["passage"]))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [passage for _, passage in scored[:top_k]]


def _generate_answer(question: str, context: list[str]) -> str:
    """模板生成器：把命中片段拼成答案。真实场景这里是一次 LLM 调用。"""
    if not context:
        return "抱歉，知识库中没有找到相关内容。"
    # 用第一个命中片段对应的标准答案（模拟"基于 context 生成"）
    return next(
        (
            entry["answer"]
            for entry in _KNOWLEDGE_BASE
            if entry["passage"] == context[0]
        ),
        context[0],
    )


# ── @track 包装版本（evaluate 场景用）───────────────────────────


@track(name="retrieve", type="tool")
def retrieve(question: str, top_k: int = 2) -> list[str]:
    passages = _retrieve_passages(question, top_k=top_k)
    opik_context.update_current_span(
        metadata={"top_k": top_k, "hit_count": len(passages)},
    )
    return passages


@track(name="generate", type="llm")
def generate(question: str, context: list[str]) -> str:
    answer = _generate_answer(question, context)
    # 模拟 token 用量，方便在 Opik 看 cost/usage
    opik_context.update_current_span(
        model="mock-llm-v1",
        usage={
            "prompt_tokens": len(question) + sum(len(c) for c in context),
            "completion_tokens": len(answer),
            "total_tokens": len(question) + sum(len(c) for c in context) + len(answer),
        },
    )
    return answer


@track(name="rag_agent")
def rag_agent(question: str, thread_id: str | None = None) -> dict[str, Any]:
    """端到端 RAG：retrieve → generate。

    返回 dict 的 key 故意对齐 Opik 指标的 score() 参数：
        output  → 答案
        context → 命中片段列表
    这样 evaluate() 把"数据集 item + 任务输出"合并后能直接喂给指标。
    """
    if thread_id is not None:
        # 让这次请求归属到某条对话线程（飞书 bot 多轮场景见 feishu_thread.py）
        opik_context.update_current_trace(thread_id=thread_id)

    context = retrieve(question)
    answer = generate(question, context)
    return {"output": answer, "context": context}
