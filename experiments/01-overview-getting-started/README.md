# 01 — Tracing Overview & Getting Started

## 底层逻辑

Opik 的可观测性基于 **Trace**（跟踪）和 **Span**（跨度） 两级结构。一个 Trace 代表一次完整的 LLM 调用链路，Span 则是链路中的独立步骤。

## 最佳实践

| 实践 | 说明 |
|------|------|
| **Trace 粒度 = 一次用户请求** | 每个外部请求创建一个 Trace，内部步骤用 Span |
| **Span 类型** | `general`、`llm`、`tool`、`guardrail` 四种类型，选对类型便于 UI 过滤 |
| **Always call end()** | 不调用 end() 会导致 Trace 在 UI 上显示为"进行中" |
| **metadata 传递上下文** | 把 environment、session_id、user_id 等放在 metadata 中 |
| **tags 做分类** | 用 tags 标记版本、环境、实验组 |
| **thread_id 关联多轮** | 多轮对话用 thread_id 把多个 Trace 关联成线程 |
| **flush 确保落盘** | 程序退出前调用 `client.end()` 确保所有数据已发送 |

## Hands-on 实验

```bash
# 运行 01_basic_tracing.py
uv run python experiments/01-overview-getting-started/01_basic_tracing.py
```

代码演示：
1. Trace 创建 - end - update 全生命周期
2. Span 嵌套（子 span）
3. llm 类型 span 的使用
4. metadata、tags、error_info 的传递
5. thread_id 多轮关联