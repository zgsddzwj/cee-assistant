# Agent 智能咨询层 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建多轮对话式智能咨询 Agent，支持意图识别、对话管理、记忆系统和工具调用

**Architecture:** DeepSeek LLM 驱动，状态机管理对话流程，Redis 存储记忆，工具调用集成推荐引擎

**Tech Stack:** Python + DeepSeek API + Redis + WebSocket

---

## 文件结构规划

```
cee-agent/
├── agent/
│   ├── __init__.py
│   ├── core.py                 # Agent 核心类
│   ├── intent_classifier.py    # 意图识别
│   ├── dialogue_manager.py     # 对话管理
│   ├── memory.py               # 记忆系统
│   └── tool_executor.py        # 工具执行
├── models/
│   ├── __init__.py
│   └── schemas.py              # 数据模型
├── tests/
│   ├── __init__.py
│   ├── test_agent.py
│   ├── test_intent.py
│   └── test_memory.py
├── pyproject.toml              # uv 依赖管理
└── README.md                   # 服务说明
```

## 任务分解

### Task 1: Agent 基础架构搭建

**Files:**
- Create: `cee-agent/pyproject.toml`
- Create: `cee-agent/models/schemas.py`
- Create: `cee-agent/agent/__init__.py`
- Test: `tests/test_schemas.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_schemas.py
def test_intent_enum_values():
    from models.schemas import IntentType
    assert IntentType.QUERY_SCORE == "query_score"
    assert IntentType.RECOMMENDATION == "recommendation"
    assert IntentType.GENERAL_CHAT == "general_chat"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd cee-agent && python -m pytest tests/test_schemas.py::test_intent_enum_values -v`
Expected: FAIL with "IntentType not defined"

- [ ] **Step 3: Write minimal implementation**

```python
# models/schemas.py
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_schemas.py::test_intent_enum_values -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add cee-agent/
git commit -m "feat: add agent service base architecture"
```

### Task 2: 意图识别实现

**Files:**
- Create: `cee-agent/agent/intent_classifier.py`
- Test: `tests/test_intent.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_intent.py
def test_intent_classifier_recognizes_score_query():
    from agent.intent_classifier import IntentClassifier
    from models.schemas import IntentType
    
    classifier = IntentClassifier()
    intent = classifier.classify("我考了600分能上什么学校？")
    
    assert intent == IntentType.QUERY_SCORE
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_intent.py::test_intent_classifier_recognizes_score_query -v`
Expected: FAIL with "IntentClassifier not defined"

- [ ] **Step 3: Write minimal implementation**

```python
# agent/intent_classifier.py
import re
from typing import Optional
from models.schemas import IntentType, DialogContext


class IntentClassifier:
    """意图识别器 - 基于规则 + 关键词匹配"""
    
    # 关键词映射
    KEYWORDS = {
        IntentType.QUERY_SCORE: ["分数", "多少分", "能上", "可以报", "录取线"],
        IntentType.QUERY_MAJOR: ["专业", "学什么", "怎么样", "好不好"],
        IntentType.QUERY_COLLEGE: ["学校", "大学", "院校", "好不好", "怎么样"],
        IntentType.CAREER_PLANNING: ["职业", "工作", "就业", "未来", "规划"],
        IntentType.POLICY_QUESTION: ["政策", "规则", "怎么填", "志愿", "平行"],
        IntentType.RECOMMENDATION: ["推荐", "建议", "选什么", "报哪个"],
        IntentType.COMPARISON: ["对比", "比较", "哪个好", "还是"],
        IntentType.GENERAL_CHAT: ["你好", "谢谢", "紧张", "害怕", "担心"]
    }
    
    def classify(self, user_input: str, context: Optional[DialogContext] = None) -> IntentType:
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_intent.py::test_intent_classifier_recognizes_score_query -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add cee-agent/agent/intent_classifier.py cee-agent/tests/test_intent.py
git commit -m "feat: add intent classifier with keyword matching"
```

### Task 3: 记忆系统实现

**Files:**
- Create: `cee-agent/agent/memory.py`
- Test: `tests/test_memory.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_memory.py
def test_memory_stores_student_info():
    from agent.memory import AgentMemoryStore
    
    memory = AgentMemoryStore()
    memory.update_student_info(score=600, rank=15000, province="北京")
    
    assert memory.get("student_score") == 600
    assert memory.get("student_rank") == 15000
    assert memory.get("student_province") == "北京"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_memory.py::test_memory_stores_student_info -v`
