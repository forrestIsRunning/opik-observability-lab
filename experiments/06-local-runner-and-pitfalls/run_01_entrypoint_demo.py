"""
实验 06-1: Entrypoint 参数规则 + Local Runner 演示

演示 @opik.track(entrypoint=True) 的正确用法：
- entrypoint 函数只接受 primitive 类型（str, int, float, bool）
- 复杂类型（Pydantic model、dataclass）需要用 thin wrapper 包一层
- 这样 Opik Local Runner 才能在 UI 里为每个参数生成表单字段

运行（普通模式）:
    uv run python experiments/06-local-runner-and-pitfalls/run_01_entrypoint_demo.py

运行（通过 opik connect 配对 Local Runner）:
    opik connect --pair <CODE> uv run python experiments/06-local-runner-and-pitfalls/run_01_entrypoint_demo.py

其中 <CODE> 是在 Opik UI → Local Runner 页面点击 "New Runner" 后得到的配对码。
"""

from __future__ import annotations

import opik
from opik import opik_context

# ---------------------------------------------------------------------------
# 内部数据模型（模拟真实应用中的 Pydantic model / dataclass）
# ---------------------------------------------------------------------------

class RecommendRequest:
    """代表应用内部流转的复杂请求对象，不能直接用作 entrypoint 参数。"""

    def __init__(self, city: str, category: str, max_results: int) -> None:
        self.city = city
        self.category = category
        self.max_results = max_results


# ---------------------------------------------------------------------------
# 内部业务逻辑（接受复杂类型，没有 entrypoint 标记）
# ---------------------------------------------------------------------------

@opik.track(name="recommend-core")
def run_recommend(request: RecommendRequest) -> dict:
    """核心推荐逻辑。接受内部模型，正常做业务处理。"""
    opik_context.update_current_trace(
        tags=["recommend", request.category],
        metadata={"city": request.city, "max_results": request.max_results},
    )

    # 模拟推荐逻辑
    results = [
        f"{request.category} venue #{i + 1} in {request.city}"
        for i in range(request.max_results)
    ]

    return {
        "city": request.city,
        "category": request.category,
        "recommendations": results,
    }


# ---------------------------------------------------------------------------
# ✅ 正确的 entrypoint：只接受 primitive 类型
#
# 为什么这样做：
#   Opik Local Runner 读取函数的 type hint，在 UI 里为每个参数生成输入框。
#   如果参数是 RecommendRequest 这样的复杂类型，UI 无法渲染表单字段。
#   Thin wrapper 接受 primitives，在内部拼成复杂对象，再调用业务逻辑。
# ---------------------------------------------------------------------------

@opik.track(name="recommend-agent", entrypoint=True)
def run_entrypoint(city: str, category: str, max_results: int = 3) -> dict:
    """
    Opik entrypoint — Local Runner 从这里触发。

    参数全是 primitive，UI 会自动生成：
    - city:        text input
    - category:    text input
    - max_results: number input
    """
    request = RecommendRequest(
        city=city,
        category=category,
        max_results=max_results,
    )
    return run_recommend(request)


# ---------------------------------------------------------------------------
# ❌ 反例：complex type 作为 entrypoint（注释保留用于对比理解）
#
# @opik.track(name="recommend-agent", entrypoint=True)
# def bad_entrypoint(request: RecommendRequest) -> dict:
#     # RecommendRequest 不是 primitive — Local Runner 无法为它生成表单
#     return run_recommend(request)
# ---------------------------------------------------------------------------


def main() -> None:
    client = opik.Opik(
        project_name="opik-exp-06-entrypoint",
        host="http://localhost:5173/api",
        workspace="default",
    )

    print("=" * 60)
    print("[实验 06-1] Entrypoint Primitives Demo")
    print("=" * 60)
    print()
    print("本脚本演示了正确的 entrypoint 写法。")
    print("直接运行时触发一次 demo 调用；通过 opik connect 配对后，")
    print("可以从 Opik UI 的 Local Runner 表单触发。")
    print()

    result = run_entrypoint(
        city="Shanghai",
        category="coffee shop",
        max_results=3,
    )

    print("调用结果:")
    for rec in result["recommendations"]:
        print(f"  - {rec}")

    print()
    print("前往 Opik UI 查看 trace：")
    print("  http://localhost:5173  → 项目 opik-exp-06-entrypoint")
    print()
    print("通过 Local Runner 端到端测试：")
    print("  1. 在 Opik UI → Local Runner → New Runner，获取配对码")
    print("  2. 运行：")
    print("       opik connect --pair <CODE> \\")
    print("         uv run python experiments/06-local-runner-and-pitfalls/run_01_entrypoint_demo.py")
    print("  3. 回到 UI，在表单中填入 city / category / max_results，点击 Run")

    client.end(timeout=30, flush=True)


if __name__ == "__main__":
    main()
