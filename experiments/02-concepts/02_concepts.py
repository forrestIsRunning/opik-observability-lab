"""
实验 02: Opik 核心概念深度演示
================================
演示 Trace、Span、Project、Feedback Score、Dataset、Prompt 等核心概念。

运行方式:
    uv run python experiments/02-concepts/02_concepts.py
"""

import opik


def demonstrate_trace_span_relationship():
    """Trace-Span 关系: 1 Trace : N Spans (树形结构)"""
    print("=" * 60)
    print("[实验 2.1] Trace-Span 关系")
    print("=" * 60)

    client = opik.Opik(project_name="opik-ob-experiment-02", host="http://localhost:5173/api", workspace="default")

    trace = client.trace(name="concept_demo", input={"demo": "trace_span_relationship"})

    # Span 可以嵌套任意层
    span_a = trace.span(name="step_A", type="tool", input={"step": "A"})
    span_a_1 = span_a.span(name="step_A_1", type="general", input={"step": "A1"})
    span_a_1.end(output={"result": "A1 done"})
    span_a_2 = span_a.span(name="step_A_2", type="general", input={"step": "A2"})
    span_a_2.end(output={"result": "A2 done"})
    span_a.end(output={"result": "A done"})

    span_b = trace.span(name="step_B", type="llm", input={"step": "B"}, model="gpt-4", provider=opik.LLMProvider.OPENAI)
    span_b.end(output={"result": "B done"}, usage={"total_tokens": 50})

    trace.end(output={"result": "all done"})

    print("  Trace → Span A → Span A1, Span A2")
    print("       → Span B")
    print("  树形结构已记录到 Opik 后端")

    client.end()


def demonstrate_span_types():
    """四种 Span 类型及其用途"""
    print("=" * 60)
    print("[实验 2.2] Span 类型")
    print("=" * 60)

    client = opik.Opik(project_name="opik-ob-experiment-02", host="http://localhost:5173/api", workspace="default")
    trace = client.trace(name="span_types_demo", input={"demo": "span_types"})

    # general: 通用步骤
    s1 = trace.span(name="parse_input", type="general", input={"raw": "user input"})
    s1.end(output={"parsed": "structured"})

    # llm: LLM 调用
    s2 = trace.span(name="llm_reasoning", type="llm", input={"prompt": "think step by step"},
                     model="gpt-4", provider=opik.LLMProvider.OPENAI)
    s2.end(output={"reasoning": "..."}, usage={"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30})

    # tool: 工具调用（检索、API、计算等）
    s3 = trace.span(name="search_knowledge_base", type="tool", input={"query": "question"})
    s3.end(output={"docs": ["doc1", "doc2"]})

    # guardrail: 安全/内容过滤
    s4 = trace.span(name="content_safety_check", type="guardrail", input={"text": "generated output"})
    s4.end(output={"passed": True, "risk_score": 0.02})

    trace.end(output={"summary": "all span types demonstrated"})
    print("  4 种 Span 类型: general, llm, tool, guardrail")
    client.end()


if __name__ == "__main__":
    demonstrate_trace_span_relationship()
    demonstrate_span_types()