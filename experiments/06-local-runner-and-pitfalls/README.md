# 实验 06 — Local Runner 与三大陷阱

> 用可运行的代码把 opik-skills 里反复强调的三件事变成真实示例。

## 为什么有这个模块

opik-skills 反复强调三件事 — entrypoint primitives / opik connect / LiteLLM current_span_data — 本仓库之前都没演示。这里补齐。

具体说，之前的实验展示了基本 tracing 和 feedback，但有三个生产级细节始终缺失：

1. `@opik.track(entrypoint=True)` 的参数必须是 primitive 类型，否则 Local Runner UI 无法渲染表单
2. 用 `opik connect` 把本地脚本配对到 Opik UI，实现无需部署就能从 UI 触发运行
3. `litellm.completion` 在 `@opik.track` 内使用时，必须传 `current_span_data`，否则产生孤儿 trace

## 目录结构

```
06-local-runner-and-pitfalls/
├── README.md
├── run_01_entrypoint_demo.py    # Entrypoint primitives + Local Runner
└── run_02_litellm_orphan_fix.py # LiteLLM 孤儿 trace 复现 + 修复
```

## 依赖

本实验需要 `litellm`：

```bash
# uv 项目
uv add litellm

# 或 pip
pip install litellm
```

注：如果你的项目已经间接依赖 opik 的集成扩展，litellm 可能已经存在。run_02 脚本默认使用 mock 模式，不需要任何 API key。

## 实验一：Entrypoint 参数规则

### 什么是 Local Runner

Opik Local Runner 允许你从 Opik UI 直接触发本地脚本，免去部署环节。UI 会读取 `entrypoint=True` 函数的 type hint，为每个参数生成输入表单。这要求 entrypoint 的参数必须是 primitive 类型。

### 规则

| 允许的参数类型 | 不允许的参数类型 |
|--------------|----------------|
| `str` | Pydantic model |
| `int` | dataclass |
| `float` | 自定义 class |
| `bool` | `dict` 嵌套复杂对象 |
| `list[str]` 等基础 list | request/response 对象 |

**正确写法**：创建 thin wrapper，wrapper 只接受 primitives，内部拼出复杂对象再调业务逻辑：

```python
# ✅ entrypoint 只接受 primitives — UI 可渲染表单
@opik.track(name="recommend-agent", entrypoint=True)
def run_entrypoint(city: str, category: str, max_results: int = 3) -> dict:
    request = RecommendRequest(city=city, category=category, max_results=max_results)
    return run_recommend(request)

# ✅ 业务逻辑接受复杂类型，但没有 entrypoint 标记
@opik.track(name="recommend-core")
def run_recommend(request: RecommendRequest) -> dict:
    ...
```

**错误写法**：

```python
# ❌ RecommendRequest 不是 primitive — Local Runner 无法渲染
@opik.track(name="recommend-agent", entrypoint=True)
def bad_entrypoint(request: RecommendRequest) -> dict:
    ...
```

### 运行

```bash
uv run python experiments/06-local-runner-and-pitfalls/run_01_entrypoint_demo.py
```

## 如何端到端验证 opik connect

`opik connect` 把本地进程配对到 Opik UI，让你在 UI 里填表单、点 Run，脚本在本机执行，trace 自动上报。

**步骤：**

1. 启动 Opik Docker 服务（如果还没启动）：

   ```bash
   docker compose -f docker-compose.opik.yml up -d
   ```

   验证服务正常：
   ```bash
   curl http://localhost:5173/api/is-alive/ping
   # 应返回 {"message":"Healthy Server","healthy":true}
   ```

2. 在 Opik UI 获取配对码：
   - 打开 http://localhost:5173
   - 导航到 **Local Runner** 页面（左侧导航栏）
   - 点击 **New Runner**，复制显示的配对码（格式类似 `ABC-123`）

3. 在终端运行配对命令：

   ```bash
   opik connect --pair <CODE> \
     uv run python experiments/06-local-runner-and-pitfalls/run_01_entrypoint_demo.py
   ```

   把 `<CODE>` 替换为第 2 步获取的配对码。

4. 回到 Opik UI，Local Runner 页面应显示 runner 已连接。点击 **Run**，在弹出的表单中填入：
   - `city`: `Shanghai`
   - `category`: `coffee shop`
   - `max_results`: `3`

5. 点击 **Run**，观察本地终端的输出，以及 Opik UI → Projects → `opik-exp-06-entrypoint` 中新生成的 trace。

## 孤儿 trace 是什么

### 问题根源

`litellm` 的 `OpikLogger` 回调会自动创建 trace/span。但它需要知道"当前活跃的 span 是哪个"，才能把 LLM call 挂在正确的父节点下。

如果你在 `@opik.track` 函数里调用 `litellm.completion`，但没有通过 `metadata` 传递当前 span 信息，`OpikLogger` 找不到父节点，就会在 Opik 里创建一个独立的顶层 trace —— 这就是"孤儿 trace"。

### ASCII 对比图

**你以为得到的（FIXED，正确）：**

```
Trace: fixed-agent
└── Span: fixed-llm-call
    └── Span: litellm/gpt-4o-mini   <-- 正确挂在父级下
```

**实际得到的（BROKEN，错误）：**

```
Trace: broken-agent
└── Span: broken-llm-call
    (LLM call 不见了！)

Trace: litellm/gpt-4o-mini          <-- 孤儿：独立的顶层 trace，无父级
```

UI 里会看到两条 trace，而你期望只有一条。

### 修复方式

在每次 `litellm.completion` 调用时加上 `metadata`：

```python
from opik.opik_context import get_current_span_data

@opik.track
def call_llm(messages):
    return litellm.completion(
        model="gpt-4o-mini",
        messages=messages,
        metadata={
            "opik": {
                "current_span_data": get_current_span_data(),  # 关键
                "tags": ["litellm"],
            },
        },
    )
```

`get_current_span_data()` 返回当前活跃 span 的引用，`OpikLogger` 用它把 LLM call 嵌套到正确位置。

### 运行演示

```bash
# 默认使用 mock 模式，无需 API key
uv run python experiments/06-local-runner-and-pitfalls/run_02_litellm_orphan_fix.py

# 如有 OpenAI API key，自动切换到 gpt-4o-mini 真实调用
OPENAI_API_KEY=sk-... uv run python experiments/06-local-runner-and-pitfalls/run_02_litellm_orphan_fix.py
```

脚本会打印每个 case 的预期行为，前往 Opik UI 验证。

## 三个陷阱总结

| 陷阱 | 症状 | 修复 |
|------|------|------|
| entrypoint 参数不是 primitive | Local Runner 无法渲染表单，或表单字段缺失 | 用 thin wrapper 接受 primitives，内部构造复杂对象 |
| 未配对 `opik connect` | 本地脚本无法从 UI 触发 | `opik connect --pair <CODE> <command>` |
| LiteLLM 缺少 `current_span_data` | UI 出现多余的孤儿顶层 trace | 在 `metadata["opik"]["current_span_data"]` 传入 `get_current_span_data()` |
