# 03 — Log Conversations & Media

## Conversations (对话)

Opik 用 `thread_id` 将多个 Trace 关联成一个对话线程。这是实现多轮对话可观测性的关键机制。

### 最佳实践

| 实践 | 说明 |
|------|------|
| **同一 thread_id 跨 Trace** | 同一对话的所有轮次用同一 `thread_id` |
| **thread_id 需全局唯一** | 每个 project 内 thread_id 唯一 |
| **在 Trace 创建时传入** | `client.trace(thread_id=...)` |
| **trace.end() 也可以传** | 也可以在 end() 时更新 thread_id |

## Media & Attachments (媒体)

Opik 支持在 Trace/Span 上附加文件（图片、PDF 等），通过 `Attachment` 类实现。

### 最佳实践

| 实践 | 说明 |
|------|------|
| **Attachment 对象创建** | `Attachment(file_path=...或 content=..., mime_type=...)` |
| **在 span() 时传入** | `span = trace.span(attachments=[...])` |
| **支持二进制内容** | 直接传 `content` bytes 或文件路径 |
| **自动上传** | SDK 会自动上传并关联到 span |

> **注意**: Attachment 只能在 span 创建时传入，不能通过 update/end 追加。