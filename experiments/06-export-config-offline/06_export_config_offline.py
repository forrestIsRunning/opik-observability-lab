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


def demonstrate_sdk_configuration():
    """多种 SDK 配置方式"""
    print("=" * 60)
    print("[实验 6.1] SDK 配置方式")
    print("=" * 60)

    # 方式 1: 直接传入
    client = opik.Opik(
        project_name="opik-ob-experiment-06",
        host="http://localhost:5173",
        workspace="default",
    )
    print(f"  [配置 1] project_name={client.project_name}")

    # 通过 config 属性查看
    print(f"  [配置] config.host={client.config.host}")
    print(f"  [配置] config.workspace={client.config.workspace}")

    trace = client.trace(name="config_demo", input={"demo": True})
    trace.end(output={"status": "done"})
    client.end()
    print("  [完成] SDK 配置演示\n")


def demonstrate_export_data():
    """导出已记录的数据"""
    print("=" * 60)
    print("[实验 6.2] 数据导出")
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

    trace_id = trace.id
    span_id = span.id
    print(f"  [记录] Trace ID: {trace_id}")
    print(f"  [记录] Span ID: {span_id}")

    # 读回 Trace 数据 (需要在 flush 后, 后端已处理)
    client.flush()
    try:
        trace_data = client.get_trace_content(trace_id)
        print(f"  [导出] Trace name: {trace_data.name}")
        print(f"  [导出] Trace input: {trace_data.input}")
        print(f"  [导出] Trace output: {trace_data.output}")
    except Exception as e:
        print(f"  [注意] 读取 Trace 需要后端可用: {e}")

    # 读回 Span 数据
    try:
        span_data = client.get_span_content(span_id)
        print(f"  [导出] Span name: {span_data.name}")
    except Exception as e:
        print(f"  [注意] 读取 Span 需要后端可用: {e}")

    client.end()


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