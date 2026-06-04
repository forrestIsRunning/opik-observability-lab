"""
02_oql_export.py — OQL 搜索、数据导出、离线缓存概念

运行方式:
    uv run python experiments/03-ops-feedback-cost-export/02_oql_export.py
"""

import os
import opik
import opik.message_processing.replay.replay_manager as replay_manager

OPIK_PROJECT = os.getenv("OPIK_PROJECT", "ops-demo")


def oql_export() -> None:
    """创建示例 Trace 并演示 OQL 过滤语法 + get_trace_content。"""
    print("=" * 60)
    print("[2.1] OQL 搜索 & 数据导出")
    print("=" * 60)

    client = opik.Opik(
        project_name=OPIK_PROJECT,
        host="http://localhost:5173/api",
        workspace="default",
    )

    trace = client.trace(name="export_me", input={"data": "test"}, tags=["export-demo"])
    span = trace.span(name="step1", type="general", input={"step": 1})
    span.end(output={"result": "step1 done"})
    trace.end(output={"result": "all done"})

    client.flush()

    # OQL 支持的过滤语法（search_traces / search_spans / search_threads 通用）
    print("  [OQL] 常用过滤示例:")
    oql_examples = [
        'input contains "Opik"',
        'usage.total_tokens > 1000',
        'tags contains "production"',
        'feedback_scores.user_rating is_not_empty',
        'start_time >= "2024-01-01T00:00:00Z"',
    ]
    for q in oql_examples:
        print(f'    filter_string={q!r}')

    # 按 ID 读取单条 Trace（需后端可用）
    try:
        trace_data = client.get_trace_content(trace.id)
        print(f"\n  [导出] Trace name: {trace_data.name}, id: {trace.id}")
    except Exception as e:
        print(f"\n  [注意] get_trace_content 需后端可用: {e}")

    client.end(timeout=30, flush=True)
    print("  [完成] OQL 导出演示\n")


def sdk_config() -> None:
    """三种 SDK 配置方式速览（代码注释即文档）。"""
    print("=" * 60)
    print("[2.2] SDK 配置方式")
    print("=" * 60)

    # 方式 1: 构造函数传参（本实验统一用这种方式）
    client = opik.Opik(
        project_name=OPIK_PROJECT,
        host="http://localhost:5173/api",
        workspace="default",
    )
    print(f"  [配置] project_name={client.project_name}")

    # 方式 2: opik.configure(use_local=True)  ← 写入 ~/.opik.config，CLI 友好
    # 方式 3: 环境变量 OPIK_API_KEY / OPIK_URL_OVERRIDE / OPIK_PROJECT_NAME

    t = client.trace(name="config_demo", input={"demo": True})
    t.end(output={"status": "done"})
    client.end(timeout=30, flush=True)
    print("  [完成] SDK 配置演示\n")


def offline_cache() -> None:
    """离线缓存：断网时本地记录，恢复后通过 replay_manager 回放。"""
    print("=" * 60)
    print("[2.3] 离线缓存概念")
    print("=" * 60)

    has_replay = hasattr(replay_manager, "ReplayManager")
    print(f"  [离线] ReplayManager 可用: {has_replay}")
    print("  [离线] 网络中断时 SDK 将 Trace 写入本地队列")
    print("  [离线] 恢复连接后 replay_manager 自动回放，不丢数据")
    print("  [完成] 离线缓存概念演示\n")


def main() -> None:
    oql_export()
    sdk_config()
    offline_cache()


if __name__ == "__main__":
    main()
