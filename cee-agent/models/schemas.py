from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class IntentType(str, Enum):
    """意图类型"""
    QUERY_SCORE = "query_score"
    QUERY_MAJOR = "query_major"
    QUERY_COLLEGE = "query_college"
    CAREER_PLANNING = "career_planning"
    POLICY_QUESTION = "policy_question"
    RECOMMENDATION = "recommendation"
    COMPARISON = "comparison"
    GENERAL_CHAT = "general_chat"


class Message(BaseModel):
    """对话消息"""
    role: str  # "user" | "assistant" | "system"
    content: str
    timestamp: Optional[str] = None


class DialogContext(BaseModel):
    """对话上下文"""
    messages: List[Message] = []
    current_intent: Optional[IntentType] = None
    stage: str = "greeting"  # greeting / info_collection / recommendation / etc.

    def summary(self) -> str:
        """生成对话摘要"""
        return f"对话轮数: {len(self.messages)}, 当前阶段: {self.stage}"


class AgentMemory(BaseModel):
    """Agent 记忆"""
    student_score: Optional[float] = None
    student_rank: Optional[int] = None
    student_province: Optional[str] = None
    interests: List[str] = []
    recommended_colleges: List[str] = []
    conversation_summary: str = ""
