# 05 — User Feedback & Cost Tracking

## User Feedback (用户反馈)

Opik 支持对 Trace 和 Span 记录反馈评分，用于质量评估和监控。

### 核心 API

```python
# 方式 1: 在 Trace/Span 对象上直接打分
trace.log_feedback_score(name="helpfulness", value=5, category_name="good", reason="Accurate answer")

# 方式 2: 批量打分 (ID 已知即可，不依赖对象存在)
client.log_traces_feedback_scores([
    {"id": trace_id, "name": "accuracy", "value": 0.95, "reason": "Correct"}
])
client.log_spans_feedback_scores([...])
client.log_threads_feedback_scores([...])
```

### 最佳实践

| 实践 | 说明 |
|------|------|
| **评分标准化** | 固定评分范围（如 1-5 或 0-1），便于聚合 |
| **命名规范** | `accuracy`、`helpfulness`、`relevance` 等 |
| **category_name** | 分类评分用 category_name 区分 |
| **reason** | 记录评分原因，便于复盘 |
| **批量打分** | 后台上报用批量 API，性能更好 |
| **打分时机** | 可以在 Trace 结束后任意时间打分 |

## Cost Tracking (成本追踪)

Opik 通过在 Span 上记录 `usage`、`model`、`provider`、`total_cost` 来实现成本追踪。

### 支持的 Provider

`opik.LLMProvider` 枚举:
- `OPENAI` — OpenAI 模型
- `ANTHROPIC` — Anthropic Claude
- `GOOGLE_VERTEXAI` — Google VertexAI
- `GOOGLE_AI` — Google AI
- `GROQ` — Groq
- `BEDROCK` — AWS Bedrock
- `ANTHROPIC_VERTEXAI` — Anthropic on VertexAI

### 最佳实践

| 实践 | 说明 |
|------|------|
| **Provider + Model 必填** | 自动成本计算依赖这两个字段 |
| **usage 用 OpenAI 格式** | `prompt_tokens`、`completion_tokens`、`total_tokens` |
| **total_cost 覆盖** | 手动指定 `total_cost` 会覆盖自动计算 |
| **metadata 补充** | 额外计费信息放 metadata |