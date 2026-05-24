Opik supports multimodal traces allowing you to track not just the text input and output of your LLM, but also images, videos and audio and any other media.

![](https://files.buildwithfern.com/https://opik.docs.buildwithfern.com/docs/opik/99d85955ae6b263e219b27d9c0a9dee39ded4bb713ca6da0cad52ca9a3b70de3/img/tracing/attachments.png)

data: The path to the file, raw bytes, or a base64 encoded string of the file file\_name: Optional name for the attachment (required when using raw bytes without a file path) content\_type: The content type of the file formatted as a MIME type

## Logging Attachments

In the Python SDK, you can use the `Attachment` type to add files to your traces. Attachements can be images, videos, audio files or any other file that you might want to log to Opik.

Each attachment is made up of the following fields:

- `data`: The path to the file, raw bytes, or a base64 encoded string of the file
- `file_name`: Optional name for the attachment (required when using raw bytes without a file path)
- `content_type`: The content type of the file formatted as a MIME type

These attachements can then be logged to your traces and spans using The `opik_context.update_current_span` and `opik_context.update_current_trace` methods:

### Using file paths

The most common way to log attachments is by providing a file path:

```python
1from opik import opik_context, track, Attachment
2
3@track
4def my_llm_agent(input):
5    # LLM chain code
6    # ...
7
8    # Update the trace with a file path
9    opik_context.update_current_trace(
10        attachments=[
11            Attachment(
12                data="<path to the image>",
13                content_type="image/png",
14            )
15        ]
16    )
17
18    return "World!"
19
20print(my_llm_agent("Hello!"))
```

### Using raw bytes (file-like data)

You can also pass raw bytes directly to an attachment. This is useful when you have file content in memory (e.g., from an API response, generated content, or streaming data) and don’t want to write it to disk first:

```python
1from opik import opik_context, track, Attachment
2
3@track
4def process_image(image_bytes: bytes):
5    # Process the image
6    # ...
7
8    # Log the raw bytes as an attachment
9    opik_context.update_current_trace(
10        attachments=[
11            Attachment(
12                data=image_bytes,  # Raw bytes
13                file_name="processed_image.png",  # Required for bytes
14                content_type="image/png",
15            )
16        ]
17    )
18
19    return "Image processed!"
20
21# Example: Reading a file into memory and logging it
22with open("image.png", "rb") as f:
23    image_data = f.read()
24
25print(process_image(image_data))
```

When using raw bytes, Opik automatically creates a temporary file for upload and cleans it up after the attachment is uploaded. If you don’t specify a `content_type`, Opik will try to infer it from the `file_name` or default to `application/octet-stream`.

### Logging images from HTTP responses

A common use case is logging images fetched from external APIs or URLs:

```python
1import httpx
2from opik import opik_context, track, Attachment
3
4@track
5def analyze_remote_image(image_url: str):
6    # Fetch image from URL
7    response = httpx.get(image_url)
8    image_bytes = response.content
9    content_type = response.headers.get("content-type", "image/jpeg")
10
11    # Log the fetched image as an attachment
12    opik_context.update_current_trace(
13        attachments=[
14            Attachment(
15                data=image_bytes,
16                file_name="remote_image.jpg",
17                content_type=content_type,
18            )
19        ]
20    )
21
22    # Process the image...
23    return "Image analyzed!"
24
25# Analyze an image from a URL
26result = analyze_remote_image("https://example.com/image.jpg")
```

### Logging generated content

You can also log dynamically generated content like charts or reports:

```python
1from opik import opik_context, track, Attachment
2import json
3
4@track
5def generate_report(data: dict):
6    # Generate a JSON report
7    report_bytes = json.dumps(data, indent=2).encode("utf-8")
8
9    opik_context.update_current_trace(
10        attachments=[
11            Attachment(
12                data=report_bytes,
13                file_name="report.json",
14                content_type="application/json",
15            )
16        ]
17    )
18
19    return "Report generated!"
```

### Using the Opik client directly

You can also log attachments using the Opik client directly with both file paths and raw bytes:

```python
1import opik
2from opik import Attachment
3
4client = opik.Opik()
5
6# Create a trace
7trace = client.trace(
8    name="my-trace",
9    input={"query": "Process this data"},
10    project_name="my-project",
11)
12
13# Log attachment with file path
14span_with_file = client.span(
15    trace_id=trace.id,
16    name="file-attachment-span",
17    attachments=[
18        Attachment(
19            data="/path/to/document.pdf",
20            content_type="application/pdf",
21        )
22    ],
23)
24
25# Log attachment with raw bytes
26binary_data = b"Hello, this is binary content!"
27span_with_bytes = client.span(
28    trace_id=trace.id,
29    name="bytes-attachment-span",
30    attachments=[
31        Attachment(
32            data=binary_data,
33            file_name="data.bin",
34            content_type="application/octet-stream",
35        )
36    ],
37)
38
39client.flush()
```

The attachements will be uploaded to the Opik platform and can be both previewed and dowloaded from the UI.

![](https://files.buildwithfern.com/https://opik.docs.buildwithfern.com/docs/opik/99d85955ae6b263e219b27d9c0a9dee39ded4bb713ca6da0cad52ca9a3b70de3/img/tracing/attachments.png)

data: The path to the file, raw bytes, or a base64 encoded string of the file file\_name: Optional name for the attachment (required when using raw bytes without a file path) content\_type: The content type of the file formatted as a MIME type

In order to preview the attachements in the UI, you will need to supply a supported content type for the attachment. We support the following content types:

- Image: `image/jpeg`, `image/png`, `image/gif` and `image/svg+xml`
- Video: `video/mp4` and `video/webm`
- Audio: `audio/wav`, `audio/vorbis` and `audio/x-wav`
- Text: `text/plain` and `text/markdown`
- PDF: `application/pdf`
- Other: `application/json` and `application/octet-stream`

## Managing Attachments Programmatically

You can also manage attachments programmatically using the [`AttachmentClient`](https://www.comet.com/docs/opik/python-sdk-reference/Objects/AttachmentClient.html):

```python
1import opik
2
3opik_client = opik.Opik()
4attachment_client = opik_client.get_attachment_client()
5
6# Get list of attachments
7attachments_details = attachment_client.get_attachment_list(
8    project_name="my-project",
9    entity_id="some-trace-uuid-7",
10    entity_type="trace"
11)
12
13# Download an attachment
14attachment_data = attachment_client.download_attachment(
15    project_name="my-project",
16    entity_type="trace",
17    entity_id="some-trace-uuid-7",
18    file_name="report.pdf",
19    mime_type="application/pdf"
20)
21
22# Upload a new attachment
23attachment_client.upload_attachment(
24    project_name="my-project",
25    entity_type="trace", 
26    entity_id="some-trace-uuid-7",
27    file_path="/path/to/document.pdf"
28)
```

## Previewing base64 encoded images and image URLs

Opik automatically detects base64 encoded images and URLs logged to the platform, once an image is detected we will hide the string to make the content more readable and display the image in the UI. This is supported in the tracing view, datasets view and experiment view.

For example if you are using the OpenAI SDK, if you pass an image to the model as a URL, Opik will automatically detect it and display the image in the UI:

```python
1from opik.integrations.openai import track_openai
2from openai import OpenAI
3
4# Make sure to wrap the OpenAI client to enable Opik tracing
5client = track_openai(OpenAI())
6
7response = client.chat.completions.create(
8  model="gpt-4o-mini",
9  messages=[
10    {
11      "role": "user",
12      "content": [
13        {"type": "text", "text": "What's in this image?"},
14        {
15          "type": "image_url",
16          "image_url": {
17            "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
18          },
19        },
20      ],
21    }
22  ],
23  max_tokens=300,
24)
25
26print(response.choices[0])
```
![](https://files.buildwithfern.com/https://opik.docs.buildwithfern.com/docs/opik/b28450e12ff7f45f2e58ce32b39edb07a359baf00ec7eb23dbcd8edd0a5e824e/img/tracing/image_trace.png)

data: The path to the file, raw bytes, or a base64 encoded string of the file file\_name: Optional name for the attachment (required when using raw bytes without a file path) content\_type: The content type of the file formatted as a MIME type

## Embedded Attachments

When you embed base64-encoded media directly in your trace/span `input`, `output`, or `metadata` fields, Opik automatically optimizes storage and retrieval for performance.

### How It Works

For base64-encoded content larger than 250KB, Opik automatically extracts and stores it separately. This happens transparently - you don’t need to change your code.

When you retrieve your traces or spans later, the attachments are automatically included by default. For faster queries when you don’t need the attachment data, use the `strip_attachments=true` parameter.

### Size Limits

Opik Cloud supports embedded attachments up to **100MB per field**. This limit applies to individual string values in your `input`, `output`, or `metadata` fields.

Base64 encoding increases file size by about 33%. For example, a 75MB video becomes ~100MB when base64-encoded.

If you need to work with larger files:

1. **Use the Attachment API** - Upload files separately using `AttachmentClient` (recommended for files >50MB). See [Managing Attachments Programmatically](https://www.comet.com/docs/opik/tracing/advanced/log_multimodal_traces#managing-attachments-programmatically)
2. **Contact us** - [Get in touch](https://www.comet.com/site/about-us/contact-us/) if you need higher limits
3. **Self-host Opik** - Configure your own limits. See the [Self-hosting Guide](https://www.comet.com/docs/opik/self-host/overview)

### Best Practices

- Embed smaller files directly - Opik handles them efficiently
- For files >50MB, use the Attachment API for better performance
- Use `strip_attachments=true` when querying if you don’t need the attachment data

## Downloading attachments

You can download attachments in two ways:

1. **From the UI**: Hover over the attachments and click on the download icon
2. **Programmatically**: Use the `AttachmentClient` as shown in the examples above

Let’s us know on [Github](https://github.com/comet-ml/opik/issues/new/choose) if you would like to us to support additional image formats.