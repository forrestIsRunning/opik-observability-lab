# 07 — Dashboards & Production Monitoring

## Dashboards (仪表板)

Opik 的 Dashboard 是 UI 层面的功能，支持:

- **Trace 列表** — 按 project、时间、tags 过滤
- **Span 火焰图** — 可视化调用链路和耗时
- **Feedback Score 聚合** — 平均分、分布、趋势
- **Cost 分析** — 按 model/provider 的成本统计
- **自定义 Dashboard** — 拖拽式图表配置

> Dashboard 的底层数据来源就是 SDK 记录的 Trace、Span、Feedback Score、Cost。数据质量决定了 Dashboard 的价值。

### 最佳实践

| 实践 | 说明 |
|------|------|
| **tags 做维度** | tags 是 Dashboard 过滤的主要维度 |
| **metadata** | 结构化的 metadata 支持 Dashboard 聚合分析 |
| **命名规范** | 统一的 project_name 和 span name |
| **数据完整性** | 确保所有 span 都正常 end() |

## Production Monitoring (生产监控)

生产环境的可观测性需要:

1. **持续追踪** — 所有 LLM 调用自动记录
2. **反馈评分** — 用户反馈 + AI 自动评估
3. **异常检测** — error_info 聚合告警
4. **成本监控** — 按 model/provider 的成本趋势
5. **性能监控** — span 耗时追踪

### 最佳实践

| 实践 | 说明 |
|------|------|
| **使用 @track 装饰器** | 自动追踪函数调用 |
| **环境标签** | 所有 Trace 标记 `environment=production` |
| **错误追踪** | 捕获异常并记录 error_info |
| **采样策略** | 高流量场景按比例采样 |
| **批量客户端** | 生产环境用 `max_workers` 控制并发 |