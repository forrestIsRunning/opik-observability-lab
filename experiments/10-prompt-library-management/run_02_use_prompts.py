"""
实验 10-2: 在代码中使用 Opik Prompt

演示生产环境最佳实践：pin 特定 commit + 模板填充 + trace 联动。

运行:
    uv run python experiments/10-prompt-library-management/run_02_use_prompts.py

预期结果:
    控制台输出从 Opik 拉取的 prompt 内容、模板填充结果、trace 记录
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from prompt_lib import settings  # noqa: E402


def main():
    client = settings.make_client()

    print("=" * 60)
    print("[入口 1] 从 Opik Prompt Library 获取 prompt")
    print("=" * 60)

    # -----------------------------------------------------------
    # 获取最新版本（开发环境常用）
    # -----------------------------------------------------------
    print("\n1. 获取最新版本 customer_service_system...")
    system_prompt = client.get_prompt(name="customer_service_system")
    print(f"   commit: {system_prompt.commit}")
    print(f"   内容:\n{'-'*40}\n{system_prompt.prompt}\n{'-'*40}")

    # -----------------------------------------------------------
    # Pin 到特定版本（生产环境强烈推荐！）
    # -----------------------------------------------------------
    print("\n2. [生产最佳实践] Pin 到特定 commit...")
    # 实际项目中，这些 commit hash 应放在配置文件或环境变量中
    # commit=None = 获取最新版本；传具体 hash = 锁定版本
    APPROVED_COMMITS = {
        "customer_service_system": None,  # 生产环境请替换为实际 commit hash
        "user_question_template": None,
        "conversation_summarizer": None,
    }

    def _get_pinned(name: str) -> str:
        commit = APPROVED_COMMITS[name]
        label = commit or "latest"
        print(f"   正在获取 {name} @ {label}...")
        prompt = client.get_prompt(name=name, commit=commit)
        assert prompt is not None, f"Prompt '{name}' 不存在，请先运行 run_01_register_prompts.py"
        print(f"   ✓ commit: {prompt.commit}")
        return prompt

    system_prompt = _get_pinned("customer_service_system")

    # -----------------------------------------------------------
    # 模板填充
    # -----------------------------------------------------------
    print("\n3. 填充 user_question_template...")
    user_template = _get_pinned("user_question_template")

    filled_prompt = user_template.format(
        question="我的订单#12345 已经 10 天没收到了，怎么办？",
        chat_history="用户：你好\n客服：您好，有什么可以帮您？",
    )
    print(f"   模板内容:\n{'-'*40}\n{user_template.prompt}\n{'-'*40}")
    print(f"\n   填充结果:\n{'-'*40}\n{filled_prompt}\n{'-'*40}")

    # -----------------------------------------------------------
    # Prompt + Tracing 联动
    # -----------------------------------------------------------
    print("\n4. Trace 中记录使用的 prompt 版本...")
    trace = client.trace(
        name="customer_service_call",
        input={"question": "订单#12345 状态查询", "prompt_commit": system_prompt.commit},
        metadata={
            "prompt_name": "customer_service_system",
            "prompt_commit": system_prompt.commit,
        },
    )

    span = trace.span(
        name="llm_call",
        type="llm",
        input={"system": system_prompt.prompt, "user": filled_prompt},
        metadata={"model": "gpt-4o", "prompt_version": system_prompt.commit},
    )

    # 模拟 LLM 响应
    mock_response = "您好，我已经查到了您的订单#12345，目前正在海关清关中，预计还需要2-3个工作日。请您耐心等待，如有任何问题随时联系我们。"
    span.end(
        output=mock_response,
        usage={"completion_tokens": 45, "prompt_tokens": 210, "total_tokens": 255},
    )
    trace.end(output=mock_response)
    print(f"   ✓ Trace ID: {trace.id}")
    print(f"   ✓ 已在 trace metadata 中记录 prompt commit: {system_prompt.commit}")

    # -----------------------------------------------------------
    # Attachment: 把完整 prompt 作为 attachment 附在 trace 上（可选）
    # -----------------------------------------------------------
    trace = client.trace(
        name="prompt_snapshot",
        input={"note": "记录本次使用的 prompt 完整内容"},
        metadata={
            "prompt_name": "customer_service_system",
            "prompt_commit": system_prompt.commit,
        },
    )
    trace.end(
        output={"prompt_preview": system_prompt.prompt[:200] + "..."},
    )
    print(f"\n   ✓ Prompt snapshot trace ID: {trace.id}")

    client.end()
    print("\n✅ 完成！前往 Opik UI → Traces 查看 prompt 版本记录")


if __name__ == "__main__":
    main()