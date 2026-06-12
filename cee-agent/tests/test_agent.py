from agent.core import GaokaoAgent


def test_agent_processes_greeting():
    agent = GaokaoAgent()
    response = agent.chat("你好，我想咨询志愿填报")

    assert response is not None
    assert len(response) > 0
    assert "高考志愿填报助手" in response


def test_agent_collects_score_info():
    agent = GaokaoAgent()
    agent.chat("你好")
    response = agent.chat("我考了600分，位次15000")

    assert agent.memory.get("student_score") == 600
    assert agent.memory.get("student_rank") == 15000
    assert "收到" in response


def test_agent_recommends_based_on_score():
    agent = GaokaoAgent()
    agent.chat("你好")
    agent.chat("我考了620分，位次8000")
    response = agent.chat("给我推荐几个学校")

    assert "620" in response
    assert "8000" in response
    assert "冲刺" in response
    assert "稳妥" in response
    assert "保底" in response


def test_agent_asks_for_info_before_recommendation():
    agent = GaokaoAgent()
    agent.chat("你好")
    response = agent.chat("给我推荐几个学校")

    assert "分数" in response
    assert "位次" in response


def test_agent_tracks_conversation_history():
    agent = GaokaoAgent()
    agent.chat("你好")
    agent.chat("我考了600分")

    messages = agent.memory.get_messages()
    assert len(messages) == 4  # user + assistant + user + assistant
