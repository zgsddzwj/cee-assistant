from agent.intent_classifier import IntentClassifier
from models.schemas import IntentType


def test_intent_classifier_recognizes_score_query():
    classifier = IntentClassifier()
    intent = classifier.classify("我考了600分能上什么学校？")
    assert intent == IntentType.QUERY_SCORE


def test_intent_classifier_recognizes_recommendation():
    classifier = IntentClassifier()
    intent = classifier.classify("给我推荐几个学校")
    assert intent == IntentType.RECOMMENDATION


def test_intent_classifier_recognizes_comparison():
    classifier = IntentClassifier()
    intent = classifier.classify("清华和北大哪个好")
    assert intent == IntentType.COMPARISON


def test_intent_classifier_recognizes_greeting():
    classifier = IntentClassifier()
    intent = classifier.classify("你好")
    assert intent == IntentType.GENERAL_CHAT


def test_intent_classifier_defaults_to_chat():
    classifier = IntentClassifier()
    intent = classifier.classify("abcdefg")
    assert intent == IntentType.GENERAL_CHAT


def test_requires_tool():
    classifier = IntentClassifier()
    assert classifier.requires_tool(IntentType.QUERY_SCORE) is True
    assert classifier.requires_tool(IntentType.RECOMMENDATION) is True
    assert classifier.requires_tool(IntentType.GENERAL_CHAT) is False
