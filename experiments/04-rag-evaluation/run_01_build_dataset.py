"""
入口 1: 构建评测集
===================
把黄金问答对写入 Opik Dataset。幂等，可重复跑。

运行:
    uv run python experiments/04-rag-evaluation/run_01_build_dataset.py

看结果:
    打开 Opik UI → 左侧 Datasets → 找到 "rag-agent-golden-qa"
"""

import sys
from pathlib import Path

# 让脚本无论从哪运行都能 import 到本目录下的 rag_eval 包
sys.path.insert(0, str(Path(__file__).resolve().parent))

from rag_eval import dataset as dataset_module  # noqa: E402


def main() -> None:
    print("=" * 60)
    print("[入口 1] 构建 RAG 评测集")
    print("=" * 60)

    dataset = dataset_module.build_dataset()
    items = dataset.get_items()

    print(f"  [完成] 数据集 '{dataset_module.DATASET_NAME}' 当前共 {len(items)} 条样本")
    for i, item in enumerate(items, 1):
        print(f"    {i}. {item.get('input', '')[:40]}")
    print("  [下一步] 运行 run_02_evaluate.py 在该数据集上跑评测\n")


if __name__ == "__main__":
    main()