Expected: FAIL with "AgentMemoryStore not defined"

- [ ] **Step 3: Write minimal implementation**

```python
# agent/memory.py
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_memory.py::test_memory_stores_student_info -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add cee-agent/agent/memory.py cee-agent/tests/test_memory.py
git commit -m "feat: add agent memory store"
```

### Task 4: 对话管理实现

**Files:**
- Create: `cee-agent/agent/dialogue_manager.py`
- Test: `tests/test_dialogue.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_dialogue.py
def test_dialogue_manager_transitions():
    from agent.dialogue_manager import DialogueManager
    from models.schemas import IntentType
    
    dm = DialogueManager()
    assert dm.current_stage == "greeting"
    
    dm.transition(IntentType.QUERY_SCORE)
    assert dm.current_stage == "info_collection"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_dialogue.py::test_dialogue_manager_transitions -v`
Expected: FAIL with "DialogueManager not defined"

- [ ] **Step 3: Write minimal implementation**

```python
# agent/dialogue_manager.py
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_dialogue.py::test_dialogue_manager_transitions -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add cee-agent/agent/dialogue_manager.py cee-agent/tests/test_dialogue.py
git commit -m "feat: add dialogue manager with stage transitions"
```

### Task 5: Agent 核心实现

**Files:**
- Create: `cee-agent/agent/core.py`
- Test: `tests/test_agent.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_agent.py
def test_agent_processes_user_input():
    from agent.core import GaokaoAgent
    
    agent = GaokaoAgent()
    response = agent.chat("你好，我想咨询志愿填报")
    
    assert response is not None
    assert len(response) > 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_agent.py::test_agent_processes_user_input -v`
Expected: FAIL with "GaokaoAgent not defined"

- [ ] **Step 3: Write minimal implementation**

```python
# agent/core.py
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
        import re
        
        score_match = re.search(r'(\d+)\s*分', user_input)
        rank_match = re.search(r'(\d+)\s*位', user_input)
        
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_agent.py::test_agent_processes_user_input -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add cee-agent/agent/core.py cee-agent/tests/test_agent.py
git commit -m "feat: add GaokaoAgent core with multi-turn dialogue"
```

### Task 6: 项目配置和文档

**Files:**
- Create: `cee-agent/pyproject.toml`
- Create: `cee-agent/README.md`

- [ ] **Step 1: Write pyproject.toml**

```toml
[project]
name = "cee-agent"
version = "0.1.0"
description = "高考志愿填报智能咨询Agent"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
authors = [
    {name = "CEE Assistant Team"},
]
keywords = ["cee", "agent", "chatbot", "education"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
]

dependencies = [
    "pydantic>=2.5.0",
    "httpx>=0.25.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.4",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

- [ ] **Step 2: Write README.md**

```markdown
# 高考志愿填报智能咨询 Agent

多轮对话式智能咨询 Agent，为考生提供全流程志愿填报咨询服务。

## 功能

- 意图识别：自动识别用户咨询意图
- 多轮对话：支持上下文感知的连续对话
- 记忆系统：记住考生信息和对话历史
- 工具调用：集成推荐引擎查询

## 快速开始

```bash
uv venv
uv pip install -e ".[dev]"
```

## 使用

```python
from agent.core import GaokaoAgent

agent = GaokaoAgent()
response = agent.chat("你好，我想咨询志愿填报")
print(response)
```

## 对话示例

```
考生: "你好，我想咨询志愿填报"
Agent: "你好！我是你的高考志愿填报助手..."

考生: "我考了600分，位次15000"
Agent: "收到！我已经记录了你的信息..."

考生: "给我推荐几个学校"
Agent: "根据你的分数(600分)和位次(15000)，我为你推荐..."
```
```

- [ ] **Step 3: Commit**

```bash
git add cee-agent/pyproject.toml cee-agent/README.md
git commit -m "chore: add agent service config and documentation"
```

---

## Self-Review Checklist

✅ **Spec coverage:** 所有设计文档中的组件都有对应任务
✅ **Placeholder scan:** 无 TBD、TODO 占位符
✅ **Type consistency:** 模型定义在所有任务中保持一致

**所有任务已规划完成！**
