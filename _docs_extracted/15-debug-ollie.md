Your agent returned the wrong answer, ignored context it was given, or took twice as long as it should. The trace is right there in Opik — but tracing alone doesn’t tell you *why* it happened or how to fix it. That’s where [Ollie](https://www.comet.com/docs/opik/ollie) comes in.

## What Ollie has access to

Ollie is more than a chatbot — it has tools that let it act on your workspace and your code.

- **Read and analyze traces** — Ollie reads full span trees including inputs, outputs, latencies, token counts, and feedback scores. It can drill into individual spans, compare traces side by side, and search across your project for patterns.
- **Search your workspace** — Traces, threads, datasets, experiments, and prompts are all queryable. Ollie can aggregate data, find outliers, and surface trends you’d otherwise need to query manually.
- **Read and edit your code** — When you connect your repository with [`opik connect`](https://www.comet.com/docs/opik/development/agent-playground), Ollie gains secure, read-only access to your source files. It can propose edits that you review and approve before anything changes on disk.
- **Run your agent** — With `opik connect` active, Ollie can rerun your agent using inputs from a failing trace to verify a fix in real time. New traces stream back into Opik automatically.
- **Manage test suites** — Ollie can add traces as test cases to test suites, define assertions, trigger evaluation runs, and summarize pass/fail results.
- **Navigate the Opik UI** — Ollie can link you directly to traces, experiments, datasets, and prompts it references during a conversation.

Code access and agent execution require [`opik connect`](https://www.comet.com/docs/opik/development/agent-playground) to be running in your project directory. Without it, Ollie can still analyze traces and search your workspace but cannot read your source files or rerun your agent.

## The debug-fix-verify loop

The fastest way to improve agent quality is a tight loop: find a bad trace, understand it, fix it, and make sure it stays fixed. Ollie handles this end-to-end.

[^1]

### Find a failing trace

Start in the Opik dashboard. Filter traces by error status, low feedback score, or latency spike to find a run that didn’t behave as expected.

[^2]

### Ask Ollie what went wrong

Open Ollie from the trace view and describe what looks off. Ollie reads the full span tree — every LLM call, tool invocation, and retrieval step — and identifies the root cause.

![Ollie analyzing a trace and identifying the root cause](https://files.buildwithfern.com/https://opik.docs.buildwithfern.com/docs/opik/cc6e36d7e4c5c970af552a48767c8d9f24ea0559095b6899fe8f9d3c1c72ca8f/img/v2/ollie/step-2-ask-ollie.png)

Ollie analyzing a trace and identifying the root cause

[^3]

### Let Ollie fix your code

Once Ollie knows where the bug lives, it reads the relevant source file via `opik connect` and proposes a change. You see the diff and approve it — nothing happens without your click.

![Ollie proposing a code fix with a diff view](https://files.buildwithfern.com/https://opik.docs.buildwithfern.com/docs/opik/2692e7aa086d5961b10c3182c64eb4e1158550828b201e025c059da52dde6f87/img/v2/ollie/step-4-suggested-fix.png)

Ollie proposing a code fix with a diff view

[^4]

### Verify with a test suite

Ask Ollie to add the original trace as a regression test case, then run the suite against your updated agent. You get a pass/fail summary and a test that catches the bug if it ever comes back.

![Ollie running a test suite and showing pass/fail results](https://files.buildwithfern.com/https://opik.docs.buildwithfern.com/docs/opik/5257da8decefa09cd73ff47ae9fdf21836e406355bc48a972099dbc230ab0417/img/v2/ollie/step-6-eval-verification.png)

Ollie running a test suite and showing pass/fail results

Each cycle makes your agent more robust. Over time, your test suite becomes a comprehensive regression guard built directly from real failures.

## Example prompts

Ollie works best when you describe the problem in plain language. Here are prompts for common debugging scenarios:

### Investigating failures

- *“Why did the final answer ignore the retrieved context?”*
- *“Which span caused the latency spike in this trace?”*
- *“The tool call returned empty — what went wrong?”*

### Comparing traces

- *“Compare this failed trace to a recent successful one for the same query”*
- *“Find all traces where the tool call timed out this week”*
- *“What changed between the last successful run and this failure?”*

### Building test coverage

- *“Add this trace to my customer-support-qa suite with the assertion: the response must cite a specific step from the provided context”*
- *“Run the customer-support-qa suite against the updated prompt”*
- *“Why did 3 of the 5 items in this run fail?”*

### Understanding your workspace

- *“Show me the dataset for the last experiment”*
- *“What’s the average latency for traces in this project over the past week?”*
- *“Which prompts are used by the most experiments?”*

## Next steps

- [Ollie overview](https://www.comet.com/docs/opik/ollie) — Full introduction to Ollie’s capabilities and setup
- [Agent playground](https://www.comet.com/docs/opik/development/agent-playground) — How `opik connect` discovers and runs your agent
- [Evaluation overview](https://www.comet.com/docs/opik/evaluation/overview) — Build the regression net Ollie populates for you

[^1]: [1](https://www.comet.com/docs/opik/tracing/debug-agents#find-a-failing-trace)

### Find a failing trace

Start in the Opik dashboard. Filter traces by error status, low feedback score, or latency spike to find a run that didn’t behave as expected.

[^2]: [2](https://www.comet.com/docs/opik/tracing/debug-agents#ask-ollie-what-went-wrong)

### Ask Ollie what went wrong

Open Ollie from the trace view and describe what looks off. Ollie reads the full span tree — every LLM call, tool invocation, and retrieval step — and identifies the root cause.

![Ollie analyzing a trace and identifying the root cause](https://files.buildwithfern.com/https://opik.docs.buildwithfern.com/docs/opik/cc6e36d7e4c5c970af552a48767c8d9f24ea0559095b6899fe8f9d3c1c72ca8f/img/v2/ollie/step-2-ask-ollie.png)

Ollie analyzing a trace and identifying the root cause

[^3]: [3](https://www.comet.com/docs/opik/tracing/debug-agents#let-ollie-fix-your-code)

### Let Ollie fix your code

Once Ollie knows where the bug lives, it reads the relevant source file via `opik connect` and proposes a change. You see the diff and approve it — nothing happens without your click.

![Ollie proposing a code fix with a diff view](https://files.buildwithfern.com/https://opik.docs.buildwithfern.com/docs/opik/2692e7aa086d5961b10c3182c64eb4e1158550828b201e025c059da52dde6f87/img/v2/ollie/step-4-suggested-fix.png)

Ollie proposing a code fix with a diff view

[^4]: [4](https://www.comet.com/docs/opik/tracing/debug-agents#verify-with-a-test-suite)

### Verify with a test suite

Ask Ollie to add the original trace as a regression test case, then run the suite against your updated agent. You get a pass/fail summary and a test that catches the bug if it ever comes back.

![Ollie running a test suite and showing pass/fail results](https://files.buildwithfern.com/https://opik.docs.buildwithfern.com/docs/opik/5257da8decefa09cd73ff47ae9fdf21836e406355bc48a972099dbc230ab0417/img/v2/ollie/step-6-eval-verification.png)

Ollie running a test suite and showing pass/fail results