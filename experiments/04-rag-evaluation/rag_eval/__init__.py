"""
rag_eval — 可复用的 RAG / Agent 评测工具包
=============================================

本包把"如何用 Opik 评测一个 RAG/Agent 系统"拆成 5 个**可单独复用**的模块，
任何人都可以只 import 其中一块到自己的项目里：

    settings.py        — Opik 连接配置的单一真源（host/project/workspace）
    pipeline.py        — 一个零依赖的 mock RAG Agent（retrieve→generate），已用 @track 埋点
    dataset.py         — 构建评测集：get_or_create_dataset + insert 黄金问答对
    metrics.py         — 评测指标：离线启发式指标（默认，无需 LLM Key）+ LLM 裁判指标（可选）
    feishu_thread.py   — 把"同一个飞书 bot 会话线程"映射成"同一条 Opik thread"

设计原则（为什么这么拆）:
    1. 单一真源：所有 Opik 连接信息只在 settings.py 出现一次。
    2. 业务无关：pipeline/feishu_thread 不依赖 metrics，metrics 不依赖 pipeline，
       每块都能单独搬走。
    3. 离线可跑：默认指标不调用任何外部 LLM，只要本地 Opik Docker 在跑就能出数。
"""

from . import settings

__all__ = ["settings"]
