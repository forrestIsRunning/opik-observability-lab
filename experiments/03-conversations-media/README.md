# 03 — Log Conversations & Media Attachments

> 基于真实文档更新

## Conversations (Threads)

Threads 通过 `thread_id` 将多个 Trace 归组为对话线程。

### 文档关键点

- **thread_id**: 用户自定义，每个 project 内唯一
- **设置方式**: `client.trace(thread_id=...)` 或 `@opik.track` 传 `opik_args={"trace": {"thread_id": ...}}`
- **UI 查看**: Project → Threads tab
- **线程级反馈**: 支持对整条线程打分
- **Cool down**: 线程在线评分冷却期默认 15 分钟
- **过滤运算符**: `=`, `!=`, `contains`, `starts_with`, `ends_with`, `>`, `<`

## Media Attachments

`Attachment(data=..., file_name=..., content_type=...)`:
- `data`: 文件路径、原始 bytes、或 base64 编码字符串
- `file_name`: bytes 模式必填
- `content_type`: MIME 类型

### 支持预览的 MIME 类型

- Image: `image/jpeg`, `image/png`, `image/gif`, `image/svg+xml`
- Video: `video/mp4`, `video/webm`
- Audio: `audio/wav`, `audio/vorbis`, `audio/x-wav`
- Text: `text/plain`, `text/markdown`
- PDF: `application/pdf`
- Other: `application/json`, `application/octet-stream`

### 上传方式

1. **文件路径**: `Attachment(data="/path/to/file", content_type="image/png")`
2. **原始 bytes**: `Attachment(data=image_bytes, file_name="img.png", content_type="image/png")`
3. **HTTP 响应**: `httpx.get(url).content` → Attachment
4. **生成内容**: `json.dumps(data).encode("utf-8")` → Attachment
5. **Client 直接**: `client.span(attachments=[Attachment(...)])`
6. **Context 更新**: `opik_context.update_current_trace(attachments=[Attachment(...)])`
7. **AttachmentClient**: 程序化管理（列表、下载、上传，适用于 >50MB 文件）