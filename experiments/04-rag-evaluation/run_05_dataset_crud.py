"""
入口 5: 数据集 CRUD（增 / 查 / 改 / 删）
==========================================
演示对 Opik Dataset 的全套操作，每一步都打印前后对比，便于"看懂"。

涉及 API（均来自已安装 SDK，已核对签名）:
    client.get_or_create_dataset(name, description)   建/取
    dataset.get_items()                               查（返回 list[dict]，含 id）
    dataset.insert([{...}])                            增（按内容哈希去重）
    dataset.update([{"id":..., ...}])                  改（必须带 id，整条覆盖）
    dataset.delete([item_id, ...])                     删指定项
    dataset.clear()                                    清空所有项
    client.delete_dataset(name)                        删整个数据集

运行:
    uv run python experiments/04-rag-evaluation/run_05_dataset_crud.py

注意:
    本脚本使用独立的临时数据集名（带时间戳），跑完会把它整个删掉，
    不会污染 run_01 建的正式评测集 rag-agent-golden-qa。
"""

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rag_eval import settings  # noqa: E402


def _show(title: str, items: list[dict]) -> None:
    print(f"  {title}（{len(items)} 条）:")
    for it in items:
        print(f"    - id={str(it.get('id'))[:8]}  input={it.get('input', '')[:30]}")


def main() -> None:
    print("=" * 60)
    print("[入口 5] 数据集 CRUD")
    print("=" * 60)

    client = settings.make_client()
    tmp_name = f"crud-demo-{datetime.now():%Y%m%d-%H%M%S}"

    # ── 增：建数据集 + 插入 2 条 ──────────────────────────────
    print(f"\n[1/6] 创建数据集 '{tmp_name}' 并插入 2 条")
    ds = client.get_or_create_dataset(name=tmp_name, description="CRUD demo（临时）")
    ds.insert(
        [
            {"input": "Q1: 什么是 Trace?", "expected_output": "一次端到端请求"},
            {"input": "Q2: 什么是 Span?", "expected_output": "Trace 内的步骤"},
        ]
    )
    _show("当前内容", ds.get_items())

    # ── 查：读回来拿到每条的 id ───────────────────────────────
    print("\n[2/6] 查询（get_items 返回带 id 的 dict）")
    items = ds.get_items()
    _show("读到", items)

    # ── 改：更新第 1 条（update 必须带 id，整条覆盖）──────────
    print("\n[3/6] 更新第 1 条（必须带 id）")
    first = dict(items[0])
    first["expected_output"] = "一次端到端请求（已更新✏️）"
    ds.update([first])
    _show("更新后", ds.get_items())

    # ── 删：删掉第 2 条 ───────────────────────────────────────
    print("\n[4/6] 删除第 2 条（按 id 删）")
    # 重新读 id，保证拿到服务端最新版本
    items = ds.get_items()
    target = next(it for it in items if it["input"].startswith("Q2"))
    ds.delete([target["id"]])
    _show("删除后", ds.get_items())

    # ── 清空：clear 删掉所有项（数据集本身还在）──────────────
    print("\n[5/6] 清空所有项（clear，数据集本身保留）")
    ds.clear()
    _show("清空后", ds.get_items())

    # ── 删整个数据集 ─────────────────────────────────────────
    print("\n[6/6] 删除整个数据集")
    client.delete_dataset(name=tmp_name)
    try:
        client.get_dataset(tmp_name)
        print("  [异常] 数据集仍存在（不符合预期）")
    except Exception as e:  # noqa: BLE001
        print(f"  [确认] 数据集已删除，再查报错: {type(e).__name__}")

    print("\n  [完成] 数据集 CRUD 全流程演示结束\n")


if __name__ == "__main__":
    main()
