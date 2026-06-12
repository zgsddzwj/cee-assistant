from typing import Dict, List, Optional, Any
from models.schemas import Message


class AgentMemoryStore:
    """Agent 记忆存储 - 管理对话历史和考生信息"""

    def __init__(self):
        self.data: Dict[str, Any] = {
            "messages": [],
            "student_score": None,
            "student_rank": None,
            "student_province": None,
            "interests": [],
            "recommended_colleges": [],
            "conversation_summary": ""
        }

    def get(self, key: str) -> Any:
        """获取记忆项"""
        return self.data.get(key)

    def set(self, key: str, value: Any):
        """设置记忆项"""
        self.data[key] = value

    def add_message(self, role: str, content: str):
        """添加对话消息"""
        message = Message(role=role, content=content)
        self.data["messages"].append(message)

    def get_messages(self) -> List[Message]:
        """获取所有对话消息"""
        return self.data["messages"]

    def update_student_info(self, score: Optional[float] = None,
                           rank: Optional[int] = None,
                           province: Optional[str] = None):
        """更新考生信息"""
        if score is not None:
            self.data["student_score"] = score
        if rank is not None:
            self.data["student_rank"] = rank
        if province is not None:
            self.data["student_province"] = province

    def add_recommended_college(self, college_name: str):
        """添加已推荐的院校"""
        if college_name not in self.data["recommended_colleges"]:
            self.data["recommended_colleges"].append(college_name)

    def summary(self) -> str:
        """生成记忆摘要"""
        parts = []
        if self.data["student_score"]:
            parts.append(f"分数: {self.data['student_score']}")
        if self.data["student_rank"]:
            parts.append(f"位次: {self.data['student_rank']}")
        if self.data["student_province"]:
            parts.append(f"省份: {self.data['student_province']}")
        if self.data["interests"]:
            parts.append(f"兴趣: {', '.join(self.data['interests'])}")

        return "; ".join(parts) if parts else "暂无考生信息"
