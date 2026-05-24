You can log chat conversations to the Opik platform and track the full conversations your users are having with your chatbot. Threads allow you to group related traces together, creating a conversational flow that makes it easy to review multi-turn interactions and track user sessions.

![](https://files.buildwithfern.com/https://opik.docs.buildwithfern.com/docs/opik/32f258642be47e6b0718234014a8c52cee55eebe92a074f7b901f268c4f0bc90/img/tracing/chat_conversations.png)

Multi-turn conversations: Track complete chat sessions between users and AI assistants User sessions: Group all interactions from a single user session Conversational agents: Follow the flow of agent interactions and tool usage Workflow tracking: Monitor complex workflows that span multiple function calls

## Understanding Threads

Threads in Opik are collections of traces that are grouped together using a unique `thread_id`. This is particularly useful for:

- **Multi-turn conversations**: Track complete chat sessions between users and AI assistants
- **User sessions**: Group all interactions from a single user session
- **Conversational agents**: Follow the flow of agent interactions and tool usage
- **Workflow tracking**: Monitor complex workflows that span multiple function calls

The `thread_id` is a user-defined identifier that must be unique per project. All traces with the same `thread_id` will be grouped together and displayed as a single conversation thread in the Opik UI.

## Logging conversations

You can log chat conversations by specifying the `thread_id` parameter when using either the low level SDK, Python decorators, or integration libraries:

```
1import { Opik } from "opik";
2
3const client = new Opik({
4apiUrl: "https://www.comet.com/opik/api", // Only required if you are using Opik Cloud
5apiKey: "your-api-key",
6projectName: "your-project-name",
7workspaceName: "your-workspace-name", // Optional
8});
9
10const threadId = "your-thread-id"; // any unique string per conversation
11
12// Option A: set on trace creation
13const trace = client.trace({
14    name: "chat turn",
15    input: { user: "Hi there" },
16    output: { assistant: "Hello!" },
17    threadId
18});
```

The input to each trace will be displayed as the user message while the output will be displayed as the AI assistant response.

## Thread ID Best Practices

### Generating Thread IDs

Choose a thread ID strategy that fits your application:

```
1import uuid
2import opik
3
4# Generate unique thread ID per user session
5user_id = "user_12345"
6session_start_time = "2024-01-15T10:30:00Z"
7thread_id = f"{user_id}-{session_start_time}"
8
9@opik.track
10def process_user_message(message, user_id):
11    return "Response to: " + message
12
13process_user_message("What is Opik ?", opik_args={"trace": {"thread_id": thread_id}})
```

### Integration-Specific Threading

Different integrations handle thread IDs in various ways:

```
1from opik.integrations.langchain import OpikTracer
2
3# Set thread_id at tracer level - applies to all traces
4opik_tracer = OpikTracer(
5    project_name="my-chatbot",
6    thread_id="conversation-123"
7)
8
9# Or pass dynamically via metadata
10chain.invoke(
11    {"input": "Hello"},
12    config={
13        "callbacks": [opik_tracer],
14        "metadata": {"thread_id": "dynamic-conversation-456"}
15    }
16)
```

## Reviewing conversations

Conversations can be viewed at a project level in the `threads` tab. All conversations are tracked and by clicking on the thread ID you will be able to view the full conversation.

The thread view supports markdown making it easier for you to review the content that was returned to the user. If you would like to dig in deeper, you can click on the `View trace` button to deepdive into how the AI assistant response was generated.

By clicking on the thumbs up or thumbs down icons, you can quickly rate the AI assistant response. This feedback score will be logged and associated to the relevant trace. By switching to the trace view, you can review the full trace as well as add additional feedback scores through the annotation functionality.

![](https://files.buildwithfern.com/https://opik.docs.buildwithfern.com/docs/opik/e8fb41c6f4b98b6dc14981e793d9b1d2a4e7da2dc96d03deb18cc21ebf4a567f/img/tracing/chat_conversations_actions.png)

Multi-turn conversations: Track complete chat sessions between users and AI assistants User sessions: Group all interactions from a single user session Conversational agents: Follow the flow of agent interactions and tool usage Workflow tracking: Monitor complex workflows that span multiple function calls

## Scoring conversations

You can assign conversation-level feedback scores to threads at any time. Threads are aggregated traces that are created when tracking agents or simply traces interconnected by a `thread_id`.

![](https://files.buildwithfern.com/https://opik.docs.buildwithfern.com/docs/opik/f888ac8e11aa5549a0d0c005ec15ee02b08047e0c4a95e0a14b16fea22fa958a/img/tracing/chat_conversations_score.png)

Multi-turn conversations: Track complete chat sessions between users and AI assistants User sessions: Group all interactions from a single user session Conversational agents: Follow the flow of agent interactions and tool usage Workflow tracking: Monitor complex workflows that span multiple function calls

In the conversation list, you can see the feedback scores associated to each thread.

![](https://files.buildwithfern.com/https://opik.docs.buildwithfern.com/docs/opik/37f5f3cd0a277951e2b18a6f732f41de9b43189b3db1087ac5d05fca277b225b/img/tracing/chat_conversations_score_list.png)

Multi-turn conversations: Track complete chat sessions between users and AI assistants User sessions: Group all interactions from a single user session Conversational agents: Follow the flow of agent interactions and tool usage Workflow tracking: Monitor complex workflows that span multiple function calls

You can also tag a thread and add comments to it. This is useful to add additional context during the review process or investigate a specific conversation.

![](https://files.buildwithfern.com/https://opik.docs.buildwithfern.com/docs/opik/174a133be6060b0c75b78f45b50a581613c5a1ba98a12c6ae771a750e24febb1/img/tracing/chat_conversation_tags_comments.png)

Multi-turn conversations: Track complete chat sessions between users and AI assistants User sessions: Group all interactions from a single user session Conversational agents: Follow the flow of agent interactions and tool usage Workflow tracking: Monitor complex workflows that span multiple function calls

### Thread Online Scoring Rule Cooldown Period

For thread-level online evaluation rules (automatic scoring), Opik waits for a “cooldown period” after the last activity in a thread before running the rules. This gives conversations time to settle before automatic evaluation.

By default, the cooldown period is 15 minutes. You can change this value by setting the `OPIK_TRACE_THREAD_TIMEOUT_TO_MARK_AS_INACTIVE` environment variable (if you are using the Opik self-hosted version). On cloud, you can change this setting at workspace level under “Thread online scoring rule cooldown period”.

#### Behavior When Adding Traces to Existing Threads

When a new trace is added to an existing thread, the following happens:

- **Existing feedback scores are preserved**: Any manual feedback scores or online evaluation scores you have added remain intact.
- **The cooldown timer restarts**: The timer resets from the moment the new trace is added, ensuring online evaluation waits for the full cooldown period before scoring the updated thread.
- **Online evaluation re-runs**: Once the cooldown period expires, thread-level online scoring rules will automatically evaluate the complete conversation again. If a new score is logged with the same name as an existing score, the existing score is updated.

## Advanced Thread Features

### Filtering and Searching Threads

You can filter threads using the `thread_id` field in various Opik features:

#### In Data Export

When exporting data, you can filter by `thread_id` using these operators:

- `=` (equals), `!=` (not equals)
- `contains`, `not_contains`
- `starts_with`, `ends_with`
- `>`, `<` (lexicographic comparison)

#### In Thread Evaluation

You can evaluate entire conversation threads using the thread evaluation features. This is particularly useful for:

- Conversation quality assessment
- Multi-turn coherence evaluation
- User satisfaction scoring across complete interactions

### Thread Management

Threads can have traces added to them at any time, and you can add feedback scores, comments, and tags to threads regardless of whether new traces are still being added.

### Programmatic Thread Management

You can also manage threads programmatically using the Opik SDK:

```
1import opik
2
3# Initialize client
4client = opik.Opik()
5
6# Search for threads by various criteria
7threads = client.search_traces(
8    project_name="my-chatbot",
9    filter_string='thread_id contains "user-session"'
10)
11
12# Get specific thread content
13for trace in threads:
14    if trace.thread_id:
15        thread_content = client.get_trace_content(trace.id)
16        print(f"Thread: {trace.thread_id}")
17        print(f"Input: {thread_content.input}")
18        print(f"Output: {thread_content.output}")
19
20# Add feedback scores to thread traces
21for trace in threads:
22    trace.log_feedback_score(
23        name="conversation_quality",
24        value=0.8,
25        reason="Good multi-turn conversation flow"
26    )
```

## Next steps

Once you have added observability to your multi-turn agent, why not:

1. [Run offline multi-turn conversation evaluation](https://www.comet.com/docs/opik/evaluation/evaluate_threads)
2. [Create online evaluation rules](https://www.comet.com/docs/opik/production/online-evaluation/rules) to score your multi-turn conversations in production