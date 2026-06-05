"""
实验 05-1: 注册 Prompt 到 Opik Prompt Library

演示如何把 hard-coded prompts 注册到 Opik，开启版本管理。
每次运行都会创建新版本（新 commit）。

运行:
    uv run python experiments/05-prompt-library/run_01_register_prompts.py

预期结果:
    在 Opik UI → Prompt Library 中可以看到 3 个 prompt 及其 V1
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from prompt_lib import prompts, settings  # noqa: E402

def main():
    client = settings.make_client()

    print("=" * 60)
    print("[入口 1] 注册 hard-coded prompts → Opik Prompt Library")
    print("=" * 60)

    # -----------------------------------------------------------
    # 注册 V1：sysetm prompt
    # -----------------------------------------------------------
    print("\n1. 注册 system prompt (V1)...")
    system_prompt = client.create_prompt(
        name="customer_service_system",
        prompt=prompts.HARD_CODED_SYSTEM_PROMPT,
        metadata=prompts.PROMPT_METADATA["customer_service_system"],
    )
    print(f"   ✓ customer_service_system  commit: {system_prompt.commit}")

    # -----------------------------------------------------------
    # 注册 V1：user template（带 Mustache 变量）
    # -----------------------------------------------------------
    print("\n2. 注册 user question 模板 (V1)...")
    user_template = client.create_prompt(
        name="user_question_template",
        prompt=prompts.HARD_CODED_USER_TEMPLATE,
        metadata=prompts.PROMPT_METADATA["user_question_template"],
    )
    print(f"   ✓ user_question_template   commit: {user_template.commit}")

    # -----------------------------------------------------------
    # 注册 V1：summary prompt
    # -----------------------------------------------------------
    print("\n3. 注册 conversation summarizer (V1)...")
    summary_prompt = client.create_prompt(
        name="conversation_summarizer",
        prompt=prompts.HARD_CODED_SUMMARY_PROMPT,
        metadata=prompts.PROMPT_METADATA["conversation_summarizer"],
    )
    print(f"   ✓ conversation_summarizer  commit: {summary_prompt.commit}")

    # -----------------------------------------------------------
    # 注册 V2：更新 system prompt
    # -----------------------------------------------------------
    print("\n4. 更新 system prompt → V2（增加退货细分规则 + 升级机制）...")
    system_prompt_v2 = client.create_prompt(
        name="customer_service_system",
        prompt=prompts.V2_SYSTEM_PROMPT,
        metadata={
            **prompts.PROMPT_METADATA["customer_service_system"],
            "tags": ["production", "customer-service", "v2"],
            "changelog": "新增电子产品15天退货规则 + 升级人工客服机制 + 品牌语调",
        },
    )
    print(f"   ✓ customer_service_system V2  commit: {system_prompt_v2.commit}")

    # -----------------------------------------------------------
    # 验证：从 Prompt Library 拉取
    # -----------------------------------------------------------
    print("\n" + "=" * 60)
    print("[验证] 从 Opik Prompt Library 拉取验证")
    print("=" * 60)

    latest = client.get_prompt(name="customer_service_system")
    print(f"\n  customer_service_system:")
    print(f"    最新版本 commit: {latest.commit}")
    print(f"    内容预览 (前100字): {latest.prompt[:100]}...")

    v1_system = client.get_prompt(name="customer_service_system", commit=system_prompt.commit)
    print(f"\n  Pin 到 V1 commit: {v1_system.commit}")
    print(f"    内容预览 (前100字): {v1_system.prompt[:100]}...")

    # 验证两个版本确实不同
    assert latest.commit != v1_system.commit, "V1 和 V2 应该是不同的 commit！"
    print("\n  ✓ V1 ≠ V2 commit，版本隔离正确")

    client.end()
    print("\n✅ 完成！前往 Opik UI → Prompt Library 查看注册结果")


if __name__ == "__main__":
    main()