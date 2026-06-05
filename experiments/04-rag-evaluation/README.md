# 实验 04: RAG / Agent 系统的 Opik 评测

> 一个端到端、可复用、**默认无需任何外部 LLM Key** 的 RAG/Agent 评测 demo。
> 回答三个问题：**怎么建评测集、怎么做 dashboard、飞书 bot 多轮请求怎么归到一条 Opik thread。**

---

## 与 opik-skills 的关系

`comet-ml/opik-skills` 的 `references/evaluation.md` 教你**单点 API**——
怎么建 dataset、怎么调 `evaluate()` 或 `run_tests()`、有哪些 60+ 内置 metric。

本模块教你**组合方式与 production 闭环**——
- 评测集 + task + metric 三层怎么搭配
- 飞书会话 `chat_id` → Opik `thread_id` 的真实映射（skill 没讲）
- 机器评分 → 不合格自动入 Annotation Queue → 人工 review 的闭环（skill 没讲）
- Dashboard widget 怎么按 metadata/tags 配（skill 没讲）

读 skill 先理解 API，再看本模块看怎么用在真业务上。

---

## 这个 demo 解决什么问题

你有一个 RAG 系统（或基于 RAG 的 Agent），想用 Opik 回答：

1. **它答得准不准？** → 需要一个"评测集"（黄金问答对）+ 一套"指标"，跑出分数。
2. **分数怎么看趋势、怎么对比不同版本？** → Opik 的 **Experiment** 就是 dashboard。
3. **飞书 bot 里同一个会话连问 3 句，怎么在 Opik 里连成一条对话？** → **thread_id** 映射。

本 demo 把这三件事拆成可单独复用的模块，逐个跑通。

---

## 心智模型（先理解这张图，代码就好懂了）

```
评测集 (Dataset)            评测任务 (task)              指标 (metrics)
┌─────────────────┐        ┌──────────────────┐        ┌────────────────────┐
│ input           │        │ 跑一次你的 RAG    │        │ 给每条结果打分      │
│ expected_output │──喂──▶ │ → {output,context}│──喂──▶ │ 命中率/覆盖率/幻觉  │
└─────────────────┘        └──────────────────┘        └────────────────────┘
        │                          │                            │
        └──────────────────────────┴────────────────────────────┘
                                    ▼
                        Experiment（= dashboard）
                     每条样本的分数 + 平均分 + 历次趋势


飞书会话                          Opik
┌──────────────────────┐         ┌──────────────────────────┐
│ chat_id / root_id    │──映射──▶│ thread_id（同会话归一条） │
│ 多轮 message         │         │ thread 下挂多个 Trace     │
└──────────────────────┘         └──────────────────────────┘
```

三个关键认知：

- **context 不写进评测集**。检索到的 context 是"被评测对象"产出的，应由 task 实时生成，
  否则你没法衡量"检索好不好"。评测集只放 `input` + `expected_output`。
- **Experiment 就是 dashboard**。你不用单独搭面板，`evaluate()` 跑完自动在 Opik UI
  的 Experiments 页生成分数表、平均分、可对比历史 run。
- **thread_id 必须在 project 内唯一且稳定**。同一条飞书会话的多轮请求，要推导出
  **相同** 的 thread_id，才能归并；不同会话要推导出**不同**的。

---

## 目录结构

```
04-rag-evaluation/
├── README.md                    # 本文件
├── rag_eval/                    # 可复用包（每个模块都能单独搬走）
│   ├── settings.py              # Opik 连接配置（单一真源）
│   ├── pipeline.py              # mock RAG Agent（@track 埋点）
│   ├── machine_scoring.py       # 自定义规则的机器评分（纯函数）
│   ├── dataset.py               # 构建评测集
│   ├── metrics.py               # 离线指标 + 可选 LLM 裁判指标
│   └── feishu_thread.py         # 飞书会话 → Opik thread 映射
├── run_01_build_dataset.py      # 入口1: 建评测集
├── run_02_evaluate.py           # 入口2: 跑评测 → 生成 Experiment(dashboard)
├── run_03_feishu_threads.py     # 入口3: 模拟飞书多轮 → Opik thread
├── run_04_evaluate_threads.py   # 入口4: 会话级评测（需 LLM Key）
├── run_05_dataset_crud.py       # 入口5: 数据集 增/查/改/删
├── run_06_machine_scoring_queue.py  # 入口6: 自定义规则机器评分 + 标注队列
└── run_07_dashboard_seed.py     # 入口7: 造 dashboard 数据 + UI 配置指南
```

