Logging user feedback and scoring traces is a crucial aspect of evaluating and improving your agent. By systematically recording qualitative or quantitative feedback on specific interactions or entire conversation flows, you can:

1. Track performance over time
2. Identify areas for improvement
3. Compare different model versions or prompts
4. Gather data for fine-tuning or retraining
5. Provide stakeholders with concrete metrics on system effectiveness

## Logging user feedback using the SDK

You can use the SDKs to log user feedback and score traces:

```
1import { Opik } from "opik";
2
3const client = new Opik();
4
5// Create a new trace with a span
6const trace = client.trace({
7  name: "my_trace",
8  input: { input: "Hi!" },
9  output: { output: "Hello!" },
10});
11
12const span = trace.span({
13  name: "processing",
14  input: { step: 1 },
15});
16span.update({ output: { result: "processed" } });
17span.end();
18trace.end();
19
20// Log feedback scores to existing traces
21client.logTracesFeedbackScores([
22  { id: trace.data.id, name: "overall_quality", value: 0.9, reason: "Good answer" },
23  { id: trace.data.id, name: "coherence", value: 0.8 }
24]);
25
26// Log feedback scores to existing spans
27client.logSpansFeedbackScores([
28  { id: span.data.id, name: "accuracy", value: 0.95 }
29]);
30
31// Flush to ensure all data is sent
32await client.flush();
```

## Annotating Traces through the UI

To annotate traces through the UI, you can navigate to the trace you want to annotate in the traces page and click on the `Annotate` button. This will open a sidebar where you can add annotations to the trace.

You can annotate both traces and spans through the UI, make sure you have selected the correct span in the sidebar.

![](https://files.buildwithfern.com/https://opik.docs.buildwithfern.com/docs/opik/4452de97d7a787b9ebfe09d9bdb901fa4f9129f236441d58d560721ca9c7bfff/img/tracing/multivalue_feedback_scores.png)

Evaluate specific traces or threads that failed or require closer inspection Apply evaluation rules to historical data that wasn’t captured by sampling Test new evaluation rules on selected examples before enabling them for automatic scoring Re-evaluate traces with updated or modified rules

Once a feedback scores has been provided, you can also add a reason to explain why this particular score was provided. This is useful to add additional context to the score.

If multiple team members are annotating the same trace, you can see the annotations of each team member in the UI in the `Feedback scores` section. The average score will be displayed at a trace and trace level.

If you want a more dedicated annotation interface, you can use the [Annotation Queues](https://www.comet.com/docs/opik/evaluation/advanced/annotation_queues) feature.

## Online evaluation

You don’t need to manually annotate each trace to measure the performance of your agents! By using Opik’s [online evaluation feature](https://www.comet.com/docs/opik/production/online-evaluation/rules), you can define LLM as a Judge metrics that will automatically score all, or a subset, of your production traces.

![Online evaluation](https://files.buildwithfern.com/https://opik.docs.buildwithfern.com/docs/opik/53f825a787e649d815d80587c1bb6c41731887809bae722445d12f237f03737f/img/production/online_evaluation.gif)

Online evaluation

## Manual evaluation

While online evaluation automatically scores traces based on sampling rates and enabled rules, manual evaluation gives you complete control over which traces or threads get evaluated and when. This is particularly useful when you want to:

- Evaluate specific traces or threads that failed or require closer inspection
- Apply evaluation rules to historical data that wasn’t captured by sampling
- Test new evaluation rules on selected examples before enabling them for automatic scoring
- Re-evaluate traces with updated or modified rules

### How manual evaluation works

Manual evaluation allows you to apply any existing evaluation rule to selected traces or threads directly from the UI, bypassing sampling rates and rule enablement status. You can trigger manual evaluation from:

1. **Traces page**: Select one or more traces and click “Evaluate” to apply trace-level rules
2. **Threads page**: Select one or more threads and click “Evaluate” to apply thread-level rules

**Important**: Trace-level rules can only be applied to traces, and thread-level rules can only be applied to threads. Make sure you’re using the appropriate rule type for your selected entities.

When you trigger manual evaluation:

- All selected traces/threads will be queued for evaluation, regardless of sampling rate
- You can apply multiple rules at once
- Rules will execute even if they are currently disabled
- Evaluation results will appear as feedback scores on the evaluated traces/threads
- The evaluation is processed asynchronously, so you may need to wait a few seconds or refresh the page to see the results

This gives you the flexibility to evaluate exactly what you need, when you need it, without waiting for the next sampled trace or modifying your online evaluation configuration.

## Next steps

You can go one step further and:

1. [Create an offline evaluation](https://www.comet.com/docs/opik/v1/evaluation/evaluate_prompt) to evaluate your agent before it is deployed to production
2. [Score your agent in production](https://www.comet.com/docs/opik/production/online-evaluation/rules) to track and catch specific issues with your agent
3. [Use annotation queues](https://www.comet.com/docs/opik/evaluation/advanced/annotation_queues) to organize your traces for review and labeling by your team of experts
4. [Checkout our LLM as a Judge metrics](https://www.comet.com/docs/opik/evaluation/metrics/overview)