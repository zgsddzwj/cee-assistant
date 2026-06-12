from typing import Optional
from models.schemas import IntentType


class DialogueManager:
    """对话管理器 - 管理对话状态和阶段转换"""

    STAGES = ["greeting", "info_collection", "clarification",
              "recommendation", "explanation", "comparison", "confirmation"]

    # 意图到阶段的映射
    INTENT_STAGE_MAP = {
        IntentType.QUERY_SCORE: "info_collection",
        IntentType.QUERY_MAJOR: "recommendation",
        IntentType.QUERY_COLLEGE: "recommendation",
        IntentType.CAREER_PLANNING: "info_collection",
        IntentType.POLICY_QUESTION: "explanation",
        IntentType.RECOMMENDATION: "recommendation",
        IntentType.COMPARISON: "comparison",
        IntentType.GENERAL_CHAT: "greeting"
    }

    def __init__(self):
        self.current_stage = "greeting"
        self.stage_history = ["greeting"]

    def transition(self, intent: IntentType) -> str:
        """根据意图转换对话阶段"""
        target_stage = self.INTENT_STAGE_MAP.get(intent, self.current_stage)

        # 阶段转换逻辑
        if target_stage != self.current_stage:
            self.current_stage = target_stage
            self.stage_history.append(target_stage)

        return self.current_stage

    def get_stage(self) -> str:
        """获取当前阶段"""
        return self.current_stage

    def is_info_complete(self) -> bool:
        """检查信息是否收集完整"""
        # TODO: 实现信息完整性检查
        return True

    def needs_clarification(self) -> bool:
        """判断是否需要澄清"""
        # TODO: 实现澄清判断逻辑
        return False
