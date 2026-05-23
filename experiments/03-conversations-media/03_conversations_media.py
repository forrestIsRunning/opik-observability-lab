"""
实验 03: Log Conversations & Media Attachments
===============================================
多轮对话关联 + 文件附件上传。

运行方式:
    uv run python experiments/03-conversations-media/03_conversations_media.py
"""

import uuid
import opik


def demonstrate_conversation_thread():
    """
    多轮对话: 用 thread_id 把多轮 Trace 关联为一条对话。
    """
    print("=" * 60)
    print("[实验 3.1] 多轮对话线程")
    print("=" * 60)

    client = opik.Opik(
        project_name="opik-ob-experiment-03",
        host="http://localhost:5173",
        workspace="default",
    )

    thread_id = f"chat_{uuid.uuid4().hex[:12]}"

    conversation = [
        {"turn": 1, "user": "What is LLM observability?", "assistant": "LLM observability is the practice of monitoring..."},
        {"turn": 2, "user": "Why is it important?", "assistant": "It helps debug, evaluate, and improve LLM applications."},
        {"turn": 3, "user": "What tools support it?", "assistant": "Opik, Langfuse, Weights & Biases, and others."},
    ]

    for turn in conversation:
        trace = client.trace(
            name=f"turn_{turn['turn']}",
            input={"message": turn["user"]},
            thread_id=thread_id,
            metadata={"turn_number": turn["turn"]},
            tags=["conversation", "multi-turn"],
        )

        # LLM 调用 span
        llm_span = trace.span(
            name="llm_response",
            type="llm",
            input={"messages": [{"role": "user", "content": turn["user"]}]},
            model="gpt-4",
            provider=opik.LLMProvider.OPENAI,
        )
        llm_span.end(
            output={"content": turn["assistant"]},
            usage={"prompt_tokens": 20, "completion_tokens": 15, "total_tokens": 35},
        )

        trace.end(output={"response": turn["assistant"]})
        print(f"  [轮次 {turn['turn']}] 已记录")

    client.end()
    print(f"  [完成] 3 轮对话通过 thread_id={thread_id} 关联\n")


def demonstrate_media_attachment():
    """
    在 Span 上附加媒体文件 (Attachment)。
    生成一个模拟的图片内容来演示。
    """
    print("=" * 60)
    print("[实验 3.2] Media Attachment")
    print("=" * 60)

    client = opik.Opik(
        project_name="opik-ob-experiment-03",
        host="http://localhost:5173",
        workspace="default",
    )

    trace = client.trace(
        name="multi_modal_query",
        input={"question": "Analyze this image"},
        tags=["multi-modal", "attachment"],
    )

    # 创建一个模拟的图片附件
    # 在实际场景中, 这里可以是上传的图片文件
    from opik.api_objects.attachment import Attachment

    attachment = Attachment(
        file_name="sample_diagram.png",
        file_content=b"fake_png_content_for_demonstration",
        mime_type="image/png",
    )

    # 在创建 span 时传入 attachments
    llm_span = trace.span(
        name="vision_analysis",
        type="llm",
        input={"image": "sample_diagram.png", "question": "Analyze this image"},
        model="gpt-4o",
        provider=opik.LLMProvider.OPENAI,
        attachments=[attachment],
    )
    llm_span.end(
        output={"analysis": "This is a diagram showing the architecture..."},
        usage={"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150},
    )

    trace.end(output={"answer": "Analysis complete"})
    print("  [完成] 附件已关联到 span (mime_type=image/png)")

    client.end()


if __name__ == "__main__":
    demonstrate_conversation_thread()
    demonstrate_media_attachment()