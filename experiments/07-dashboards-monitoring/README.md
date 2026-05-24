# 07 — Dashboards & Production Monitoring

> 基于真实文档更新

## Dashboards

Opik 提供两种可视化方式：

### Insights（内嵌视图）
- **Project Insights** — 项目内的 `Insights` tab，内置 Project Overview 视图
- **Experiment Insights** — 实验对比时的内置只读视图

### Workspace Dashboards（独立仪表板）
- 从侧边栏访问
- 两种类型：
  | 类型 | 用途 | 可用组件 |
  |------|------|----------|
  | **Multi-project** | 跨项目指标 | Time series, Single metric, Markdown |
  | **Experiments** | 实验对比 | Metrics, Leaderboard, Markdown |

### 可用指标
- Trace feedback scores, Trace volume, Trace duration
- Token usage, Estimated cost, Failed guardrails
- Thread volume, Thread duration, Thread feedback scores

## Production Monitoring

Opik 从设计上支持高并发生产环境。

### 生产监控流程

1. **记录反馈分数**
```python
@track
def llm_chain(input_text):
    opik_context.update_current_trace(
        feedback_scores=[
            {"name": "user_feedback", "value": 1.0, "reason": "Helpful response"}
        ]
    )
```

2. **定义 LLM as a Judge 指标** — 在线评估自动评分
3. **搜索并更新** — 批量处理已记录的 Trace
```python
traces = opik_client.search_traces(project_name="Default Project")
for trace in traces:
    opik_client.log_traces_feedback_scores(scores=[{
        "id": trace.id, "name": "quality", "value": 0.95
    }])
```

### 最佳实践

| 实践 | 说明 |
|------|------|
| **Online Evaluation** | 用 LLM as a Judge 自动评分 |
| **Insights 监控** | 内置 Project Overview 看板 |
| **开发到生产闭环** | Trace → 分析 → 优化 → 部署 → Trace |