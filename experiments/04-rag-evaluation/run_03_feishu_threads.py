"""
入口 3: 模拟飞书 Bot 多轮会话 → Opik Thread
=============================================
模拟两个飞书会话，每个会话里用户连问几轮。
关键：同一会话的多轮请求共享同一个 thread_id，在 Opik 里归为一条 thread。

真实接入：把 FeishuThreadTracer.log_turn 接到你飞书 bot 的 im.message.receive
事件回调里，传入事件里的 chat_id / message_id / root_id 即可。

运行:
    uv run python experiments/04-rag-evaluation/run_03_feishu_threads.py

看结果:
    Opik UI → Threads → 能看到两条独立 thread，各自含多轮对话
    （记下打印出的 thread_id，下一步 run_04 会用它做会话级评测）
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rag_eval.feishu_thread import FeishuThreadTracer  # noqa: E402

# 两个模拟会话。会话 A 是"回复话题串"（带 root_id），会话 B 是普通单聊（无 root_id）。
SIMULATED_CHATS = [
    {
        "chat_id": "oc_chat_alpha",
        "root_id": "om_root_alpha",  # 整串回复归一条 thread
        "turns": [
            ("om_msg_a1", "什么是 Opik 可观测性平台?"),
            ("om_msg_a2", "那 Trace 和 Span 是什么关系?"),
            ("om_msg_a3", "怎么把多轮对话归到一条 thread?"),
        ],
    },
    {
        "chat_id": "oc_chat_beta",
        "root_id": None,  # 无话题串 → 退化用 chat_id 归并
        "turns": [
            ("om_msg_b1", "Opik 有哪些 RAG 指标?"),
            ("om_msg_b2", "dataset 和 experiment 怎么配合?"),
        ],
    },
]


def main() -> None:
    print("=" * 60)
    print("[入口 3] 模拟飞书 Bot 多轮会话 → Opik Thread")
    print("=" * 60)

    tracer = FeishuThreadTracer.create()
    seen_threads: set[str] = set()

    for chat in SIMULATED_CHATS:
        print(f"\n  [会话] chat_id={chat['chat_id']} root_id={chat['root_id']}")
        for message_id, text in chat["turns"]:
            res = tracer.log_turn(
                chat_id=chat["chat_id"],
                message_id=message_id,
                user_text=text,
                root_id=chat["root_id"],
                user_open_id="ou_demo_user",
            )
            seen_threads.add(res["thread_id"])
            print(f"    Q: {text}")
            print(f"    A: {res['answer']}")
            print(f"    └─ thread_id={res['thread_id']}  trace_id={res['trace_id']}")

    tracer.flush()

    print("\n  [完成] 生成的 thread_id（run_04 评测会用到）:")
    for tid in sorted(seen_threads):
        print(f"    - {tid}")
    print("  [下一步] 运行 run_04_evaluate_threads.py 做会话级评测\n")


if __name__ == "__main__":
    main()
