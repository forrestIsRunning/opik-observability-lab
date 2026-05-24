# 01 — Tracing Overview & Getting Started

> 基于真实文档更新

## 底层逻辑

Opik 提供三种接入方式:
1. **AI Coding Agent**（推荐）— 安装 `opik-skills`，用 `/instrument` 命令自动插桩
2. **Opik Connect** — 从 Dashboard 用 Ollie 自动设置追踪
3. **手动 SDK** — `@opik.track` 装饰器或低层 API

## 核心流程

```
opik connect --project <NAME>   # 1. 关联项目
@opik.track                     # 2. 插桩代码
def my_agent(user_message):
    ...
# Trace 自动出现在 Dashboard  # 3. 查看追踪
```

## 最佳实践（来自文档原文）

| 实践 | 原文引用 |
|------|----------|
| **Trace 边界清晰** | "Define clear boundaries — typically a complete user interaction" |
| **Span 命名有意义** | "Choose descriptive names that clearly indicate what operation is being performed" |
| **Thread ID 关联对话** | "Use consistent thread IDs for related interactions" |
| **持续监控** | "Set up alerts to monitor trace performance, error rates, and costs" |
| **用 Trace 做优化** | "Regularly analyze traces to identify optimization opportunities" |
| **关注关键路径** | "Start with basic tracing, gradually add more detail — don't trace everything at once" |
| **敏感数据保护** | "Be mindful of PII and sensitive data in traces" |

## 可捕获的数据

Traces & Spans → Cost tracking → Media & attachments → User feedback → Agent graphs