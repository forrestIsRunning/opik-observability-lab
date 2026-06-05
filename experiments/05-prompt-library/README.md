# 实验 05 — Opik Prompt Library 管理

> Hard-coded prompts 的版本控制、集中管理和生产级编排方案。像 Git 一样管理 prompt，从此告别"改 prompt = 改代码 + 重新部署"的痛点。

## 这个实验解决什么问题？

LLM 应用中，prompt 是核心资产，但大多数团队的 prompt 管理还停留在石器时代：

| 问题 | Hard-code 的现状 | Opik 的解法 |
|------|------------------|-------------|
| 版本管理 | 散落在 Git 历史里，无法快速对比 | 每次注册自动生成 commit，支持 diff 和回滚 |
| 部署风险 | 改 prompt 必须改代码 → 全量部署 | 代码动态拉取，更新 prompt 不影响生产 |
| 环境一致 | dev/staging/prod 的 prompt 容易漂移 | 中央化存储，pin 特定 commit 保证一致性 |
| 团队协作 | 产品/运营无法参与 | Prompt Playground UI，非技术人员也能编辑 |
| 效果对比 | 靠人工记忆"上一个版本好像更好" | 跟 tracing + evaluation 联动，数据驱动决策 |

## 核心概念

```
┌─────────────────────────────────────────────────────────────┐
│                    Opik Prompt Library                        │
│                                                              │
│  ┌──────────────────┐   ┌──────────────────┐                │
│  │  customer_service │   │  order_query      │   ...更多      │
│  │  _system          │   │  _prompt          │                │
│  └───┬──────────────┘   └───┬──────────────┘                │
│      │                      │                                │
│      ▼                      ▼                                │
│  ┌──────┬──────┬──────┐  ┌──────┬──────┬──────┐             │
│  │ V1   │ V2   │ V3   │  │ V1   │ V2   │ V3   │             │
│  │abc123│def456│ghi789│  │abc123│def456│ghi789│             │
│  └──────┴──────┴──────┘  └──────┴──────┴──────┘             │
│       ▲                      ▲                               │
│       │    Pin to commit      │                               │
│       └──────────┬────────────┘                               │
│                  │                                            │
│         ┌────────┴────────┐                                   │
│         │   production    │                                   │
│         │  config: {      │                                   │
│         │   commits: {...}│                                   │
│         │  }              │                                   │
│         └─────────────────┘                                   │
└─────────────────────────────────────────────────────────────┘
```

**关键机制**：
- 每个 prompt 通过 `name` 标识，相同 `name` + 不同 `prompt` 内容 → 自动创建新版本（新 commit）
- 代码中可以 pick 最新版（开发环境）或 pin 特定 commit（生产环境）
- 支持 Mustache 模板（`{{variable}}`）和 `.format()` 填充

## 目录结构

```
05-prompt-library/
├── README.md
├── prompt_lib/
│   ├── __init__.py
│   ├── settings.py          # Opik 连接配置（单点真理）
│   └── prompts.py           # Hard-coded prompts 示例（"迁移前" vs "迁移后"）
├── run_01_register_prompts.py    # 注册 prompts → Prompt Library
├── run_02_use_prompts.py         # 生产级使用（pin + 模板 + trace 联动）
└── run_03_prompt_evolution.py    # 版本演进工作流（V1→V2→V3→回滚）
```

## 快速开始

**前提**：Opik 服务已启动（`docker compose -f docker-compose.opik.yml up -d`）。

### 1. 注册 prompt 到 Opik Prompt Library

```bash
uv run python experiments/05-prompt-library/run_01_register_prompts.py
```

创建 3 个 prompt，其中 `customer_service_system` 会生成 V1 和 V2 两个版本。前往 UI → Prompt Library 查看。

### 2. 生产级使用演示

```bash
uv run python experiments/05-prompt-library/run_02_use_prompts.py
```

演示：
- 拉取 prompt（最新版 vs pin commit）
- 模板填充（`.format()`）
- Prompt 版本号记录到 trace metadata

### 3. 版本演进工作流

```bash
uv run python experiments/05-prompt-library/run_03_prompt_evolution.py
```

演示完整的 prompt 生命周期：V1 创建 → V2 迭代（多订单支持） → V3（情绪检测）→ 版本对比 → 回滚验证。

## API 参考

> 与 `opik-skills` 推荐 API 对齐 —— `opik.Prompt(...)` / `opik.ChatPrompt(...)` 已 deprecated，
> 一律走 client 方法。

| 方法 | 说明 |
|------|------|
| `client.create_prompt(name=, prompt=, metadata=)` | 创建/注册 string prompt，同名不同内容 = 新版本 |
| `client.create_chat_prompt(name=, messages=, metadata=)` | 创建 multi-turn chat 模板 |
| `client.get_prompt(name=)` | 获取 string prompt 最新版本 |
| `client.get_prompt(name=, commit=)` | Pin 到特定 commit（生产推荐） |
| `client.get_chat_prompt(name=)` | 获取 chat prompt 最新版本 |
| `prompt.format(**kwargs)` | Mustache 模板填充 |
| `prompt.commit` | 当前版本的 commit hash |
| `prompt.metadata` | 同版本绑定的 model / temperature 等参数 |

> Skill 强调：`get_prompt()` 必须在 `@opik.track` 装饰的函数内调用，否则 prompt 版本不会
> 链接到 trace，UI 看不见 —— 见 `.agents/skills/opik/SKILL.md` 第 226 行 CRITICAL 段。

## 生产环境最佳实践

```python
# config.py — 统一管理所有 prompt 的 commit
PROMPT_COMMITS = {
    "customer_service_system": "a1b2c3d4e5f6...",  # 经过测试批准的版本
    "user_question_template": "7f8g9h0i1j2k...",
}

# 使用时 pin 到批准版本
system_prompt = client.get_prompt(
    name="customer_service_system",
    commit=PROMPT_COMMITS["customer_service_system"]
).prompt
```

**更新流程**：
1. 在 Prompt Playground 编辑 → 测试
2. 用 evaluation 对比新旧版本效果
3. 验证通过后，更新 `PROMPT_COMMITS` 中的 commit hash
4. 部署配置 → prompt 即时生效，无需改代码

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `OPIK_HOST` | `http://localhost:5173/api` | Opik 服务地址 |
| `OPIK_WORKSPACE` | `default` | 工作空间 |
| `OPIK_PROJECT` | `prompt-library-demo` | 项目名称 |

## 进阶：Prompt + Evaluation 联动

实验 04 展示了 evaluation 的能力。结合 Prompt Library：
1. 用不同 commit 的 prompt 跑同一条 evaluation dataset
2. 对比各版本的准确率、幻觉率等指标
3. 数据驱动地决定晋升哪个版本到生产

提示：`client.get_prompt(name=..., commit=...)` 返回的 `prompt` 字段可以直接传给 evaluation 的 `task` 函数。