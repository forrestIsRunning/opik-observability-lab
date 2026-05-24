# 05 — Annotate Traces (User Feedback) & Cost Tracking

> 基于真实文档更新。文档中该章节名为 "Annotate Traces" 而非 "Log User Feedback"

## Annotate Traces

### SDK 打分方式

```python
# 方式 1: 在 Trace/Span 上直接打分
trace.log_feedback_score(name="quality", value=0.9, reason="Good answer")

# 方式 2: 批量打分
client.log_traces_feedback_scores([
    {"id": trace_id, "name": "accuracy", "value": 0.95, "reason": "Correct"}
])
client.log_spans_feedback_scores([...])
client.log_threads_feedback_scores([...])
```

### UI 标注

- 在 Trace 页面点击 `Annotate` 按钮
- 支持多团队成员标注，显示平均值
- 支持标注原因（reason）

### Online Evaluation

Opik 支持 LLM as a Judge 自动评分:
1. 在平台定义评估规则
2. 自动对所有（或采样）Trace 打分
3. 支持 Trace-level 和 Thread-level 规则
4. 冷却期结束后自动执行

### Manual Evaluation

- 从 Traces 页面选择 Traces → "Evaluate"
- 从 Threads 页面选择 Threads → "Evaluate"
- 绕过采样率，对特定 Trace 执行规则

## Cost Tracking

Opik 自动为受支持的 Provider 计算成本（USD）。

### 支持自动计算的 Provider

- OpenAI (`openai`) — GPT 系列
- Anthropic (`anthropic`) — Claude 系列
- Anthropic on Vertex AI (`anthropic_vertexai`)
- Google AI (`google_ai`) — Gemini
- Google Vertex AI (`google_vertexai`)
- AWS Bedrock (`bedrock`)
- Groq (`groq`)

### 手动设置成本

```python
opik_context.update_current_span(
    provider="openai",
    model="gpt-3.5-turbo",
    usage={"prompt_tokens": 4, "completion_tokens": 6, "total_tokens": 10}
)

# 或直接设置总成本（覆盖自动计算）
opik_context.update_current_span(total_cost=0.05)
```

### 批量成本更新（CRON Job 模式）

Opik 支持后期补算成本：`client.search_spans()` 找到未计算成本的 span → 自定义成本算法 → `client.update_span(total_cost=...)`