from typing import Optional
from models.schemas import IntentType


class IntentClassifier:
    """意图识别器 - 基于规则 + 关键词匹配"""

    # 关键词映射
    KEYWORDS = {
        IntentType.QUERY_SCORE: ["分数", "分", "多少分", "能上", "可以报", "录取线", "考了"],
        IntentType.QUERY_MAJOR: ["专业", "学什么", "怎么样"],
        IntentType.QUERY_COLLEGE: ["学校", "大学", "院校", "如何"],
        IntentType.CAREER_PLANNING: ["职业", "工作", "就业", "未来", "规划"],
        IntentType.POLICY_QUESTION: ["政策", "规则", "怎么填", "平行"],
        IntentType.RECOMMENDATION: ["推荐", "建议", "选什么", "报哪个", "给我"],
        IntentType.COMPARISON: ["对比", "比较", "哪个好", "还是"],
        IntentType.GENERAL_CHAT: ["你好", "谢谢", "紧张", "害怕", "担心"]
    }

    def classify(self, user_input: str, context: Optional[dict] = None) -> IntentType:
        """识别用户意图"""
        user_input = user_input.lower()

        # 计算各意图的匹配分数
        scores = {}
        for intent, keywords in self.KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in user_input)
            if score > 0:
                scores[intent] = score

        # 返回得分最高的意图
        if scores:
            return max(scores, key=scores.get)

        # 默认返回闲聊
        return IntentType.GENERAL_CHAT

    def requires_tool(self, intent: IntentType) -> bool:
        """判断意图是否需要调用工具"""
        tool_intents = [
            IntentType.QUERY_SCORE,
            IntentType.QUERY_MAJOR,
            IntentType.QUERY_COLLEGE,
            IntentType.RECOMMENDATION,
            IntentType.COMPARISON
        ]
        return intent in tool_intents
