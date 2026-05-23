# 08 — Debugging Agents with Ollie

## Ollie (Opik LLM Investigator)

Ollie 是 Opik 内置的 Agent 调试工具，帮助可视化、分析和调试 LLM Agent 的行为。

> **注意**: Ollie 是 Opik 前端/平台功能，主要通过 UI 使用。SDK 层面的准备是确保 Trace/Span 数据质量。

## 调试 Agent 的最佳实践

| 实践 | 说明 |
|------|------|
| **完整 Span 树** | Agent 每一步都创建明确的 Span（思考、工具调用、响应） |
| **metadata 记录思维链** | Agent 的推理过程放在 metadata |
| **input/output 完整** | 每一步的输入输出都要记录 |
| **error_info** | Agent 调用失败时记录完整错误堆栈 |
| **tags 标记版本** | Agent prompt 版本、model 版本用 tags 标记 |
| **thread_id 关联会话** | 同一 Agent 会话的所有步骤关联到 thread |

## Opik Connect

Opik Connect 是 Opik 的数据管道集成能力，支持将 Trace 数据导出到外部系统。

### 数据流

```
LLM 应用 → Opik SDK → Opik Backend → Opik Connect → 外部系统
                                                    ├── Dashboard
                                                    ├── Alerting
                                                    └── Custom pipeline
```