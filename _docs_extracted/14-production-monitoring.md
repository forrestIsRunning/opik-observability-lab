Opik has been designed from the ground up to support high volumes of traces making it the ideal tool for monitoring your production LLM applications.

You can use the **Insights** tab within any project to review your feedback scores, trace count, latency, and cost over time. The built-in Project Overview provides an at-a-glance health check with stats cards and time-series charts. For more details, see [Dashboards](https://www.comet.com/docs/opik/tracing/dashboards/dashboards).

![Project Overview — built-in Insights view](https://files.buildwithfern.com/https://opik.docs.buildwithfern.com/docs/opik/2a6055a34bc79060b1f9b03b4b466cec5519f51ce07efa9b07cf009416f6e6cf/img/production/dashboard_example.png)

Project Overview — built-in Insights view

In addition to viewing scores over time, you can also view the average feedback scores for all the traces in your project from the traces table.

## Logging feedback scores

To monitor the performance of your LLM application, you can log feedback scores using the [Python SDK and through the UI](https://www.comet.com/docs/opik/tracing/advanced/annotate_traces).

### Defining online evaluation metrics

You can define LLM as a Judge metrics in the Opik platform that will automatically score all, or a subset, of your production traces. You can find more information about how to define LLM as a Judge metrics in the [Online evaluation](https://www.comet.com/docs/opik/production/online-evaluation/rules) section.

Once a rule is defined, Opik will score all the traces in the project and allow you to track these feedback scores over time.

In addition to allowing you to define LLM as a Judge metrics, Opik will soon allow you to define Python metrics to give you even more control over the feedback scores.

### Manually logging feedback scores alongside traces

Feedback scores can be logged while you are logging traces:

```python
1from opik import track, opik_context
2
3@track
4def llm_chain(input_text):
5    # LLM chain code
6    # ...
7
8    # Update the trace
9    opik_context.update_current_trace(
10        feedback_scores=[
11            {"name": "user_feedback", "value": 1.0, "reason": "The response was helpful and accurate."}
12        ]
13    )
```

### Updating traces with feedback scores

You can also update traces with feedback scores after they have been logged. For this we are first going to fetch all the traces using the search API and then update the feedback scores for the traces we want to annotate.

#### Fetching traces using the search API

You can use the [`Opik.search_traces`](https://www.comet.com/docs/opik/python-sdk-reference/Opik.html#opik.Opik.search_traces) method to fetch all the traces you want to annotate.

```python
1import opik
2
3opik_client = opik.Opik()
4
5traces = opik_client.search_traces(
6    project_name="Default Project"
7)
```

The `search_traces` method allows you to fetch traces based on any of trace attributes, you can learn more about the different search parameters in the [search traces documentation](https://www.comet.com/docs/opik/v1/tracing/export_data).

#### Updating feedback scores

Once you have fetched the traces you want to annotate, you can update the feedback scores using the [`Opik.log_traces_feedback_scores`](https://www.comet.com/docs/opik/python-sdk-reference/Opik.html#opik.Opik.log_traces_feedback_scores) method.

```python
1for trace in traces:
2    opik_client.log_traces_feedback_scores(
3        scores=[
4            {
5                "id": trace.id,
6                "name": "user_feedback",
7                "value": 1.0,
8                "reason": "The response was helpful and accurate.",
9                "project_name": "Default Project"
10            }
11        ],
12    )
```

You will now be able to see the feedback scores in the Opik dashboard and track the changes over time.

### Updating trace content

#### Get trace content

You can view the content of your traces using [`Opik.get_trace_content(id: str)`](https://www.comet.com/docs/opik/python-sdk-reference/Opik.html#opik.Opik.get_trace_content), to look up your trace by id. Trace ids can be found using the [`Opik.search_traces()`](https://www.comet.com/docs/opik/python-sdk-reference/Opik.html#opik.Opik.search_traces) method or by looking at the ID column within the Projects > ‘My-project’ view.

```python
1from opik import Opik
2
3TRACE_ID = 'EXAMPLE-ID' # UUIDv7 Identifier
4
5opik_client = Opik()
6trace_content = opik_client.get_trace_content(id = TRACE_ID)
```

This will return a [`TracePublic`](https://www.comet.com/docs/opik/python-sdk-reference/Objects/TracePublic.html#opik.rest_api.types.trace_public.TracePublic) object, a pydantic model object with all the data associated with the trace found.

#### Update trace by ID

You can update a given trace by first re-instantiating the trace using [`opik.Opik.trace()`](https://www.comet.com/docs/opik/python-sdk-reference/Opik.html#opik.Opik.trace) and then updating any one of the trace attributes using [`Trace.update()`](https://www.comet.com/docs/opik/python-sdk-reference/Objects/Trace.html#opik.api_objects.trace.Trace.update). See above section for guidance on how to retrieve trace ids.

```python
1from opik import Opik
2
3TRACE_ID = 'EXAMPLE-ID' # UUIDv7 Identifier
4
5opik_client = Opik()
6trace = opik_client.trace(id = TRACE_ID)
7trace.update(output = updated_output)
```

The trace attributes that can be used as parameters are as follows:

- end\_time: The end time of the trace.
- metadata: Additional metadata to be associated with the trace.
- input: The input data for the trace.
- output: The output data for the trace.
- tags: A list of tags to be associated with the trace.
- error\_info: The dictionary with error information (typically used when the trace function has failed).
- thread\_id: Used to group multiple traces into a thread. The identifier is user-defined and has to be unique per project.