If you want to jump straight to code, head to the [Getting started](https://www.comet.com/docs/opik/tracing/getting-started) guide to add tracing in under five minutes.

LLM applications are more than a single API call. A typical agent involves retrieval steps, tool calls, prompt assembly, multiple LLM invocations, and post-processing — all wired together in ways that are invisible at runtime. When something goes wrong, you need to see exactly what happened at every step.

Opik gives you full visibility into every request your agent handles. Every LLM call, every tool invocation, every retrieval step is captured as a trace you can inspect, search, and analyze.

![](https://files.buildwithfern.com/https://opik.docs.buildwithfern.com/docs/opik/509190201962bdf0a77fb8d701a1a9acd32dcc3522b3e1e885c4d2f537760905/img/v2/observability/traces_overview.png)

See the full execution path of every request — from user input through tool calls and LLM completions to the final response Root-cause production issues fast — filter and search traces by status, latency, cost, or custom tags to find the problem in seconds Track costs and latency over time — monitor token usage and spending across models and providers Capture multi-turn conversations — group related traces into threads to understand how interactions evolve across turns Close the feedback loop — attach human or automated scores to traces and use them to drive evaluations

## Why use Opik for observability

Debugging LLM applications without observability means guessing. You see the final output but not why the model hallucinated, which retrieval step returned irrelevant context, or where latency spiked.

With Opik, you can:

- **See the full execution path** of every request — from user input through tool calls and LLM completions to the final response
- **Root-cause production issues fast** — filter and search traces by status, latency, cost, or custom tags to find the problem in seconds
- **Track costs and latency over time** — monitor token usage and spending across models and providers
- **Capture multi-turn conversations** — group related traces into threads to understand how interactions evolve across turns
- **Close the feedback loop** — attach human or automated scores to traces and use them to drive evaluations

## What you can capture

[<svg data-prefix="far" data-icon="diagram-project" role="img" viewBox="0 0 512 512" aria-hidden="true" width="100%" height="100%"><defs><style>.fa-secondary{opacity:.4}</style></defs><path fill="currentColor" d="M48 80l0 96 96 0 0-96-96 0zM0 80C0 53.5 21.5 32 48 32l96 0c26.5 0 48 21.5 48 48l0 24 128 0 0-24c0-26.5 21.5-48 48-48l96 0c26.5 0 48 21.5 48 48l0 96c0 26.5-21.5 48-48 48l-96 0c-26.5 0-48-21.5-48-48l0-24-128 0 0 24c0 10.4-3.3 20.1-9 28l63 84 90 0c26.5 0 48 21.5 48 48l0 96c0 26.5-21.5 48-48 48l-96 0c-26.5 0-48-21.5-48-48l0-96c0-10.4 3.3-20.1 9-28l-63-84-90 0c-26.5 0-48-21.5-48-48L0 80zM240 336l0 96 96 0 0-96-96 0zM464 80l-96 0 0 96 96 0 0-96z"></path></svg>](https://www.comet.com/docs/opik/tracing/concepts)

[Traces & spans](https://www.comet.com/docs/opik/tracing/concepts)

[

Full execution trees with inputs, outputs, timing, and metadata for every step

](https://www.comet.com/docs/opik/tracing/concepts)[<svg data-prefix="far" data-icon="dollar-sign" role="img" viewBox="0 0 320 512" aria-hidden="true" width="100%" height="100%"><defs><style>.fa-secondary{opacity:.4}</style></defs><path fill="currentColor" d="M136 24c0-13.3 10.7-24 24-24s24 10.7 24 24l0 40 64 0c13.3 0 24 10.7 24 24s-10.7 24-24 24l-130 0c-29.8 0-54 24.2-54 54 0 26.4 19.1 48.9 45.1 53.2l106.1 17.7c51.3 8.5 88.8 52.9 88.8 104.8 0 58.7-47.6 106.3-106.3 106.3l-13.7 0 0 40c0 13.3-10.7 24-24 24s-24-10.7-24-24l0-40-80 0c-13.3 0-24-10.7-24-24s10.7-24 24-24l141.7 0c32.2 0 58.3-26.1 58.3-58.3 0-28.5-20.6-52.8-48.7-57.5L101.2 266.5C52 258.3 16 215.8 16 166 16 109.6 61.6 64 118 64l18 0 0-40z"></path></svg>

Cost tracking

Token usage and spending broken down by model, provider, and trace

](https://www.comet.com/docs/opik/tracing/advanced/cost_tracking)[<svg data-prefix="far" data-icon="image" role="img" viewBox="0 0 448 512" aria-hidden="true" width="100%" height="100%"><defs><style>.fa-secondary{opacity:.4}</style></defs><path fill="currentColor" d="M64 80c-8.8 0-16 7.2-16 16l0 320c0 8.8 7.2 16 16 16l320 0c8.8 0 16-7.2 16-16l0-320c0-8.8-7.2-16-16-16L64 80zM0 96C0 60.7 28.7 32 64 32l320 0c35.3 0 64 28.7 64 64l0 320c0 35.3-28.7 64-64 64L64 480c-35.3 0-64-28.7-64-64L0 96zm128 32a32 32 0 1 1 0 64 32 32 0 1 1 0-64zm136 72c8.5 0 16.4 4.5 20.7 11.8l80 136c4.4 7.4 4.4 16.6 .1 24.1S352.6 384 344 384l-240 0c-8.9 0-17.2-5-21.3-12.9s-3.5-17.5 1.6-24.8l56-80c4.5-6.4 11.8-10.2 19.7-10.2s15.2 3.8 19.7 10.2l17.2 24.6 46.5-79c4.3-7.3 12.2-11.8 20.7-11.8z"></path></svg>

Media & attachments

Images, audio, video, and files logged alongside your traces

](https://www.comet.com/docs/opik/tracing/advanced/log_multimodal_traces)[<svg data-prefix="far" data-icon="thumbs-up" role="img" viewBox="0 0 512 512" aria-hidden="true" width="100%" height="100%"><defs><style>.fa-secondary{opacity:.4}</style></defs><path fill="currentColor" d="M171.5 38.8C192.3 4 236.5-10 274 7.6l7.2 3.8C316 32.3 330 76.5 312.4 114l0 0-14.1 30 109.7 0 7.4 .4c36.3 3.7 64.6 34.4 64.6 71.6 0 13.2-3.6 25.4-9.8 36 6.1 10.6 9.7 22.8 9.8 36 0 18.3-6.9 34.8-18 47.5 1.3 5.3 2 10.8 2 16.5 0 25.1-12.9 47-32.2 59.9-1.9 35.5-29.4 64.2-64.4 67.7l-7.4 .4-104.1 0c-18 0-35.9-3.4-52.6-9.9l-7.1-3-.7-.3-6.6-3.2-.7-.3-12.2-6.5c-12.3-6.5-23.3-14.7-32.9-24.1-4.1 26.9-27.3 47.4-55.3 47.4l-32 0c-30.9 0-56-25.1-56-56L0 200c0-30.9 25.1-56 56-56l32 0c10.8 0 20.9 3.1 29.5 8.5l50.1-106.5 .6-1.2 2.7-5 .6-.9zM56 192c-4.4 0-8 3.6-8 8l0 224c0 4.4 3.6 8 8 8l32 0c4.4 0 8-3.6 8-8l0-224c0-4.4-3.6-8-8-8l-32 0zM253.6 51c-14.8-6.9-32.3-1.6-40.7 12l-2.2 4-56.8 120.9c-3.5 7.5-5.5 15.5-6 23.7l-.1 4.2 0 112.9 .2 7.9c2.4 32.7 21.4 62.1 50.7 77.7l11.5 6.1 6.3 3.1c12.4 5.6 25.8 8.5 39.4 8.5l104.1 0 2.4-.1c12.1-1.2 21.6-11.5 21.6-23.9l-.2-2.6c-.1-.9-.2-1.7-.4-2.6-2.7-12.1 4.3-24.2 16-28 9.7-3.1 16.6-12.2 16.6-22.8 0-4.3-1.1-8.2-3.1-11.8-6.3-11.1-2.8-25.2 8-32 6.8-4.3 11.2-11.8 11.2-20.2 0-7.1-3.1-13.5-8.2-18-5.2-4.6-8.2-11.1-8.2-18s3-13.4 8.2-18c5.1-4.5 8.2-10.9 8.2-18l-.1-2.4c-1.1-11.3-10.1-20.3-21.4-21.4l-2.4-.1-147.5 0c-8.2 0-15.8-4.2-20.2-11.1-4.4-6.9-5-15.7-1.5-23.1L269 93.6c7-15 1.4-32.7-12.5-41L253.6 51z"></path></svg>

User feedback

Qualitative and quantitative scores attached to individual traces

](https://www.comet.com/docs/opik/tracing/advanced/annotate_traces)[<svg data-prefix="far" data-icon="share-nodes" role="img" viewBox="0 0 512 512" aria-hidden="true" width="100%" height="100%"><defs><style>.fa-secondary{opacity:.4}</style></defs><path fill="currentColor" d="M432 96a48 48 0 1 0 -96 0 48 48 0 1 0 96 0zm48 0c0 53-43 96-96 96-27.4 0-52.1-11.5-69.6-29.9L188.9 231.8c2 7.7 3.1 15.8 3.1 24.2s-1.1 16.5-3.1 24.2l125.5 69.7c17.5-18.4 42.2-29.9 69.6-29.9 53 0 96 43 96 96s-43 96-96 96-96-43-96-96c0-8.3 1.1-16.5 3.1-24.2L165.6 322.1C148.1 340.5 123.4 352 96 352 43 352 0 309 0 256s43-96 96-96c27.4 0 52.1 11.5 69.6 29.9l125.5-69.7c-2-7.7-3.1-15.8-3.1-24.2 0-53 43-96 96-96s96 43 96 96zM144 256a48 48 0 1 0 -96 0 48 48 0 1 0 96 0zM384 464a48 48 0 1 0 0-96 48 48 0 1 0 0 96z"></path></svg>

Agent graphs

Visual execution graphs showing how your agent’s steps connect

](https://www.comet.com/docs/opik/tracing/advanced/log_agent_graphs)

## How it works

[^1]

### Connect your project

Run `opik connect` from your agent’s directory to pair it with Opik:

```bash
$opik connect --project <YOUR_PROJECT_NAME>
```

[^2]

### Instrument your code

The fastest way to add tracing is with [opik-skills](https://github.com/comet-ml/opik-skills) — install the skill and let your coding agent handle the rest:

```bash
$npx skills add comet-ml/opik-skills
```

Then ask your coding agent:

```
Instrument my agent with Opik using the /instrument command.
```

This works with Claude Code, Cursor, Codex, OpenCode, and other coding agents. You can also instrument manually with the SDK:

```
1import opik
2
3@opik.track
4def my_agent(user_message):
5    context = retrieve_context(user_message)
6    response = call_llm(user_message, context)
7    return response
```

[^3]

### View traces in the dashboard

Every request creates a trace with detailed span-level information. You can inspect the full execution tree, see inputs and outputs at each step, and filter by duration, cost, status, or tags.

![](https://files.buildwithfern.com/https://opik.docs.buildwithfern.com/docs/opik/7ae96ef9813496e5a30bd54e2cce832bdc78ff2b7962ba4b97a242386ef94f69/img/v2/home/traces_page_for_quickstart.png)

[^4]

### Analyze and improve

Use traces to debug failures, identify slow steps, and track quality over time. Attach feedback scores, run evaluations against datasets, and use [Ollie](https://www.comet.com/docs/opik/tracing/debug-agents) — Opik’s AI assistant — to help root-cause issues automatically.

## Integrations

Opik has first-class support for 30+ frameworks in Python, TypeScript, and OpenTelemetry — so you can start capturing traces without changing how your application is built.

**[View all integrations →](https://www.comet.com/docs/opik/integrations/overview)**

## Next steps

- [Getting started](https://www.comet.com/docs/opik/tracing/getting-started) — Add observability to your agent in minutes
- [Concepts](https://www.comet.com/docs/opik/tracing/concepts) — Understand traces, spans, threads, and feedback scores
- [Debugging agents with Ollie](https://www.comet.com/docs/opik/tracing/debug-agents) — Use AI-assisted root-cause analysis
- [Cost tracking](https://www.comet.com/docs/opik/tracing/advanced/cost_tracking) — Monitor token usage and spending

[^1]: [1](https://www.comet.com/docs/opik/tracing/overview#connect-your-project)

### Connect your project

Run `opik connect` from your agent’s directory to pair it with Opik:

```bash
$opik connect --project <YOUR_PROJECT_NAME>
```

[^2]: [2](https://www.comet.com/docs/opik/tracing/overview#instrument-your-code)

### Instrument your code

The fastest way to add tracing is with [opik-skills](https://github.com/comet-ml/opik-skills) — install the skill and let your coding agent handle the rest:

```bash
$npx skills add comet-ml/opik-skills
```

Then ask your coding agent:

```
Instrument my agent with Opik using the /instrument command.
```

This works with Claude Code, Cursor, Codex, OpenCode, and other coding agents. You can also instrument manually with the SDK:

```
1import opik
2
3@opik.track
4def my_agent(user_message):
5    context = retrieve_context(user_message)
6    response = call_llm(user_message, context)
7    return response
```

[^3]: [3](https://www.comet.com/docs/opik/tracing/overview#view-traces-in-the-dashboard)

### View traces in the dashboard

Every request creates a trace with detailed span-level information. You can inspect the full execution tree, see inputs and outputs at each step, and filter by duration, cost, status, or tags.

![](https://files.buildwithfern.com/https://opik.docs.buildwithfern.com/docs/opik/7ae96ef9813496e5a30bd54e2cce832bdc78ff2b7962ba4b97a242386ef94f69/img/v2/home/traces_page_for_quickstart.png)

[^4]: [4](https://www.comet.com/docs/opik/tracing/overview#analyze-and-improve)

### Analyze and improve

Use traces to debug failures, identify slow steps, and track quality over time. Attach feedback scores, run evaluations against datasets, and use [Ollie](https://www.comet.com/docs/opik/tracing/debug-agents) — Opik’s AI assistant — to help root-cause issues automatically.