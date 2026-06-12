from agent.memory import AgentMemoryStore
from models.schemas import Message


def test_memory_stores_student_info():
    memory = AgentMemoryStore()
    memory.update_student_info(score=600, rank=15000, province="北京")

    assert memory.get("student_score") == 600
    assert memory.get("student_rank") == 15000
    assert memory.get("student_province") == "北京"


def test_memory_adds_messages():
    memory = AgentMemoryStore()
    memory.add_message("user", "你好")
    memory.add_message("assistant", "你好！有什么可以帮你的？")

    messages = memory.get_messages()
    assert len(messages) == 2
    assert messages[0].role == "user"
    assert messages[0].content == "你好"


def test_memory_tracks_recommended_colleges():
    memory = AgentMemoryStore()
    memory.add_recommended_college("清华大学")
    memory.add_recommended_college("北京大学")
    memory.add_recommended_college("清华大学")  # 重复添加

    colleges = memory.get("recommended_colleges")
    assert len(colleges) == 2
    assert "清华大学" in colleges
    assert "北京大学" in colleges


def test_memory_summary_with_info():
    memory = AgentMemoryStore()
    memory.update_student_info(score=600, rank=15000, province="北京")
    memory.set("interests", ["计算机", "人工智能"])

    summary = memory.summary()
    assert "分数: 600" in summary
    assert "位次: 15000" in summary
    assert "省份: 北京" in summary
    assert "兴趣: 计算机, 人工智能" in summary


def test_memory_summary_empty():
    memory = AgentMemoryStore()
    assert memory.summary() == "暂无考生信息"
