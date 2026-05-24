When working with Opik, it is important to be able to export traces, spans, and threads so that you can use them to fine-tune your models or run deeper analysis.

You can export the data you have logged to the Opik platform using:

1. Using the Opik SDK: You can use the Python SDK methods ([`Opik.search_traces`](https://www.comet.com/docs/opik/python-sdk-reference/Opik.html#opik.Opik.search_traces), [`Opik.search_spans`](https://www.comet.com/docs/opik/python-sdk-reference/Opik.html#opik.Opik.search_spans), and [`Opik.search_threads`](https://www.comet.com/docs/opik/python-sdk-reference/Opik.html#opik.Opik.search_threads)) or the TypeScript SDK method (`client.searchTraces()`) to export traces, spans, and threads.
2. Using the Opik REST API: You can use the [`/traces`](https://www.comet.com/docs/opik/v1/reference/rest-api/traces/get-traces-by-project) and [`/spans`](https://www.comet.com/docs/opik/v1/reference/rest-api/spans/get-spans-by-project) endpoints to export traces and spans.
3. Using the UI: Once you have selected the traces or spans you want to export, you can click on the `Export CSV` button in the `Actions` dropdown.

## Using the Opik SDK

### Exporting traces

The Python SDK [`Opik.search_traces`](https://www.comet.com/docs/opik/python-sdk-reference/Opik.html#opik.Opik.search_traces) method and TypeScript SDK `client.searchTraces()` method allow you to both export all the traces in a project or search for specific traces and export them.

#### Exporting all traces

To export all traces, you will need to specify a `max_results` / `maxResults` value that is higher than the total number of traces in your project:

###### Python

###### TypeScript

```python
1import opik
2
3client = opik.Opik()
4
5traces = client.search_traces(project_name="Default project", max_results=1000000)
```

#### Search for specific traces

You can use the `filter_string` (Python) / `filterString` (TypeScript) parameter to search for specific traces:

###### Python

###### TypeScript

```python
1import opik
2
3client = opik.Opik()
4
5traces = client.search_traces(
6  project_name="Default project",
7  filter_string='input contains "Opik"'
8)
9
10# Convert to Dict if required
11traces = [trace.dict() for trace in traces]
```

### Filtering with Opik Query Language (OQL)

All search methods (`search_traces`, `search_spans`, and `search_threads`) accept a `filter_string` (Python) / `filterString` (TypeScript) parameter that uses Opik Query Language (OQL):

```
"<COLUMN> <OPERATOR> <VALUE> [AND <COLUMN> <OPERATOR> <VALUE>]*"
```

**Rules:**

- String values must be wrapped in double quotes
- Multiple conditions can be combined with `AND` (OR is not supported)
- DateTime fields require ISO 8601 format (e.g., `"2024-01-01T00:00:00Z"`)
- Use dot notation for nested fields: `metadata.model`, `feedback_scores.accuracy`

Each entity type supports a different set of filter columns. The tables below list the available columns for each.

#### Trace columns

| Column | Type | Operators |
| --- | --- | --- |
| `id` | String | `=`, `!=`, `contains`, `not_contains`, `starts_with`, `ends_with`, `>`, `<` |
| `name` | String | `=`, `!=`, `contains`, `not_contains`, `starts_with`, `ends_with`, `>`, `<` |
| `input`, `output` | String | `=`, `!=`, `contains`, `not_contains`, `starts_with`, `ends_with`, `>`, `<` |
| `thread_id` | String | `=`, `!=`, `contains`, `not_contains`, `starts_with`, `ends_with`, `>`, `<` |
| `guardrails` | String | `=`, `!=`, `contains`, `not_contains`, `starts_with`, `ends_with`, `>`, `<` |
| `experiment_id` | String | `=`, `!=`, `contains`, `not_contains`, `starts_with`, `ends_with`, `>`, `<` |
| `start_time`, `end_time` | DateTime | `=`, `!=`, `>`, `>=`, `<`, `<=` |
| `created_at`, `last_updated_at` | DateTime | `=`, `!=`, `>`, `>=`, `<`, `<=` |
| `metadata` | Dictionary | `=`, `!=`, `contains`, `not_contains`, `starts_with`, `ends_with`, `>`, `>=`, `<`, `<=` |
| `input_json`, `output_json` | Dictionary | `=`, `!=`, `contains`, `not_contains`, `starts_with`, `ends_with`, `>`, `>=`, `<`, `<=` |
| `feedback_scores` | Numeric | `=`, `!=`, `>`, `>=`, `<`, `<=`, `is_empty`, `is_not_empty` |
| `span_feedback_scores` | Numeric | `=`, `!=`, `>`, `>=`, `<`, `<=`, `is_empty`, `is_not_empty` |
| `tags` | List | `=`, `!=`, `contains`, `not_contains`, `is_empty`, `is_not_empty` |
| `annotation_queue_ids` | List | `=`, `!=`, `contains`, `not_contains`, `is_empty`, `is_not_empty` |
| `usage.total_tokens`, `usage.prompt_tokens`, `usage.completion_tokens` | Numeric | `=`, `!=`, `>`, `>=`, `<`, `<=` |
| `duration`, `total_estimated_cost`, `llm_span_count` | Numeric | `=`, `!=`, `>`, `>=`, `<`, `<=` |
| `error_info` | Container | `is_empty`, `is_not_empty` |

#### Span columns

| Column | Type | Operators |
| --- | --- | --- |
| `id` | String | `=`, `!=`, `contains`, `not_contains`, `starts_with`, `ends_with`, `>`, `<` |
| `name` | String | `=`, `!=`, `contains`, `not_contains`, `starts_with`, `ends_with`, `>`, `<` |
| `input`, `output` | String | `=`, `!=`, `contains`, `not_contains`, `starts_with`, `ends_with`, `>`, `<` |
| `model` | String | `=`, `!=`, `contains`, `not_contains`, `starts_with`, `ends_with`, `>`, `<` |
| `provider` | String | `=`, `!=`, `contains`, `not_contains`, `starts_with`, `ends_with`, `>`, `<` |
| `trace_id` | String | `=`, `!=`, `contains`, `not_contains`, `starts_with`, `ends_with`, `>`, `<` |
| `type` | Enum | `=`, `!=` |
| `start_time`, `end_time` | DateTime | `=`, `!=`, `>`, `>=`, `<`, `<=` |
| `metadata` | Dictionary | `=`, `!=`, `contains`, `not_contains`, `starts_with`, `ends_with`, `>`, `>=`, `<`, `<=` |
| `input_json`, `output_json` | Dictionary | `=`, `!=`, `contains`, `not_contains`, `starts_with`, `ends_with`, `>`, `>=`, `<`, `<=` |
| `feedback_scores` | Numeric | `=`, `!=`, `>`, `>=`, `<`, `<=`, `is_empty`, `is_not_empty` |
| `tags` | List | `=`, `!=`, `contains`, `not_contains`, `is_empty`, `is_not_empty` |
| `usage.total_tokens`, `usage.prompt_tokens`, `usage.completion_tokens` | Numeric | `=`, `!=`, `>`, `>=`, `<`, `<=` |
| `duration`, `total_estimated_cost` | Numeric | `=`, `!=`, `>`, `>=`, `<`, `<=` |
| `error_info` | Container | `is_empty`, `is_not_empty` |

#### Thread columns

| Column | Type | Operators |
| --- | --- | --- |
| `id` | String | `=`, `!=`, `contains`, `not_contains`, `starts_with`, `ends_with`, `>`, `<` |
| `first_message`, `last_message` | String | `=`, `!=`, `contains`, `not_contains`, `starts_with`, `ends_with`, `>`, `<` |
| `status` | Enum | `=`, `!=` |
| `start_time`, `end_time` | DateTime | `=`, `!=`, `>`, `>=`, `<`, `<=` |
| `created_at`, `last_updated_at` | DateTime | `=`, `!=`, `>`, `>=`, `<`, `<=` |
| `feedback_scores` | Numeric | `=`, `!=`, `>`, `>=`, `<`, `<=`, `is_empty`, `is_not_empty` |
| `tags` | List | `=`, `!=`, `contains`, `not_contains`, `is_empty`, `is_not_empty` |
| `annotation_queue_ids` | List | `=`, `!=`, `contains`, `not_contains`, `is_empty`, `is_not_empty` |
| `duration`, `number_of_messages` | Numeric | `=`, `!=`, `>`, `>=`, `<`, `<=` |

###### Python

###### TypeScript

```python
1import opik
2
3client = opik.Opik(project_name="Default project")
4
5# Trace filters
6traces = client.search_traces(filter_string='input contains "Opik"')
7traces = client.search_traces(filter_string='start_time >= "2024-01-01T00:00:00Z"')
8traces = client.search_traces(filter_string='usage.total_tokens > 1000')
9traces = client.search_traces(filter_string='metadata.model = "gpt-4o"')
10traces = client.search_traces(filter_string='feedback_scores.user_rating is_not_empty')
11traces = client.search_traces(filter_string='tags contains "production"')
12
13# Thread filters
14threads = client.search_threads(filter_string='number_of_messages >= 5')
15threads = client.search_threads(filter_string='first_message contains "hello"')
16threads = client.search_threads(filter_string='status = "active"')
```

If your `feedback_scores` key contains spaces, you will need to wrap it in double quotes:

`'feedback_scores."My Score" > 0'`

If the `feedback_scores` key contains both spaces and double quotes, you will need to escape the double quotes as `""`:

`'feedback_scores."Score ""with"" Quotes" > 0'`

or by using different quotes, surrounding in triple-quotes, like this:

`'''feedback_scores.'Accuracy "Happy Index"' < 0.8'''`

### Exporting spans

You can export spans using the [`Opik.search_spans`](https://www.comet.com/docs/opik/python-sdk-reference/Opik.html#opik.Opik.search_spans) method. This method allows you to search for spans based on `trace_id` or based on a filter string.

#### Exporting spans based on trace\_id

To export all the spans associated with a specific trace, you can use the `trace_id` parameter:

```python
1import opik
2
3client = opik.Opik()
4
5spans = client.search_spans(
6  project_name="Default project",
7  trace_id="067092dc-e639-73ff-8000-e1c40172450f"
8)
```

#### Search for specific spans

You can use the `filter_string` parameter to search for specific spans:

```python
1import opik
2
3client = opik.Opik()
4
5spans = client.search_spans(
6  project_name="Default project",
7  filter_string='input contains "Opik"'
8)
```

### Exporting threads

You can export threads using the [`Opik.search_threads`](https://www.comet.com/docs/opik/python-sdk-reference/Opik.html#opik.Opik.search_threads) method. This method allows you to search for conversational threads in a project.

#### Exporting all threads

To export all threads, you will need to specify a `max_results` value that is higher than the total number of threads in your project:

```python
1import opik
2
3client = opik.Opik()
4
5threads = client.search_threads(project_name="Default project", max_results=1000000)
```

#### Search for specific threads

You can use the `filter_string` parameter to search for specific threads:

```python
1import opik
2
3client = opik.Opik()
4
5# Search for a specific thread by ID
6threads = client.search_threads(
7  project_name="Default project",
8  filter_string='id = "thread_123"'
9)
10
11# Search for threads with many messages
12threads = client.search_threads(
13  project_name="Default project",
14  filter_string='number_of_messages >= 5'
15)
16
17# Search for threads with a specific feedback score
18threads = client.search_threads(
19  project_name="Default project",
20  filter_string='feedback_scores.user_satisfaction > 0.8'
21)
22
23# Search for threads by tag
24threads = client.search_threads(
25  project_name="Default project",
26  filter_string='tags contains "important"'
27)
```

## Using the Opik REST API

To export traces using the Opik REST API, you can use the [`/traces`](https://www.comet.com/docs/opik/v1/reference/rest-api/traces/get-traces-by-project) endpoint and the [`/spans`](https://www.comet.com/docs/opik/v1/reference/rest-api/spans/get-spans-by-project) endpoint. These endpoints are paginated so you will need to make multiple requests to retrieve all the traces or spans you want.

To search for specific traces or spans, you can use the `filter` parameter. While this is a string parameter, it does not follow the same format as the `filter_string` parameter in the Opik SDK. Instead it is a list of json objects with the following format:

```json
1[
2  {
3    "field": "name",
4    "type": "string",
5    "operator": "=",
6    "value": "Opik"
7  }
8]
```

The `filter` parameter was designed to be used with the Opik UI and has therefore limited flexibility. If you need more flexibility, please raise an issue on [GitHub](https://github.com/comet-ml/opik/issues) so we can help.

## Using the UI

To export traces as a CSV file from the UI, you can simply select the traces or spans you wish to export and click on `Export CSV` in the `Actions` dropdown:

![](https://files.buildwithfern.com/https://opik.docs.buildwithfern.com/docs/opik/883d4ca5d95c63f301c199eaea8131207eee82f9d1a50c90545bec035acac5c7/img/tracing/download_traces.png)

String values must be wrapped in double quotes Multiple conditions can be combined with AND (OR is not supported) DateTime fields require ISO 8601 format (e.g., "2024-01-01T00:00:00Z" ) Use dot notation for nested fields: metadata.model, feedback\_scores.accuracy

The UI only allows you to export up to 100 traces or spans at a time as it is linked to the page size of the traces table. If you need to export more traces or spans, we recommend using the Opik SDK.