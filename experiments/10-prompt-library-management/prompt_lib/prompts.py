"""Demo prompt definitions — simulating "before migration" hard-coded prompts."""

# ============================================================
# "Before" — hard-coded prompts (the pain point)
# ============================================================

HARD_CODED_SYSTEM_PROMPT = """\
你是一个专业的跨境电商客服助手。请用友好、专业的语气回答客户问题。

回答规则：
1. 如果客户询问订单状态，引导他们提供订单号
2. 如果客户询问退货政策，解释 30 天无理由退货
3. 如果客户投诉产品质量，先道歉再提供解决方案
4. 所有回答需要用中文
"""

HARD_CODED_USER_TEMPLATE = """\
客户问题：{{question}}
历史对话：{{chat_history}}
"""

HARD_CODED_SUMMARY_PROMPT = """\
请用一句话总结以下客服对话：

{{conversation}}
"""

# ============================================================
# V2 — after first iteration
# ============================================================

V2_SYSTEM_PROMPT = """\
你是一个专业的跨境电商客服助手。请用友好、专业的语气回答客户问题。

回答规则：
1. 如果客户询问订单状态，引导他们提供订单号
2. 如果客户询问退货政策，解释 30 天无理由退货（电子产品 15 天）
3. 如果客户投诉产品质量，先道歉再提供解决方案
4. 如果客户表达强烈不满，升级到人工客服处理
5. 所有回答需要用中文

品牌语调：热情、耐心、解决问题导向
"""

# ============================================================
# Metadata helpers
# ============================================================

PROMPT_METADATA = {
    "customer_service_system": {
        "description": "跨境电商客服系统主提示词",
        "owner": "team-ai",
        "tags": ["production", "customer-service"],
    },
    "user_question_template": {
        "description": "用户问题填充模板（Mustache 语法）",
        "type": "template",
        "variables": ["question", "chat_history"],
    },
    "conversation_summarizer": {
        "description": "客服对话总结提示词",
        "owner": "team-product",
        "tags": ["production", "summary"],
    },
}