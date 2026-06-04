# 03 — Ops 三件套

> "Ops 三件套：trace 出来 → 评/算成本 → 查/导出。skill 讲单点 API，本模块讲组合方式。"

本模块把三个高频运维动作组合成可独立运行的脚本，覆盖从打分、成本追踪到数据查询导出的完整链路。

## 脚本速览

| 脚本 | 展示内容 | 适用场景 |
|------|----------|----------|
| `01_feedback_and_cost.py` | 单条/批量反馈打分；多提供商自动+手动成本追踪 | 上线后补打分、成本审计 |
| `02_oql_export.py` | OQL 过滤语法；`get_trace_content`；SDK 配置三种方式；离线缓存概念 | 数据导出、离线部署 |
| `03_production_track_pattern.py` | `@track` 嵌套装饰器；`opik_context.update_current_span`；search → 批量打分闭环 | 生产代码无侵入接入 |

## 运行

```bash
# 启动本地 Opik（如尚未启动）
docker compose -f docker-compose.opik.yml up -d

# 运行任意脚本
uv run python experiments/03-ops-feedback-cost-export/01_feedback_and_cost.py
uv run python experiments/03-ops-feedback-cost-export/02_oql_export.py
uv run python experiments/03-ops-feedback-cost-export/03_production_track_pattern.py

# 自定义项目名
OPIK_PROJECT=my-project uv run python experiments/03-ops-feedback-cost-export/01_feedback_and_cost.py
```

## 延伸阅读

`@track` 装饰器基础用法（参数、线程安全、与框架集成）见 `.agents/skills/opik/SKILL.md` Python Instrumentation 章节。
