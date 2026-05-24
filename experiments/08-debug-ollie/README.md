# 08 — Debugging Agents with Ollie

> 基于真实文档更新

## Ollie 是什么

Ollie = Opik LLM Investigator。是 Opik 内置的 AI 助手，用于自动根因分析和修复 Agent 问题。

## Ollie 的能力（文档原文）

1. **读取和分析 Trace** — 读取完整 Span 树，包括 input/output、延迟、Token 数和反馈分数
2. **搜索工作空间** — 查询 Traces、Threads、Datasets、Experiments、Prompts
3. **读取和编辑代码** — 通过 `opik connect` 获得源码只读访问
4. **运行 Agent** — 用失败 Trace 的输入重新运行 Agent，验证修复
5. **管理测试套件** — 将 Trace 添加为测试用例，定义断言，触发评估
6. **导航 UI** — 直接链接到 Trace、Experiment、Dataset

> 代码访问和 Agent 执行需要 `opik connect` 在项目目录中运行

## Debug-Fix-Verify 循环

```
1. 找到失败 Trace ──→ 2. 问 Ollie 原因 ──→ 3. Ollie 修复代码 ──→ 4. 验证
```

1. **Find a failing trace** — Dashboard 中按 error/low score/latency 过滤
2. **Ask Ollie what went wrong** — Ollie 读取完整 Span 树，定位根因
3. **Let Ollie fix your code** — 通过 `opik connect` 读取源码，提出 diff，你确认
4. **Verify with a test suite** — 添加 Trace 为回归测试用例，运行套件

## 推荐的 Prompt 示例

**调查失败**: "Why did the final answer ignore the retrieved context?"
**比较 Trace**: "Compare this failed trace to a recent successful one for the same query"
**构建测试**: "Add this trace to my customer-support-qa suite with the assertion..."
**理解工作空间**: "What's the average latency for traces in this project over the past week?"