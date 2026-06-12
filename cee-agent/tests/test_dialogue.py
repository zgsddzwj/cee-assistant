from agent.dialogue_manager import DialogueManager
from models.schemas import IntentType


def test_dialogue_manager_initial_stage():
    dm = DialogueManager()
    assert dm.current_stage == "greeting"
    assert dm.get_stage() == "greeting"


def test_dialogue_manager_transitions():
    dm = DialogueManager()
    assert dm.current_stage == "greeting"

    dm.transition(IntentType.QUERY_SCORE)
    assert dm.current_stage == "info_collection"

    dm.transition(IntentType.RECOMMENDATION)
    assert dm.current_stage == "recommendation"

    dm.transition(IntentType.COMPARISON)
    assert dm.current_stage == "comparison"


def test_dialogue_manager_stage_history():
    dm = DialogueManager()
    dm.transition(IntentType.QUERY_SCORE)
    dm.transition(IntentType.RECOMMENDATION)

    assert dm.stage_history == ["greeting", "info_collection", "recommendation"]


def test_dialogue_manager_no_redundant_transitions():
    dm = DialogueManager()
    dm.transition(IntentType.GENERAL_CHAT)

    # GENERAL_CHAT 映射到 greeting，与初始阶段相同，不应重复添加
    assert dm.stage_history == ["greeting"]


def test_dialogue_manager_policy_question():
    dm = DialogueManager()
    dm.transition(IntentType.POLICY_QUESTION)
    assert dm.current_stage == "explanation"
