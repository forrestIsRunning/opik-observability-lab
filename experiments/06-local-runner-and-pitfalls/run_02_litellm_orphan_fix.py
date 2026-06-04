"""
实验 06-2: LiteLLM 孤儿 trace — 问题复现 + 修复

演示两种行为：

CASE 1 (BROKEN)  — litellm.completion 在 @opik.track 内，但没有传 current_span_data。
                   OpikLogger 不知道当前 span，会在 Opik 中创建一个独立的顶层 trace。
                   结果：你以为有一条 trace，实际 UI 里出现两条。

CASE 2 (FIXED)   — 传入 metadata={"opik": {"current_span_data": get_current_span_data(), ...}}。
                   OpikLogger 找到活跃 span，把 LLM call 挂在正确的位置。
                   结果：一条 trace，LLM call 是子 span。

运行（默认 mock 模式，无需 API key）:
    uv run python experiments/06-local-runner-and-pitfalls/run_02_litellm_orphan_fix.py

如果设置了 OPENAI_API_KEY，自动切换到 gpt-4o-mini 真实调用。
"""

from __future__ import annotations

import os
import sys

import opik
from opik import opik_context
from opik.opik_context import get_current_span_data

# ---------------------------------------------------------------------------
# litellm 导入：缺失时给出友好提示
# ---------------------------------------------------------------------------

try:
    import litellm
    from litellm.integrations.opik.opik import OpikLogger
except ImportError:
    print("错误：litellm 未安装。")
    print("请运行：uv add litellm  或  pip install litellm")
    sys.exit(1)

# ---------------------------------------------------------------------------
# 全局配置
# ---------------------------------------------------------------------------

# 注册 OpikLogger 作为 litellm 的全局回调
litellm.callbacks = [OpikLogger()]

# 根据是否有 API key 决定使用真实模型还是 mock
_HAS_API_KEY = bool(os.environ.get("OPENAI_API_KEY"))
_MODEL = "gpt-4o-mini" if _HAS_API_KEY else "openai/gpt-4o-mini"
_MOCK_RESPONSE = None if _HAS_API_KEY else "This is a mock response for testing."

_TEST_MESSAGES = [{"role": "user", "content": "Summarize LLM observability in one sentence."}]


# ---------------------------------------------------------------------------
# CASE 1: BROKEN — 没有传 current_span_data
# ---------------------------------------------------------------------------

@opik.track(name="broken-llm-call")
def _broken_llm_call(messages: list) -> str:
    """调用 litellm 但不传 current_span_data。OpikLogger 会创建孤儿 trace。"""
    kwargs: dict = {"model": _MODEL, "messages": messages}
    if _MOCK_RESPONSE:
        kwargs["mock_response"] = _MOCK_RESPONSE
    # 没有 metadata["opik"]["current_span_data"] — OpikLogger 无法定位活跃 span
    response = litellm.completion(**kwargs)
    return response.choices[0].message.content


@opik.track(name="broken-agent", entrypoint=True)
def run_broken_case(query: str) -> str:
    """BROKEN: LLM call 会产生一个与本 trace 无关的孤儿 trace。"""
    opik_context.update_current_trace(tags=["broken", "orphan-demo"])
    return _broken_llm_call(_TEST_MESSAGES)


# ---------------------------------------------------------------------------
# CASE 2: FIXED — 传入 current_span_data
# ---------------------------------------------------------------------------

@opik.track(name="fixed-llm-call")
def _fixed_llm_call(messages: list) -> str:
    """调用 litellm，并通过 metadata 传递当前 span。OpikLogger 正确嵌套。"""
    kwargs: dict = {
        "model": _MODEL,
        "messages": messages,
        "metadata": {
            "opik": {
                "current_span_data": get_current_span_data(),
                "tags": ["litellm"],
            },
        },
    }
    if _MOCK_RESPONSE:
        kwargs["mock_response"] = _MOCK_RESPONSE
    response = litellm.completion(**kwargs)
    return response.choices[0].message.content


@opik.track(name="fixed-agent", entrypoint=True)
def run_fixed_case(query: str) -> str:
    """FIXED: LLM call 正确嵌套在本 trace 下，没有孤儿 trace。"""
    opik_context.update_current_trace(tags=["fixed", "correct-nesting"])
    return _fixed_llm_call(_TEST_MESSAGES)


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def main() -> None:
    mode = "REAL (gpt-4o-mini)" if _HAS_API_KEY else "MOCK (no API key needed)"
    print("=" * 60)
    print("[实验 06-2] LiteLLM 孤儿 Trace — 问题复现 + 修复")
    print(f"模式: {mode}")
    print("=" * 60)

    client = opik.Opik(
        project_name="opik-exp-06-litellm",
        host="http://localhost:5173/api",
        workspace="default",
    )

    # --- CASE 1: BROKEN ---
    print()
    print(">>> CASE 1: BROKEN（孤儿 trace）")
    print("    预期：Opik UI 中出现 2 条 trace：")
    print("      - broken-agent（你创建的）")
    print("      - 一条独立的 LiteLLM trace（孤儿，没有父级）")
    result_broken = run_broken_case(query="test orphan")
    print(f"    返回: {result_broken[:60]!r}")

    # --- CASE 2: FIXED ---
    print()
    print(">>> CASE 2: FIXED（正确嵌套）")
    print("    预期：Opik UI 中出现 1 条 trace：")
    print("      - fixed-agent")
    print("          └── fixed-llm-call")
    print("                └── litellm span（正确挂在父级下）")
    result_fixed = run_fixed_case(query="test correct nesting")
    print(f"    返回: {result_fixed[:60]!r}")

    print()
    print("=" * 60)
    print("验证步骤：")
    print("  1. 前往 http://localhost:5173")
    print("  2. 打开项目 opik-exp-06-litellm")
    print("  3. BROKEN case：筛选 tag=orphan-demo，会看到两条独立 trace")
    print("  4. FIXED case： 筛选 tag=correct-nesting，只有一条 trace，")
    print("                  LiteLLM call 是子 span")
    print("=" * 60)

    client.end(timeout=30, flush=True)
    print("完成。")


if __name__ == "__main__":
    main()
