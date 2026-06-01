"""
评测指标
=========
分两类：

A) 离线启发式指标（默认启用，**不调用任何外部 LLM**）
   - ContextHitRate   : 检索片段里是否包含期望答案的关键词 → 衡量"检索召回"
   - AnswerCoverage   : 模型答案覆盖了多少期望答案的关键词 → 衡量"答案正确性"
   这两个指标只做字符串/集合运算，确定性强，只要 Opik Docker 在跑就能出数。

B) LLM 裁判指标（可选，settings.use_llm_metrics=True 时启用）
   直接复用 Opik 内置的 ContextPrecision / ContextRecall / AnswerRelevance / Hallucination。
   它们默认用 LiteLLMChatModel，需要 LLM Key（OPENAI_API_KEY 或本地 litellm 代理）。

自定义指标只需继承 BaseMetric 并实现 score(...) 返回 ScoreResult。
score 的参数名要和"数据集 item + task 输出"合并后的 key 对得上：
    input / expected_output  来自数据集 item
    output / context         来自 task（pipeline.rag_agent）的返回
"""

from __future__ import annotations

import re
from typing import Any

from opik.evaluation.metrics import base_metric, score_result

from . import settings

# 去掉中英文标点，按空白和单字切分出"词"用于重叠比较
_TOKEN_RE = re.compile(r"[\w一-鿿]+", re.UNICODE)


def _tokens(text: str) -> set[str]:
    """把一段文本切成小写 token 集合（英文按词，中文按连续汉字串）。"""
    if not text:
        return set()
    return {t.lower() for t in _TOKEN_RE.findall(text)}


class ContextHitRate(base_metric.BaseMetric):
    """检索质量（离线）：期望答案的关键词有多少出现在检索到的 context 里。

    score(expected_output, context) → 0.0~1.0
    高 = 检索回来的片段确实覆盖了答案所需信息。
    """

    def __init__(self, name: str = "context_hit_rate", track: bool = True) -> None:
        super().__init__(name=name, track=track)

    def score(
        self,
        expected_output: str,
        context: list[str] | None = None,
        **ignored_kwargs: Any,
    ) -> score_result.ScoreResult:
        expected_tokens = _tokens(expected_output)
        if not expected_tokens:
            return score_result.ScoreResult(
                value=0.0, name=self.name, reason="expected_output 为空"
            )

        context_tokens: set[str] = set()
        for chunk in context or []:
            context_tokens |= _tokens(chunk)

        hit = len(expected_tokens & context_tokens) / len(expected_tokens)
        return score_result.ScoreResult(
            value=hit,
            name=self.name,
            reason=f"期望词 {len(expected_tokens)} 个，命中 {round(hit * len(expected_tokens))} 个",
        )


class AnswerCoverage(base_metric.BaseMetric):
    """答案质量（离线）：模型答案覆盖了多少期望答案的关键词。

    score(expected_output, output) → 0.0~1.0
    高 = 生成的答案和标准答案重合度高。
    """

    def __init__(self, name: str = "answer_coverage", track: bool = True) -> None:
        super().__init__(name=name, track=track)

    def score(
        self,
        expected_output: str,
        output: str,
        **ignored_kwargs: Any,
    ) -> score_result.ScoreResult:
        expected_tokens = _tokens(expected_output)
        if not expected_tokens:
            return score_result.ScoreResult(
                value=0.0, name=self.name, reason="expected_output 为空"
            )

        output_tokens = _tokens(output)
        coverage = len(expected_tokens & output_tokens) / len(expected_tokens)
        return score_result.ScoreResult(
            value=coverage,
            name=self.name,
            reason=f"答案覆盖期望关键词 {round(coverage * 100)}%",
        )


def build_metrics() -> list[base_metric.BaseMetric]:
    """组装本次评测要用的指标列表。

    默认只返回离线指标；当 settings.use_llm_metrics=True 时，
    追加 Opik 内置的 LLM 裁判指标（需要 LLM Key）。
    """
    metrics: list[base_metric.BaseMetric] = [
        ContextHitRate(),
        AnswerCoverage(),
    ]

    if settings.settings.use_llm_metrics:
        from opik.evaluation.metrics import (
            AnswerRelevance,
            ContextPrecision,
            ContextRecall,
            Hallucination,
        )

        model = settings.settings.judge_model
        metrics.extend(
            [
                # 需要 input/output/expected_output/context
                ContextPrecision(model=model),
                ContextRecall(model=model),
                # 需要 input/output/context（注意：没有 expected_output）
                AnswerRelevance(model=model),
                Hallucination(model=model),
            ]
        )

    return metrics
