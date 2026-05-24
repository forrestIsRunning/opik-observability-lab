Opik has been designed to track and monitor costs for your LLM applications by measuring token usage across all traces. Using the Opik dashboard, you can analyze spending patterns and quickly identify cost anomalies. All costs across Opik are estimated and displayed in USD.

## Monitoring Costs in the Dashboard

You can use the Opik dashboard to review costs at three levels: spans, traces, and projects. Each level provides different insights into your application’s cost structure.

### Span-Level Costs

Individual spans show the computed costs (in USD) for each LLM spans of your traces:

![](https://files.buildwithfern.com/https://opik.docs.buildwithfern.com/docs/opik/26e16cce0421d3bda2609c11088a4375cf8714c0f37c619cfb380fcfa8c4e186/img/tracing/cost_tracking_span.png)

Using models or providers not yet supported by automatic cost tracking You have a custom pricing agreement with your provider You want to track additional costs beyond model usage You need to implement cost estimation as a background process Working with integrations where spans are automatically managed

### Trace-Level Costs

If you are using one of Opik’s integrations, we automatically aggregates costs from all spans within a trace to compute total trace costs:

![](https://files.buildwithfern.com/https://opik.docs.buildwithfern.com/docs/opik/8cf4021c1de6be704bbc119840d0008c6a50346bfd640e976835a573bf367f21/img/tracing/cost_tracking_trace_view.png)

Using models or providers not yet supported by automatic cost tracking You have a custom pricing agreement with your provider You want to track additional costs beyond model usage You need to implement cost estimation as a background process Working with integrations where spans are automatically managed

### Project-Level Analytics

Track your overall project costs in:

1. The main project view, through the Estimated Cost column:
	![](https://files.buildwithfern.com/https://opik.docs.buildwithfern.com/docs/opik/7f41db7266ca09606d32be42bf220a1b53c90001172875d77417535c1834b731/img/tracing/cost_tracking_project.png)
2. The project Metrics tab, which shows cost trends over time:
	![](https://files.buildwithfern.com/https://opik.docs.buildwithfern.com/docs/opik/ec4d95fdeb6758d97e362584f5eec766cdf92ea1661d8d0e44b92042eb8faa48/img/tracing/cost_tracking_project_metrics.png)

## Retrieving Costs Programmatically

You can retrieve the estimated cost programmatically for both spans and traces. Note that the cost will be `None` if the span or trace used an unsupported model. See [Exporting Traces and Spans](https://www.comet.com/docs/opik/v1/tracing/export_data) for more ways of exporting traces and spans.

### Retrieving Span Costs

```python
1import opik
2
3client = opik.Opik()
4
5span = client.get_span_content("<SPAN_ID>")
6# Returns estimated cost in USD, or None for unsupported models
7print(span.total_estimated_cost)
```

### Retrieving Trace Costs

```python
1import opik
2
3client = opik.Opik()
4
5trace = client.get_trace_content("<TRACE_ID>")
6# Returns estimated cost in USD, or None for unsupported models
7print(trace.total_estimated_cost)
```

## Manually setting the provider and model name

If you are not using one of Opik’s integration, Opik can still compute the cost. For you will need to ensure the span type is `llm` and you will need to pass:

1. `provider`: The name of the provider, typically `openai`, `anthropic` or `google_ai` for example (the most recent providers list can be found in `opik.LLMProvider` enum object)
2. `model`: The name of the model
3. `usage`: The input, output and total tokens for this LLM call.

You can then update your code to log traces and spans:

###### Function decorator

###### Low level Python SDK

If you are using function decorators, you will need to use the `update_current_span` method:

```python
1from opik import track, opik_context
2
3@track(type="llm") # Note - Specifying the type is this is important
4def llm_call(input):
5  opik_context.update_current_span(
6    provider="openai",
7    model="gpt-3.5-turbo",
8    usage={
9      "prompt_tokens": 4,
10      "completion_tokens": 6,
11      "total_tokens": 10
12    }
13  )
14  return "Hello, world!"
15
16llm_call("Hello world!")
```

## Manually Setting Span Costs

When you need to set a custom cost or use an unsupported model, you can manually set the cost of a span. There are two approaches depending on your use case:

### Setting Costs During Span Creation

If you’re manually creating spans, you can set the cost directly when creating the span:

```python
1from opik import track, opik_context
2
3@track
4def llm_call(input):
5  opik_context.update_current_span(
6    total_cost=0.05,
7  )
8  return "Hello, world!"
9
10llm_call("Hello world!")
```

### Updating Costs After Span Completion

With Opik integrations, spans are automatically created and closed, preventing updates while they’re open. However, you can update the cost afterward using the `update_span` method. This works well for implementing periodic cost estimation jobs:

```python
1from opik import Opik
2from opik.rest_api.types.span_public import SpanPublic
3
4# Define your own cost mapping for different models
5TOKEN_COST = {
6    ("openai.chat", "gpt-4o-2024-08-06"): {
7        "input_tokens": 2.5e-06,
8        "output_tokens": 1e-05,
9    }
10}
11
12# This part would be custom for your use-case and is only here for example
13def compute_cost_for_span(span: SpanPublic):
14    provider = span.provider or span.input.get("ai.model.provider")
15    model = span.model or span.output.get("gen_ai.response.model")
16    usage = span.usage
17
18    if (provider, model) in TOKEN_COST:
19        model_cost = TOKEN_COST[(provider, model)]
20        cost = (
21            usage["input_tokens"] * model_cost["input_tokens"]
22            + usage["output_tokens"] * model_cost["output_tokens"]
23        )
24        return cost
25    return None
26
27def update_span_costs(project_name, trace_id=None):
28    opik_client = Opik()
29
30    # Find LLM spans that don't have estimated costs
31    spans = opik_client.search_spans(
32        project_name=project_name,
33        trace_id=trace_id,
34        filter_string='type="llm" and total_estimated_cost=0',
35    )
36
37    for span in spans:
38        cost = compute_cost_for_span(span)
39
40        if cost:
41            print(f"Updating span {span.id} of trace {span.trace_id} with cost: {cost}")
42            opik_client.update_span(
43                trace_id=span.trace_id,
44                parent_span_id=span.parent_span_id,
45                project_name=project_name,
46                id=span.id,
47                total_cost=cost,
48            )
49
50# Example usage in a CRON job
51if __name__ == "__main__":
52    update_span_costs("your-project-name")
```

This approach is particularly useful when:

- Using models or providers not yet supported by automatic cost tracking
- You have a custom pricing agreement with your provider
- You want to track additional costs beyond model usage
- You need to implement cost estimation as a background process
- Working with integrations where spans are automatically managed

You can run the cost update function as a CRON job to automatically update costs for spans created without cost information. This is especially valuable in production environments where accurate cost data for all spans is essential.

## Supported Models, Providers, and Integrations

Opik currently calculates costs automatically for all LLM calls in the following Python SDK integrations:

- [Google ADK Integration](https://www.comet.com/docs/opik/integrations/adk)
- [AWS Bedrock Integration](https://www.comet.com/docs/opik/integrations/bedrock)
- [LangChain Integration](https://www.comet.com/docs/opik/integrations/langchain)
- [OpenAI Integration](https://www.comet.com/docs/opik/integrations/openai)
- [LiteLLM Integration](https://docs.litellm.ai/docs/observability/opik_integration)
- [Anthropic Integration](https://www.comet.com/docs/opik/integrations/anthropic)
- [CrewAI Integration](https://www.comet.com/docs/opik/integrations/crewai)
- [Google AI Integration](https://www.comet.com/docs/opik/integrations/gemini)
- [Haystack Integration](https://www.comet.com/docs/opik/integrations/haystack)
- [LlamaIndex Integration](https://www.comet.com/docs/opik/integrations/llama_index)

### Supported Providers

Cost tracking is supported for the following LLM providers (as defined in `opik.LLMProvider` enum):

- **OpenAI** (`openai`) - Models hosted by OpenAI ([https://platform.openai.com](https://platform.openai.com/))
- **Anthropic** (`anthropic`) - Models hosted by Anthropic ([https://www.anthropic.com](https://www.anthropic.com/))
- **Anthropic on Vertex AI** (`anthropic_vertexai`) - Anthropic models hosted by Google Vertex AI
- **Google AI** (`google_ai`) - Gemini models hosted in Google AI Studio ([https://ai.google.dev/aistudio](https://ai.google.dev/aistudio))
- **Google Vertex AI** (`google_vertexai`) - Gemini models hosted in Google Vertex AI ([https://cloud.google.com/vertex-ai](https://cloud.google.com/vertex-ai))
- **AWS Bedrock** (`bedrock`) - Models hosted by AWS Bedrock ([https://aws.amazon.com/bedrock](https://aws.amazon.com/bedrock))
- **Groq** (`groq`) - Models hosted by Groq ([https://groq.com](https://groq.com/))

You can find a complete list of supported models for these providers in the [model\_prices\_and\_context\_window.json file](https://github.com/comet-ml/opik/blob/main/apps/opik-backend/src/main/resources/model_prices_and_context_window.json).

We are actively expanding our cost tracking support. Need support for additional models or providers? Please [open a feature request](https://github.com/comet-ml/opik/issues) to help us prioritize development.