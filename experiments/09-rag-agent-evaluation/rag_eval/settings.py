"""
Opik 连接配置 — 单一真源
==========================
所有实验脚本只从这里取 Opik 的连接参数，避免每个文件硬编码 host/project。

环境变量（都有默认值，本地开箱即用）:
    OPIK_HOST           Opik REST 地址（默认本地 Docker: http://localhost:5173/api）
    OPIK_WORKSPACE      工作区（本地默认 "default"）
    OPIK_PROJECT        traces 落到哪个 project（默认 "rag-agent-eval"）
    OPIK_EVAL_PROJECT   线程评测结果落到哪个 project（默认 在主 project 后加 -threads）

    RAG_EVAL_USE_LLM_METRICS  设为 "1"/"true" 时启用 LLM 裁判指标（需要下方 LLM Key）。
                              默认关闭 → 只跑离线启发式指标，无需任何外部 Key。
    RAG_EVAL_JUDGE_MODEL      LLM 裁判用的模型名（LiteLLM 格式，默认 gpt-4o-mini）。
"""

from __future__ import annotations

import os
from dataclasses import dataclass


def _env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class OpikSettings:
    host: str
    workspace: str
    project: str
    eval_project: str
    use_llm_metrics: bool
    judge_model: str

    @classmethod
    def from_env(cls) -> "OpikSettings":
        project = os.getenv("OPIK_PROJECT", "rag-agent-eval")
        return cls(
            host=os.getenv("OPIK_HOST", "http://localhost:5173/api"),
            workspace=os.getenv("OPIK_WORKSPACE", "default"),
            project=project,
            eval_project=os.getenv("OPIK_EVAL_PROJECT", f"{project}-threads"),
            use_llm_metrics=_env_bool("RAG_EVAL_USE_LLM_METRICS", default=False),
            judge_model=os.getenv("RAG_EVAL_JUDGE_MODEL", "gpt-4o-mini"),
        )


settings = OpikSettings.from_env()


def make_client(project_name: str | None = None):
    """构造一个 Opik 客户端。project_name 不传则用全局默认 project。

    单独抽出来是为了：所有脚本用同一套 host/workspace，且 set_global_client
    后 evaluate()/evaluate_threads() 也能复用同一连接。
    """
    import opik

    client = opik.Opik(
        project_name=project_name or settings.project,
        host=settings.host,
        workspace=settings.workspace,
    )
    # 让 @track 装饰器和 evaluate() 默认走这个 client
    opik.set_global_client(client)
    return client