---

## 快速开始

### 0. 前置：本地 Opik 必须在跑

```bash
# 在仓库根目录
docker compose -f docker-compose.opik.yml up -d
curl http://localhost:5173/api/is-alive/ping     # 预期: {"healthy":true}
```

### 1. 建评测集

```bash
uv run python experiments/04-rag-evaluation/run_01_build_dataset.py
```

→ Opik UI → **Datasets** → 看到 `rag-agent-golden-qa`，5 条样本。

### 2. 跑评测（默认离线指标，无需任何 Key）

```bash
uv run python experiments/04-rag-evaluation/run_02_evaluate.py
```

→ 终端打印每条样本分数 + 平均分；Opik UI → **Experiments** 看 dashboard。

### 3. 模拟飞书多轮 → thread

```bash
uv run python experiments/04-rag-evaluation/run_03_feishu_threads.py
```

→ Opik UI → **Threads** → 看到两条 thread（会话 A 三轮、会话 B 两轮）。

### 4.（可选）会话级评测 — 需要 LLM Key

```bash
RAG_EVAL_USE_LLM_METRICS=1 OPENAI_API_KEY=sk-... \
    uv run python experiments/04-rag-evaluation/run_04_evaluate_threads.py
```

→ 每条 thread 上多出 coherence / frustration 反馈分。

### 5/6/7. 数据集 CRUD、机器评分+标注队列、Dashboard 造数

```bash
# 5) 数据集增删改查（用临时数据集，跑完自动删除，不污染正式集）
uv run python experiments/04-rag-evaluation/run_05_dataset_crud.py

# 6) 自定义规则机器评分 + 把不合格回答路由到人工标注队列
uv run python experiments/04-rag-evaluation/run_06_machine_scoring_queue.py

# 7) 造一批带 metadata/tags/feedback 的 trace，并打印 UI 自定义 widget 配方
uv run python experiments/04-rag-evaluation/run_07_dashboard_seed.py
```

---

## 三个进阶能力详解

### A) 数据集 CRUD（`run_05`）

| 操作 | API | 说明 |
|---|---|---|
| 建/取 | `client.get_or_create_dataset(name, description)` | 幂等 |
| 查 | `dataset.get_items()` | 返回 `list[dict]`，**含 `id`** |
| 增 | `dataset.insert([{...}])` | 按内容哈希去重 |
| 改 | `dataset.update([{"id":..., ...}])` | **必须带 id**，整条覆盖 |
| 删项 | `dataset.delete([id, ...])` | 删指定项 |
| 清空 | `dataset.clear()` | 删所有项，数据集还在 |
| 删集 | `client.delete_dataset(name)` | 删整个数据集 |

### B) 机器评分（自定义规则）+ 标注队列（`run_06`）

生产闭环：**机器规则先打分 → 不合格的自动入人工标注队列**。

- 规则在 `rag_eval/machine_scoring.py`，都是**纯函数**（非空 / 有 context / 长度 / 不拒答），
  易单测、可替换成你的业务规则（如"必须含引用""禁含敏感词"）。
- 机器分通过 `client.log_traces_feedback_scores([{id,name,value}])` 写回。
- 不合格 trace 通过 `client.create_traces_annotation_queue(...)` + `queue.add_traces([...])`
  路由到 Opik UI 的 **Annotation Queues** 给人复核。
- 实测：off-topic 问题（"今天上海天气"）触发拒答 → `rule_has_context=0`、`rule_not_refusal=0`
  → 自动入队。

> 这正是 Opik 文档说的 [Online Evaluation Rules] 思路：自动产生 feedback 分喂给 dashboard。

