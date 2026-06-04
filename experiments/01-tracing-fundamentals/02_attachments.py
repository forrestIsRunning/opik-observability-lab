"""
实验 02: Media Attachments — 3 种上传方式
==========================================
运行方式:
    uv run python experiments/01-tracing-fundamentals/02_attachments.py
"""

import opik
from opik import Attachment, LLMProvider, opik_context, track

CLIENT_KWARGS = dict(
    project_name="opik-ob-experiment-01-attach",
    host="http://localhost:5173/api",
    workspace="default",
)


def attachment_via_span_arg():
    """方式1: 在 span() 调用时直接传入 attachments 列表."""
    print("=" * 60)
    print("[2.1] 方式1: span 创建时传入 attachments")
    print("=" * 60)

    client = opik.Opik(**CLIENT_KWARGS)

    trace = client.trace(
        name="multi_modal_query",
        input={"question": "Analyze this image"},
        tags=["attachment", "multi-modal"],
    )

    span = trace.span(
        name="vision_analysis",
        type="llm",
        input={"image": "sample_diagram.png", "question": "Analyze this image"},
        model="gpt-4o",
        provider=LLMProvider.OPENAI,
        attachments=[
            Attachment(
                data=b"fake_png_content_for_demonstration",
                file_name="sample_diagram.png",
                content_type="image/png",
            )
        ],
    )
    span.end(
        output={"analysis": "Architecture diagram..."},
        usage={"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150},
    )
    trace.end(output={"answer": "Analysis complete"})

    client.end(timeout=30, flush=True)
    print("  ✓ done\n")


def attachment_via_client_span():
    """方式2: 用 client.span() 低层 API 创建带附件的 Span."""
    print("=" * 60)
    print("[2.2] 方式2: client.span() 低层 API")
    print("=" * 60)

    client = opik.Opik(**CLIENT_KWARGS)

    trace = client.trace(
        name="attachment_via_client_span",
        input={"task": "generate report"},
        tags=["attachment"],
    )

    report_bytes = b'{"result": "analysis complete", "confidence": 0.95}'
    span = client.span(
        trace_id=trace.id,
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
    span.end(output={"status": "report generated"})
    trace.end(output={"status": "done"})

    client.end(timeout=30, flush=True)
    print("  ✓ done\n")


def attachment_via_opik_context():
    """方式3: @track 装饰器 + opik_context.update_current_trace()."""
    print("=" * 60)
    print("[2.3] 方式3: @track + opik_context")
    print("=" * 60)

    @track(project_name="opik-ob-experiment-01-attach", name="process_with_attachment")
    def process_with_attachment(query: str) -> str:
        opik_context.update_current_trace(
            attachments=[
                Attachment(
                    data=b"fake_image_bytes_from_http",
                    file_name="remote_image.jpg",
                    content_type="image/jpeg",
                )
            ]
        )
        return "processed"

    result = process_with_attachment("analyze image")
    opik.flush_tracker()
    print(f"  ✓ done ({result})\n")


if __name__ == "__main__":
    attachment_via_span_arg()
    attachment_via_client_span()
    attachment_via_opik_context()
