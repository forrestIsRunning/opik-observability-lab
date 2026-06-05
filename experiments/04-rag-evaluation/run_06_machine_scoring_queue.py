"""
入口 6: 机器评分（自定义规则）+ 标注队列
==========================================
生产里常见闭环：
  1. 机器先用规则给每条 trace 打分（便宜、快、确定性）→ 写回 feedback score
  2. 把"规则没过"的 trace 自动塞进**标注队列**，交给人工复核
  3. 人在 Opik UI 的 Annotation Queue 里逐条打人工分

涉及 API（均已核对签名）:
    client.trace(...).end(...)                          产生 trace
    client.log_traces_feedback_scores([{id,name,value}])  机器分写回
    client.create_traces_annotation_queue(name, ...)    建标注队列
    queue.add_traces([trace, ...])                      把待复核 trace 入队

运行:
    uv run python experiments/04-rag-evaluation/run_06_machine_scoring_queue.py

看结果:
    - Opik UI → 该 trace → Feedback scores 看到 rule_* 机器分
    - Opik UI → Annotation Queues → 看到待人工复核的队列
"""

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rag_eval import machine_scoring as ms  # noqa: E402
from rag_eval import pipeline, settings  # noqa: E402

# 故意混入一个"知识库答不出"的问题，触发拒答 → 规则不过 → 入队复核
QUESTIONS = [
    "什么是 Opik 可观测性平台?",
    "Trace 和 Span 是什么关系?",
    "请问今天上海的天气怎么样?",  # 知识库无关 → 拒答
]


def main() -> None:
    print("=" * 60)
    print("[入口 6] 机器评分（自定义规则）+ 标注队列")
    print("=" * 60)

    client = settings.make_client()

    needs_review = []  # 规则未全过的 trace，待人工复核
    for q in QUESTIONS:
        # 手动建 trace 以便拿到 trace_id 来写 feedback score
        trace = client.trace(name="scored_turn", input={"question": q}, tags=["machine-scored"])
        ctx = pipeline._retrieve_passages(q)
        ans = pipeline._generate_answer(q, ctx)
        trace.end(output={"answer": ans})

        payload = {"output": ans, "context": ctx}
        rule_scores = ms.score_payload(payload)
        client.log_traces_feedback_scores(ms.to_feedback_scores(trace.id, rule_scores))

        failed = [rs.name for rs in rule_scores if not rs.passed]
        flag = "✅ 全过" if not failed else f"⚠️ 未过: {failed}"
        print(f"\n  Q: {q}")
        print(f"    A: {ans[:36]}")
        print(f"    机器分: {[(rs.name, rs.value) for rs in rule_scores]}")
        print(f"    {flag}")
        if failed:
            needs_review.append(trace)

    # 把未过规则的 trace 路由到人工标注队列
    print("\n  [路由] 把规则未过的 trace 送人工复核队列")
    if needs_review:
        queue = client.create_traces_annotation_queue(
            name=f"rag-review-{datetime.now():%Y%m%d-%H%M%S}",
            description="机器规则未通过、需人工复核的 RAG 回答",
            instructions="请检查答案是否应当拒答，并对 helpfulness 打分。",
            feedback_definition_names=["helpfulness"],
        )
        queue.add_traces(needs_review)
        print(f"    [完成] 队列 '{queue.name}' (id={queue.id})，已入队 {len(needs_review)} 条")
        print("    [复核] Opik UI → Annotation Queues 打开该队列逐条人工打分")
    else:
        print("    [跳过] 本批全部通过规则，无需人工复核")

    client.flush()
    print("\n  [完成] 机器评分 + 标注队列闭环演示结束\n")


if __name__ == "__main__":
    main()
