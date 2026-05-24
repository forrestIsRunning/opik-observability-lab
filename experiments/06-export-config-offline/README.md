# 06 — Export Data, SDK Configuration & Offline Fallback

> 基于真实文档更新

## Export Data

Opik 提供三种导出方式：

### 1. SDK search 方法（推荐）

```python
# 导出所有 Traces
traces = client.search_traces(project_name="Default project", max_results=1000000)

# 使用 OQL 过滤
traces = client.search_traces(filter_string='input contains "Opik"')
traces = client.search_traces(filter_string='usage.total_tokens > 1000')
traces = client.search_traces(filter_string='tags contains "production"')
traces = client.search_traces(filter_string='feedback_scores.user_rating is_not_empty')

# 导出 Spans
spans = client.search_spans(project_name="Default project", trace_id="...")
spans = client.search_spans(filter_string='type = "llm"')

# 导出 Threads
threads = client.search_threads(project_name="...", max_results=1000000)
threads = client.search_threads(filter_string='number_of_messages >= 5')
```

### 2. REST API
- `GET /api/v1/traces` 和 `GET /api/v1/spans` 接口

### 3. UI 导出
- 选择 Trace → Actions → Export CSV（上限 100 条）

## SDK Configuration

### 配置优先级
Constructor 参数 → 环境变量 → `~/.opik.config` 文件 → 默认值

### 关键配置

| 环境变量 | 用途 |
|----------|------|
| `OPIK_API_KEY` | Opik Cloud API Key |
| `OPIK_URL_OVERRIDE` | Opik 服务地址 |
| `OPIK_PROJECT_NAME` | 项目名称 |
| `OPIK_WORKSPACE` | 工作空间 |
| `OPIK_ENVIRONMENT` | 环境标签 |

### 配置方式

```python
# CLI 方式
opik.configure(use_local=False)  # Cloud
opik.configure(use_local=True)   # 自托管

# 或直接构造
client = opik.Opik(project_name="my-app", host="http://localhost:5173/api")
```

## Offline Fallback

默认启用，零配置。三层机制：
1. **检测** — `OpikConnectionMonitor` 定期 ping `/is-alive/ping`
2. **存储** — 断网时写入本地 SQLite
3. **回放** — 恢复后 `ReplayManager` 批量重放

### 可调参数

| 环境变量 | 默认值 | 说明 |
|----------|--------|------|
| `OPIK_CONNECTION_MONITOR_PING_INTERVAL` | 10s | Ping 间隔 |
| `OPIK_REPLAY_BATCH_SIZE` | 50 | 每批回放数量 |
| `OPIK_REPLAY_BATCH_REPLAY_DELAY` | 0.5s | 批次间隔 |

### 恢复时间估算

```
replay_time ≈ ceil(failed_messages / replay_batch_size) × replay_batch_replay_delay
```

示例：500 条消息，默认配置 → ceil(500/50) × 0.5 = 5 秒