### C) 项目级 Dashboard 自定义（`run_07`）

**关键认知：Opik Dashboard/Insights 在 UI 里配置，没有"建 widget"的 SDK。**
SDK 的活是**喂结构化数据**，UI 的 widget 才能按维度自定义图表。

`run_07` 造 24 条带 `metadata{model,route,environment}` + `tags` + `usage` +
三个 feedback 分（`quality`/`groundedness`/`latency_ok`）+ 偶发 error 的 trace，
然后打印"在 UI 怎么配 widget"的对照清单，例如：

- Time series：Metric=`Trace feedback scores`→quality，Breakdown=`Metadata key`→model
- Time series：Metric=`Estimated cost`，Breakdown=`Tags` → 各 route 成本
- Single metric：`Average feedback scores`→groundedness（KPI 卡）
- Time series：`Number of traces`，Breakdown=`Has error` → 错误率
- 过滤器：`metadata.environment = "production"` → 只看线上

配置路径：项目 → **Insights** 标签 → 视图下拉 **Add new** → 加 widget。

---

## 离线指标 vs LLM 裁判指标

| | 离线启发式（默认） | LLM 裁判（可选） |
|---|---|---|
| 是否需要 Key | ❌ 不需要 | ✅ 需要 |
| 指标 | `ContextHitRate`、`AnswerCoverage` | `ContextPrecision`、`ContextRecall`、`AnswerRelevance`、`Hallucination` |
| 原理 | 关键词集合重叠，确定性 | 用一个 LLM 当裁判打分 |
| 开关 | 默认开 | `RAG_EVAL_USE_LLM_METRICS=1` |

> 用离线指标先把**流程**跑通、把**埋点**验对，再按需接 LLM 裁判，省钱省事。

---

## 接入你自己的系统（复用指南）

1. **换 pipeline**：把 `rag_eval/pipeline.py` 里的 `_retrieve_passages` / `_generate_answer`
   换成你真实的检索和 LLM 调用。返回 dict 保持 `{"output", "context"}` 即可。
2. **换评测集**：改 `rag_eval/dataset.py` 的 `GOLDEN_ITEMS`，或让 `build_dataset` 从
   CSV/JSON 读你的黄金问答对。
3. **接飞书**：把 `FeishuThreadTracer.log_turn` 接到你 bot 的 `im.message.receive` 回调，
   传入事件里的 `chat_id` / `message_id` / `root_id`。映射逻辑见 `feishu_thread.thread_id_for`。

---

## 环境变量速查

| 变量 | 默认 | 说明 |
|---|---|---|
| `OPIK_HOST` | `http://localhost:5173/api` | Opik REST 地址 |
| `OPIK_WORKSPACE` | `default` | 工作区 |
| `OPIK_PROJECT` | `rag-agent-eval` | traces 落到的 project |
| `OPIK_EVAL_PROJECT` | `<project>-threads` | 会话级评测结果 project |
| `RAG_EVAL_USE_LLM_METRICS` | `false` | 是否启用 LLM 裁判指标 |
| `RAG_EVAL_JUDGE_MODEL` | `gpt-4o-mini` | LLM 裁判模型（LiteLLM 名） |

---

## 已知限制 / 诚实说明

- mock pipeline 的检索是"关键词子串匹配"玩具实现，只为演示流程。
- 因为 mock 的知识库片段是英文、标准答案是中文，**离线指标 `ContextHitRate`
  分数会偏低（0.2~0.67）属正常**——它按词重叠算，跨语言自然低；而 `AnswerCoverage`
  因为答案==标准答案所以是 1.0。换成你真实的同语言系统这两个分数才有可比性。
- 会话级指标（run_04）**必须**有 LLM Key，没有就会优雅跳过并提示。
- **已实测**：run_01/02/03/05/06/07 均已对一台真实 Opik（`192.168.16.4:5173`）跑通——
  建集、评测(Experiment)、飞书 thread 归并、数据集 CRUD、机器评分+标注队列、dashboard 造数
  全部验证成功。只有 run_04 因需 LLM Key 未实跑。API 签名均对照已安装 SDK 源码核对。
