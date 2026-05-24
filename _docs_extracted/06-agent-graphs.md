Agent Graphs are a great way to visualize the flow of an agent and simplifies it’s debugging.

![](https://files.buildwithfern.com/https://opik.docs.buildwithfern.com/docs/opik/fe85b7f2855f7e02aa74fdccae736d557b71806abc45560e8b9dcffcf9c478b7/img/tracing/agent_definition.png)

Agent hierarchy and relationships Sequential execution flows Parallel processing branches Tool connections and dependencies Loop structures and iterations

Opik supports logging agent graphs for the following frameworks:

1. LangGraph
2. Google Agent Development Kit (ADK)
3. Manual Tracking

## LangGraph

You can log the agent execution graph by specifying the `graph` parameter in the [OpikTracer](https://www.comet.com/docs/opik/python-sdk-reference/integrations/langchain/OpikTracer.html) callback:

```python
1from opik.integrations.langchain import OpikTracer
2
3opik_tracer = OpikTracer(graph=app.get_graph(xray=True))
```

Opik will log the agent graph definition in the Opik dashboard which you can access by clicking on `Show Agent Graph` in the trace sidebar.

## Google Agent Development Kit (ADK)

Opik automatically generates visual representations of your agent workflows for Google ADK without requiring any additional configuration. Simply integrate Opik’s OpikTracer callback as shown in the [ADK integration configuration guide](https://www.comet.com/docs/opik/integrations/adk#configuring-google-adk), and your agent graphs will be automatically captured and visualized.

The graph automatically shows:

- Agent hierarchy and relationships
- Sequential execution flows
- Parallel processing branches
- Tool connections and dependencies
- Loop structures and iterations

For example, a basic weather and time agent will display its execution flow with all agent steps, LLM calls, and tool invocations:

![](https://files.buildwithfern.com/https://opik.docs.buildwithfern.com/docs/opik/b60f4a7e77a1d76194a3f93513c0b1f75a62e2bb110665a19a22c7e0582ee770/img/tracing/adk/adk_weather_time_graph_screenshot.png)

Agent hierarchy and relationships Sequential execution flows Parallel processing branches Tool connections and dependencies Loop structures and iterations

For more complex multi-agent architectures, the automatic graph visualization becomes even more valuable, providing clear visibility into nested agent hierarchies and complex execution patterns.

## Manual Tracking

You can also log the agent graph definition manually by logging the agent graph definition as a mermaid graph definition in the metadata of the trace:

```python
1import opik
2from opik import opik_context
3
4@opik.track
5def chat_agent(input: str):
6  # Update the current trace with the agent graph definition
7  opik_context.update_current_trace(
8    metadata={
9      "_opik_graph_definition": {
10        "format": "mermaid",
11            "data": "graph TD; U[User]-->A[Agent]; A-->L[LLM]; L-->A; A-->R[Answer];"
12      }
13    }
14  )
15  return "Hello, how can I help you today?"
16
17chat_agent("Hi there!")
```

Opik will log the agent graph definition in the Opik dashboard which you can access by clicking on `Show Agent Graph` in the trace sidebar.

## Next steps

Why not check out:

- [Opik’s 50+ integrations](https://www.comet.com/docs/opik/integrations/overview)
- [Logging traces](https://www.comet.com/docs/opik/tracing/advanced/log_traces)
- [Evaluating agents](https://www.comet.com/docs/opik/evaluation/evaluate_agents)