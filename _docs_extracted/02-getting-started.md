Opik makes it easy to add observability to your existing LLM application. The fastest way is to let your coding agent do it — install the Opik skill in Claude Code, Cursor, Codex, or any other coding agent and it will instrument your code for you. If you’d rather stay inside Opik, use Opik Connect to have [Ollie](https://www.comet.com/docs/opik/ollie) set up tracing from the dashboard. You can also add tracing manually with the SDK.

<video src="https://files.buildwithfern.com/https://opik.docs.buildwithfern.com/docs/opik/6a802877768b4b249a82bbc014713b5830676ffb162175e7fcb2b1b60db2d73d/img/v2/observability/getting-started.mp4" width="854" height="480" controls=""></video>

## Adding observability to your code

###### AI coding agent

###### Opik Connect

###### Manual integration

The fastest way to add observability is to install the Opik skill in your coding agent and let it instrument your code for you. The skill is compatible with Claude Code, Codex, Cursor, OpenCode and any other agent that supports skills.

[^1]

### Install the Opik skill

```bash
$npx skills add comet-ml/opik-skills
```

[^2]

### Run the integration

Ask your coding agent to instrument your code:

```
Instrument my agent with Opik using the /instrument command.
```

The agent will read your code, pick the right Opik integration, and add tracing.

## Viewing your traces

After running your application, traces will appear in the Opik dashboard. Each trace captures the full execution path of a request, including all nested spans, inputs, outputs, and timing information.

![Opik traces page showing trace details with span tree, outputs, and feedback scores](https://files.buildwithfern.com/https://opik.docs.buildwithfern.com/docs/opik/509190201962bdf0a77fb8d701a1a9acd32dcc3522b3e1e885c4d2f537760905/img/v2/observability/traces-page.png)

Opik traces page showing trace details with span tree, outputs, and feedback scores

You can use [Ollie](https://www.comet.com/docs/opik/ollie) to analyze your traces, identify issues in your agent’s behavior, and get actionable suggestions for improvement.

## Next steps

- [Concepts](https://www.comet.com/docs/opik/tracing/concepts) — Learn about traces, spans, threads, and feedback scores
- [Log traces](https://www.comet.com/docs/opik/tracing/advanced/log_traces) — In-depth guide on customizing what gets logged
- [Cost tracking](https://www.comet.com/docs/opik/tracing/advanced/cost_tracking) — Monitor token usage and spending

[^1]: [1](https://www.comet.com/docs/opik/tracing/getting-started#install-the-opik-skill)

### Install the Opik skill

```bash
$npx skills add comet-ml/opik-skills
```

[^2]: [2](https://www.comet.com/docs/opik/tracing/getting-started#run-the-integration)

### Run the integration

Ask your coding agent to instrument your code:

```
Instrument my agent with Opik using the /instrument command.
```

The agent will read your code, pick the right Opik integration, and add tracing.