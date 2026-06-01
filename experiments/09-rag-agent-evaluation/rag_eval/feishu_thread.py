"""
飞书 Bot 会话线程 → Opik Thread 映射（本 demo 的核心可复用件）
================================================================
需求：同一个飞书 bot 会话线程里的多次提问，要在 Opik 里归到**同一条 thread**，
这样在 UI 的 Threads 页就能看到完整多轮对话、并能做会话级评测。

关键问题：Opik 的 thread_id 该用飞书的什么字段？

飞书侧的事实:
  - chat_id      : 会话（群/单聊）的 ID，形如 oc_xxx
  - message_id   : 单条消息 ID，形如 om_xxx（每条都不同，**不能**直接当 thread_id）
  - root_id      : 话题/回复链的根消息 ID。同一个"话题串"里所有回复共享同一个 root_id；
                   首条消息没有 root_id（它自己就是根）。

映射策略（thread_id_for）:
  - 话题群/回复串：用 root_id 作为线程标识（整串归一条 thread）。
  - 普通群聊/单聊（无 root_id）：退化用 chat_id（同一会话归一条 thread）。
  - 统一加 "feishu:" 前缀并带上 chat_id，保证：
      1) project 内唯一（Opik 要求 thread_id 在 project 内唯一）；
      2) 人看得懂来源。

复用方式：把 log_turn 接到你飞书 bot 的消息回调里，
每来一条消息就调一次，传入 chat_id / message_id / root_id 即可。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from . import pipeline, settings


def thread_id_for(chat_id: str, root_id: str | None = None) -> str:
    """由飞书会话信息推导出稳定、唯一、可读的 Opik thread_id。

    同一条回复串（root_id 相同）或同一会话（chat_id 相同）总是得到相同结果，
    因此多轮请求会自动归并到一条 Opik thread。
    """
    anchor = root_id or chat_id
    return f"feishu:{chat_id}:{anchor}"


@dataclass
class FeishuThreadTracer:
    """把飞书每一轮问答记录成一个 Opik Trace，并用 thread_id 串成一条对话。"""

    client: Any

    @classmethod
    def create(cls) -> "FeishuThreadTracer":
        return cls(client=settings.make_client())

    def log_turn(
        self,
        *,
        chat_id: str,
        message_id: str,
        user_text: str,
        root_id: str | None = None,
        user_open_id: str | None = None,
    ) -> dict[str, Any]:
        """记录一轮飞书问答。

        返回 {"thread_id", "trace_id", "answer"}，answer 可直接回复给飞书用户。

        注意：这里手动建 Trace（而不是用 @track），是因为飞书回调通常是
        "一条消息一次函数调用"，手动建 Trace 能精确控制 thread_id 与 metadata，
        且不依赖调用栈上下文。pipeline 内部的 retrieve/generate 仍由 @track 自动
        挂成子 span —— 但要让它们挂到这个手动 Trace 下，需用分布式上下文，
        本 demo 为保持简单，直接在 Trace 上记录答案；如需嵌套 span，见下方说明。
        """
        tid = thread_id_for(chat_id, root_id)

        trace = self.client.trace(
            name="feishu_turn",
            input={"message": user_text},
            thread_id=tid,
            metadata={
                "feishu_chat_id": chat_id,
                "feishu_message_id": message_id,
                "feishu_root_id": root_id,
                "feishu_user_open_id": user_open_id,
            },
            tags=["feishu", "production"],
        )

        # 检索 + 生成（手动建 span，确保挂在本 Trace 下）
        retrieve_span = trace.span(
            name="retrieve", type="tool", input={"question": user_text}
        )
        context = pipeline._retrieve_passages(user_text)
        retrieve_span.end(output={"hits": context, "hit_count": len(context)})

        gen_span = trace.span(
            name="generate",
            type="llm",
            input={"question": user_text, "context": context},
            model="mock-llm-v1",
        )
        answer = pipeline._generate_answer(user_text, context)
        gen_span.end(
            output={"answer": answer},
            usage={
                "prompt_tokens": len(user_text),
                "completion_tokens": len(answer),
                "total_tokens": len(user_text) + len(answer),
            },
        )

        trace.end(output={"response": answer})

        return {"thread_id": tid, "trace_id": trace.id, "answer": answer}

    def flush(self) -> None:
        """飞书 bot 长驻进程里，定期/退出前刷新，确保数据上报。"""
        self.client.flush()
