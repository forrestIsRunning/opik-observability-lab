"""
实验 05-3: Prompt 版本演进工作流

演示完整的 prompt 生命周期：
V1 创建 → V2 迭代 → 版本对比 → 回滚 → 批量管理。

运行:
    uv run python experiments/05-prompt-library/run_03_prompt_evolution.py

预期结果:
    控制台输出多个版本的注册、对比信息、回滚验证
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from prompt_lib import prompts, settings  # noqa: E402


def main():
    client = settings.make_client()

    print("=" * 60)
    print("[入口 1] Prompt 版本演进：从 V1 → V2 → V3")
    print("=" * 60)

    # ==========================================================
    # 阶段 1：V1 — 初始版本
    # ==========================================================
    print("\n" + "=" * 60)
    print("阶段 1: 创建 V1 — 初始版本")
    print("=" * 60)

    v1 = client.create_prompt(
        name="order_query_prompt",
        prompt="""\
根据用户问题提取订单号，然后查询订单状态。

用户问题：{{question}}
订单状态：{{order_status}}
""",
        metadata={
            "version": "1.0",
            "description": "订单查询初始版本",
            "author": "team-ai",
        },
    )
    print(f"  V1 commit: {v1.commit}")
    print(f"  V1 内容: {v1.prompt[:80]}...")

    # 模拟间隔（真实场景可能是几天后）
    time.sleep(0.5)

    # ==========================================================
    # 阶段 2：V2 — 增加多订单支持 + 语气优化
    # ==========================================================
    print("\n" + "=" * 60)
    print("阶段 2: 创建 V2 — 增加多订单支持 + 友好语气")
    print("=" * 60)

    v2 = client.create_prompt(
        name="order_query_prompt",
        prompt="""\
你是一个友好的订单查询助手。

任务：
1. 从用户问题中提取所有订单号
2. 查询每个订单号的状态
3. 用表格形式回复用户

用户问题：{{question}}
订单状态：{{order_status}}

注意：如果用户没有提供订单号，请友好地引导用户提供。
""",
        metadata={
            "version": "2.0",
            "description": "支持多订单查询 + 表格回复 + 引导话术",
            "author": "team-ai",
            "changelog": "多订单支持、表格输出、缺失订单号引导",
        },
    )
    print(f"  V2 commit: {v2.commit}")
    print(f"  V2 内容: {v2.prompt[:80]}...")

    time.sleep(0.5)

    # ==========================================================
    # 阶段 3：V3 — 增加情绪检测 + 升级机制
    # ==========================================================
    print("\n" + "=" * 60)
    print("阶段 3: 创建 V3 — 增加情绪检测 + 升级机制")
    print("=" * 60)

    v3 = client.create_prompt(
        name="order_query_prompt",
        prompt="""\
你是一个友好的订单查询助手。

任务：
1. 检测用户情绪（正常/焦急/愤怒）
2. 从用户问题中提取所有订单号
3. 查询每个订单号的状态
4. 根据情绪级别调整回复语气

情绪处理规则：
- 正常（neutral）：标准友好回复 + 表格
- 焦急（anxious）：先共情 + 快速给出信息 + 安抚语气
- 愤怒（angry）：先道歉 + 升级到人工客服

用户问题：{{question}}
订单状态：{{order_status}}

注意：如果用户没有提供订单号，请友好地引导用户提供。
""",
        metadata={
            "version": "3.0",
            "description": "情绪检测 + 分级响应 + 人工升级",
            "author": "team-ai",
            "changelog": "新增情绪检测机制、分级回复策略、愤怒自动升级",
            "tags": ["production", "v3"],
        },
    )
    print(f"  V3 commit: {v3.commit}")
    print(f"  V3 内容: {v3.prompt[:80]}...")

    # ==========================================================
    # 阶段 4：回滚验证
    # ==========================================================
    print("\n" + "=" * 60)
    print("[验证] 版本对比 & 回滚演练")
    print("=" * 60)

    print(f"\n  order_query_prompt 版本统计:")
    print(f"    V1: {v1.commit}")
    print(f"    V2: {v2.commit}")
    print(f"    V3: {v3.commit}")

    latest = client.get_prompt(name="order_query_prompt")
    print(f"\n  当前最新版本: {latest.commit}")
    print(f"  最新内容预览: {latest.prompt[:100]}...")

    # 拉取 V1 验证回滚能力
    v1_fetched = client.get_prompt(name="order_query_prompt", commit=v1.commit)
    print(f"\n  [回滚演练] Pin 到 V1: {v1_fetched.commit}")
    print(f"  V1 内容: {v1_fetched.prompt[:100]}...")

    # 验证 V3 和 V1 内容确实不同
    assert v1.commit != v3.commit, "V1 和 V3 应该是不同版本！"
    assert v1_fetched.prompt == v1.prompt, "Promise: Pin 到 V1 应返回 V1 的原始内容"
    print("\n  ✓ 版本隔离正确：pin V1 返回的是 V1 的原始内容")
    print("  ✓ 回滚能力验证通过：只需把 APPOVED_COMMITS 指向 V1 即可回滚")

    # ==========================================================
    # 阶段 5：列出当前 project 下的 prompt 版本
    # ==========================================================
    print("\n" + "=" * 60)
    print("[入口 2] 搜索 project 下的 trace & prompt 使用记录")
    print("=" * 60)

    # 搜索使用了新版 prompt 的 trace
    traces = client.search_traces(
        filter_string='metadata.prompt_name = "order_query_prompt"',
    )
    print(f"\n  关联 trace 数量: {len(traces)}")

    client.end()
    print("\n✅ 完成！Prompt 版本演进工作流演示结束")


if __name__ == "__main__":
    main()