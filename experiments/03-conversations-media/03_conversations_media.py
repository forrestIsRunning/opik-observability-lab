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
        host="http://localhost:5173/api",
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
    多媒体附件: 3 种方式关联附件到 Trace/Span。
    文档原文: Attachment(data=..., file_name=..., content_type=...)
    """
    print("=" * 60)
    print("[实验 3.2] Media Attachment (方式1: span 创建时传入)")
    print("=" * 60)

    client = opik.Opik(
        project_name="opik-ob-experiment-03",
        host="http://localhost:5173/api",
        workspace="default",
    )

    # 方式 1: 在创建 span 时传入 attachments
    trace = client.trace(
        name="multi_modal_query",
        input={"question": "Analyze this image"},
        tags=["multi-modal", "attachment"],
    )

    from opik import Attachment

    attachment = Attachment(
        file_name="sample_diagram.png",
        data=b"fake_png_content_for_demonstration",
        content_type="image/png",
    )

    llm_span = trace.span(
        name="vision_analysis", type="llm",
        input={"image": "sample_diagram.png", "question": "Analyze this image"},
        model="gpt-4o", provider=opik.LLMProvider.OPENAI,
        attachments=[attachment],
    )
    llm_span.end(output={"analysis": "Architecture diagram..."},
                  usage={"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150})
    trace.end(output={"answer": "Analysis complete"})
    print("  [完成] 方式1: span 创建时传入附件\n")

    # 方式 2: 用低层 API 在 span 上附加（opik_context 需要 @track 装饰器）
    print("=" * 60)
    print("[实验 3.3] Media Attachment (方式2: 低层 API span 附件)")
    print("=" * 60)

    trace2 = client.trace(
        name="attachment_via_span",
        input={"task": "generate report"},
        tags=["attachment-lowlevel"],
    )

    report_bytes = b'{"result": "analysis complete", "confidence": 0.95}'
    report_span = client.span(
        trace_id=trace2.id,
        name="generate_report",
        type="general",
        input={"task": "generate"},
        attachments=[
            Attachment(
                data=report_bytes,
                file_name="report.json",
                content_type="application/json",
            )
        ],
    )
    report_span.end(output={"status": "report generated"})
    trace2.end(output={"status": "done"})
    print("  [完成] 方式2: 低层 API span 附件\n")

    # 方式 3: @track + opik_context (文档推荐方式)
    print("=" * 60)
    print("[实验 3.4] Media Attachment (方式3: @track + opik_context)")
    print("=" * 60)

    from opik import track, opik_context

    @track(name="process_with_attachment")
    def process_with_attachment(query: str) -> str:
        simulated_image = b"fake_image_bytes_from_http"
        opik_context.update_current_trace(
            attachments=[
                Attachment(
                    data=simulated_image,
                    file_name="remote_image.jpg",
                    content_type="image/jpeg",
                )
            ]
        )
        return "processed"

    result = process_with_attachment("analyze image")
    print(f"  [完成] 方式3: @track + opik_context ({result})")

    client.end()


if __name__ == "__main__":
    demonstrate_conversation_thread()
    demonstrate_media_attachment()