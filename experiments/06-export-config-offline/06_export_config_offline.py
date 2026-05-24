"""
实验 06: Export Data, SDK Configuration & Offline Fallback
===========================================================
数据导出、SDK 配置、离线模式。

运行方式:
    uv run python experiments/06-export-config-offline/06_export_config_offline.py
"""

import os
import opik
from opik import LLMProvider


def demonstrate_export_data():
    """
    数据导出 (文档原文 API):
    - client.search_traces(filter_string=...)  # OQL 过滤
    - client.search_spans(project_name=..., trace_id=...)
    - client.search_threads(filter_string=...)
    """
    print("=" * 60)
    print("[实验 6.2] 数据导出 — OQL 搜索")
    print("=" * 60)

    client = opik.Opik(
        project_name="opik-ob-experiment-06",
        host="http://localhost:5173",
        workspace="default",
    )

    # 先创建一条 Trace
    trace = client.trace(name="export_me", input={"data": "test"}, tags=["export-demo"])
    span = trace.span(name="step1", type="general", input={"step": 1})
    span.end(output={"result": "step1 done"})
    trace.end(output={"result": "all done"})

    client.flush()

    # 文档原文的 OQL 过滤示例
    print("  [OQL] 文档原文支持的过滤语法:")
    print('    filter_string=\'input contains "Opik"\'')
    print('    filter_string=\'usage.total_tokens > 1000\'')
    print('    filter_string=\'tags contains "production"\'')
    print('    filter_string=\'feedback_scores.user_rating is_not_empty\'')
    print('    filter_string=\'start_time >= "2024-01-01T00:00:00Z"\'')

    # 尝试搜索
    try:
        trace_id = trace.id
        print(f"\n  [导出] Trace ID: {trace_id}")
        trace_data = client.get_trace_content(trace_id)
        print(f"  [导出] Trace name: {trace_data.name}")
    except Exception as e:
        print(f"  [注意] 读取需要后端可用: {e}")

    client.end()
    print("  [完成] 导出演示\n")


def demonstrate_sdk_configuration():
    """
    SDK 配置 (文档原文):
    - opik.configure(use_local=True/False)
    - Constructor: opik.Opik(project_name=..., host=..., workspace=...)
    - 环境变量: OPIK_API_KEY, OPIK_URL_OVERRIDE, OPIK_PROJECT_NAME
    """
    print("=" * 60)
    print("[实验 6.3] SDK 配置方式")
    print("=" * 60)

    # 方式 1: 直接传入 (文档推荐)
    client = opik.Opik(
        project_name="opik-ob-experiment-06",
        host="http://localhost:5173",
        workspace="default",
    )
    print(f"  [配置] project_name={client.project_name}")

    trace = client.trace(name="config_demo", input={"demo": True})
    trace.end(output={"status": "done"})
    client.end()

    # 方式 2: opik.configure (CLI)
    # 文档原文:
    #   import opik
    #   opik.configure(use_local=False)   # Cloud
    #   opik.configure(use_local=True)    # 自托管
    # 或命令行:
    #   $ opik configure --yes
    print("  [配置] 另支持: opik.configure(use_local=True/False)")
    print("  [配置] 另支持: 环境变量 OPIK_API_KEY, OPIK_URL_OVERRIDE 等")
    print("  [完成] SDK 配置演示\n")


def demonstrate_offline_fallback():
    """
    离线模式演示: 本地记录, 不依赖后端服务。
    Opik 支持将 Trace 记录到本地, 后续再同步。
    """
    print("=" * 60)
    print("[实验 6.3] 离线模式")
    print("=" * 60)

    # 检查离线模式相关 API
    import opik.message_processing.replay.replay_manager as replay

    print(f"  [离线] replay_manager 可用: {hasattr(replay, 'ReplayManager')}")

    # 离线模式的概念演示: 在不连接到后端的情况下记录
    # 实际使用中, 可以在断网时本地缓存, 恢复后回放
    print("  [离线] 本地记录模式可用于网络不稳定场景")
    print("  [离线] 恢复连接后通过消息回放同步数据")

    print("  [完成] 离线模式概念演示\n")


if __name__ == "__main__":
    demonstrate_sdk_configuration()
    demonstrate_export_data()
    demonstrate_offline_fallback()