# 06 — Export Data, SDK Configuration & Offline Fallback

## Export Data (数据导出)

Opik 提供多种方式读取已记录的数据:

```python
# 通过 SDK 读取
trace_data = client.get_trace_content(trace_id)
span_data = client.get_span_content(span_id)
project = client.get_project(project_id)
```

也可以通过 REST API 直接导出。

## SDK Configuration (SDK 配置)

Opik 客户端通过 `opik.Opik()` 或 `opik.configure()` 进行配置。

### 配置项

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `host` | Opik 服务地址 | `http://localhost:5173` |
| `workspace` | 工作空间 | `default` |
| `project_name` | 项目名称 | `default` |
| `api_key` | API 密钥 | `None` |
| `use_local` | 是否本地模式 | `False` |
| `url_override` | URL 覆盖 | `None` |

### 最佳实践

| 实践 | 说明 |
|------|------|
| **环境变量** | 用 `OPIK_HOST`、`OPIK_API_KEY`、`OPIK_WORKSPACE` 环境变量 |
| **多环境配置** | dev/staging/prod 用不同 project_name 或 host |
| **client.end()** | 确保程序退出前 flush 数据 |

## Offline Fallback (离线模式)

Opik 支持在网络不可用时本地记录 Trace，后续再同步。

```python
# 开启本地记录
from opik import record_traces_locally
record_traces_locally()

# 或者通过配置
opik.configure(use_local=True)
```

### 最佳实践

| 实践 | 说明 |
|------|------|
| **本地先记** | 网络不稳定时本地记录，避免丢数据 |
| **批量同步** | 恢复连接后批量回放 |
| **消息 replay** | Opik 内置消息 replay 机制 |