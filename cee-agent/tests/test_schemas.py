from models.schemas import IntentType, Message, DialogContext, AgentMemory


def test_intent_enum_values():
    assert IntentType.QUERY_SCORE == "query_score"
    assert IntentType.RECOMMENDATION == "recommendation"
    assert IntentType.GENERAL_CHAT == "general_chat"


def test_message_creation():
    msg = Message(role="user", content="你好")
    assert msg.role == "user"
    assert msg.content == "你好"


def test_dialog_context_summary():
    ctx = DialogContext()
    assert ctx.summary() == "对话轮数: 0, 当前阶段: greeting"

    ctx.messages.append(Message(role="user", content="你好"))
    assert ctx.summary() == "对话轮数: 1, 当前阶段: greeting"


def test_agent_memory_defaults():
    mem = AgentMemory()
    assert mem.student_score is None
    assert mem.student_rank is None
    assert mem.interests == []
