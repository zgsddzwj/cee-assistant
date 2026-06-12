import re
from typing import Optional
from models.schemas import IntentType
from agent.intent_classifier import IntentClassifier
from agent.dialogue_manager import DialogueManager
from agent.memory import AgentMemoryStore


class GaokaoAgent:
    """高考志愿填报智能 Agent"""

    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.dialogue_manager = DialogueManager()
        self.memory = AgentMemoryStore()
        self.mock_mode = True  # 开发阶段使用模拟模式

    def chat(self, user_input: str) -> str:
        """处理用户输入并返回回复"""
        # 1. 保存用户消息
        self.memory.add_message("user", user_input)

        # 2. 识别意图
        intent = self.intent_classifier.classify(user_input)

        # 3. 更新对话阶段
        self.dialogue_manager.transition(intent)

        # 4. 生成回复
        response = self._generate_response(user_input, intent)

        # 5. 保存助手回复
        self.memory.add_message("assistant", response)

        return response

    def _generate_response(self, user_input: str, intent: IntentType) -> str:
        """根据意图生成回复"""
        stage = self.dialogue_manager.get_stage()

        # 根据阶段和意图生成回复
        if stage == "greeting":
            return self._greeting_response()
        elif stage == "info_collection":
            return self._info_collection_response(user_input, intent)
        elif stage == "recommendation":
            return self._recommendation_response(user_input)
        else:
            return self._default_response(user_input)

    def _greeting_response(self) -> str:
        """问候回复"""
        return ("你好！我是你的高考志愿填报助手。\n\n"
                "我可以帮助你：\n"
                "- 分析你的分数能上哪些学校\n"
                "- 推荐适合你的专业方向\n"
                "- 解答志愿填报政策问题\n"
                "- 对比不同院校的优劣\n\n"
                "为了更好地帮助你，能否告诉我：\n"
                "1. 你的高考分数和全省排名？\n"
                "2. 你所在的省份？\n"
                "3. 有没有感兴趣的专业或职业方向？")

    def _info_collection_response(self, user_input: str, intent: IntentType) -> str:
        """信息收集回复"""
        # 尝试从输入中提取分数和位次
        score_match = re.search(r'(\d+)\s*分', user_input)
        rank_match = re.search(r'(?:位次|排名|第)(\d+)', user_input)

        if score_match:
            self.memory.update_student_info(score=float(score_match.group(1)))

        if rank_match:
            self.memory.update_student_info(rank=int(rank_match.group(1)))

        return ("收到！我已经记录了你的信息。\n"
                "接下来你可以问我：\n"
                "- '给我推荐几个学校'\n"
                "- '计算机专业怎么样'\n"
                "- 'XX大学和YY大学哪个好'")

    def _recommendation_response(self, user_input: str) -> str:
        """推荐回复"""
        score = self.memory.get("student_score")
        rank = self.memory.get("student_rank")

        if not score or not rank:
            return "为了给你准确的推荐，请先告诉我你的分数和位次。"

        return (f"根据你的分数({score}分)和位次({rank})，我为你推荐：\n\n"
                "【冲刺】\n"
                "- 北京邮电大学 计算机类\n"
                "- 西安电子科技大学 软件工程\n\n"
                "【稳妥】\n"
                "- 重庆邮电大学 计算机科学与技术\n"
                "- 杭州电子科技大学 软件工程\n\n"
                "【保底】\n"
                "- 桂林电子科技大学 计算机类\n\n"
                "你想了解哪所学校的详细信息？")

    def _default_response(self, user_input: str) -> str:
        """默认回复"""
        return ("我理解你的问题。作为志愿填报助手，我可以帮你：\n"
                "1. 根据分数推荐院校\n"
                "2. 分析专业就业前景\n"
                "3. 对比不同学校\n"
                "4. 解答填报政策\n\n"
                "你想了解哪方面？")
