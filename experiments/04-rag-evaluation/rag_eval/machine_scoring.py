"""
机器评分 — 自定义规则
======================
"机器评分"= 用代码规则（而非人工、也不一定用 LLM）给每条 trace 打分，
再把分数写回 Opik 作为 feedback score。低分的样本可路由到标注队列给人复核。

这里的规则都是**纯函数**，确定性强、零依赖、可单测：
    rule_answer_non_empty   答案非空
    rule_has_context        检索到了 context
    rule_min_length         答案长度达标
    rule_not_refusal        答案不是"抱歉没找到"这类拒答

每条规则签名统一为 rule(payload: dict) -> RuleScore，
payload 至少含 {"output": str, "context": list[str]}（即 pipeline.rag_agent 的返回）。

复用方式：把 DEFAULT_RULES 换成你的业务规则（如"必须包含引用""不得出现敏感词"）。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

_REFUSAL_MARKERS = ("抱歉", "没有找到", "无法回答", "i don't know", "cannot")


@dataclass(frozen=True)
class RuleScore:
    name: str
    value: float  # 1.0 = 通过, 0.0 = 不通过
    reason: str

    @property
    def passed(self) -> bool:
        return self.value >= 1.0


def rule_answer_non_empty(payload: dict[str, Any]) -> RuleScore:
    out = (payload.get("output") or "").strip()
    ok = len(out) > 0
    return RuleScore("rule_answer_non_empty", 1.0 if ok else 0.0,
                     "答案非空" if ok else "答案为空")


def rule_has_context(payload: dict[str, Any]) -> RuleScore:
    ctx = payload.get("context") or []
    ok = len(ctx) > 0
    return RuleScore("rule_has_context", 1.0 if ok else 0.0,
                     f"检索到 {len(ctx)} 条" if ok else "未检索到任何 context")


def rule_min_length(payload: dict[str, Any], min_len: int = 8) -> RuleScore:
    out = (payload.get("output") or "").strip()
    ok = len(out) >= min_len
    return RuleScore("rule_min_length", 1.0 if ok else 0.0,
                     f"长度 {len(out)} >= {min_len}" if ok else f"长度 {len(out)} < {min_len}")


def rule_not_refusal(payload: dict[str, Any]) -> RuleScore:
    out = (payload.get("output") or "").lower()
    is_refusal = any(m in out for m in _REFUSAL_MARKERS)
    return RuleScore("rule_not_refusal", 0.0 if is_refusal else 1.0,
                     "命中拒答措辞" if is_refusal else "正常作答")


# 规则集：函数列表，每个吃 payload 出 RuleScore
DEFAULT_RULES: list[Callable[[dict[str, Any]], RuleScore]] = [
    rule_answer_non_empty,
    rule_has_context,
    rule_min_length,
    rule_not_refusal,
]


def score_payload(
    payload: dict[str, Any],
    rules: list[Callable[[dict[str, Any]], RuleScore]] | None = None,
) -> list[RuleScore]:
    """对一条结果按所有规则打分，返回 RuleScore 列表。"""
    return [rule(payload) for rule in (rules or DEFAULT_RULES)]


def to_feedback_scores(trace_id: str, rule_scores: list[RuleScore]) -> list[dict[str, Any]]:
    """把 RuleScore 转成 client.log_traces_feedback_scores 需要的 dict 列表。"""
    return [
        {"id": trace_id, "name": rs.name, "value": rs.value, "reason": rs.reason}
        for rs in rule_scores
    ]
