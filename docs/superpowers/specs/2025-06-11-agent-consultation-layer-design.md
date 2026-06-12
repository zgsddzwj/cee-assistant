# Agent 智能咨询层设计方案

## 概述

基于多轮对话的智能咨询 Agent，为高考考生提供全流程陪伴式志愿填报咨询服务。支持意图识别、对话管理、记忆系统和工具调用，实现自然流畅的人机交互。

## 一、系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent 智能咨询层                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│  │  意图识别    │    │  对话管理    │    │  记忆系统    │    │
│  │  (Intent    │───→│  (Dialogue  │←──→│  (Memory    │    │
│  │   Classifier)│    │   Manager)  │    │   Store)    │    │
│  └──────┬──────┘    └──────┬──────┘    └─────────────┘    │
│         │                  │                                │
│         │         ┌────────┴────────┐                      │
│         │         │                  │                      │
│         │    ┌────▼────┐      ┌────▼────┐                 │
│         │    │ 工具调用 │      │ DeepSeek │                 │
│         │    │ (Tools) │      │  (LLM)   │                 │
│         │    └────┬────┘      └────┬────┘                 │
│         │         │                  │                      │
│         │    ┌────┴────────────────┴────┐                 │
│         └───→│      回答生成 (Response     │                │
│              │       Generator)           │                │
│              └─────────────┬──────────────┘                │
│                            │                                │
│                            ▼                                │
│              ┌─────────────────────────┐                   │
│              │    用户界面 (WebSocket   │                   │
│              │     / SSE / HTTP)       │                   │
│              └─────────────────────────┘                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 二、核心组件

### 2.1 意图识别 (Intent Classifier)

**支持的意图类型：**

| 意图 | 示例 | 处理方式 |
|------|------|----------|
| `query_score` | "600分能上什么学校" | 调用推荐引擎 |
| `query_major` | "计算机专业怎么样" | 查询专业数据库 |
| `query_college` | "清华大学好吗" | 查询院校数据库 |
| `career_planning` | "我想当医生该学什么" | 职业规划对话 |
| `policy_question` | "平行志愿怎么填" | 政策知识库 |
| `recommendation` | "给我推荐几个学校" | 调用推荐引擎 |
| `comparison` | "A大学和B大学哪个好" | 对比分析 |
| `general_chat` | "我好紧张" | 情感支持 |

### 2.2 对话管理 (Dialogue Manager)

**对话阶段状态机：**

```
[开始] → [信息收集] → [意图确认] → [执行动作] → [结果呈现] → [结束]
           ↑                                    │
           └──────────── 追问/澄清 ←────────────┘
```

**对话阶段：**

| 阶段 | 目标 | Agent 行为 |
|------|------|-----------|
| `greeting` | 建立信任 | 自我介绍，了解考生基本情况 |
| `info_collection` | 收集信息 | 询问分数、位次、兴趣、地域偏好 |
| `clarification` | 澄清需求 | 确认理解正确，追问细节 |
| `recommendation` | 给出建议 | 调用推荐引擎，展示结果 |
| `explanation` | 解释说明 | 解释推荐理由，回答疑问 |
| `comparison` | 对比分析 | 多方案对比，优劣分析 |
| `confirmation` | 确认决策 | 帮助确认最终选择 |

### 2.3 记忆系统 (Memory Store)

**存储内容：**

```python
class AgentMemory:
    """Agent 记忆系统"""
    
    # 短期记忆（当前对话）
    current_dialog: List[Message] = []
    
    # 长期记忆（考生档案）
    student_profile: StudentProfile = None
    
    # 对话历史摘要
    conversation_summary: str = ""
    
    # 已推荐过的院校（避免重复）
    recommended_colleges: Set[str] = set()
    
    # 考生关注点
    interests_focus: List[str] = []
    
    # 决策状态
    decision_stage: str = "exploring"  # exploring / comparing / deciding / confirmed
```

### 2.4 工具调用 (Tools)

**可用工具集：**

| 工具 | 描述 | 参数 |
|------|------|------|
| `get_recommendation` | 获取院校专业推荐 | score, rank, province, interests |
| `query_college_info` | 查询院校详细信息 | college_name |
| `query_major_info` | 查询专业详细信息 | major_name |
| `compare_colleges` | 对比多所院校 | college_names |
| `get_admission_probability` | 计算录取概率 | score, college_name, major_name |

## 三、DeepSeek Prompt 工程

### 3.1 系统 Prompt

```
你是一位资深的高考志愿填报专家，拥有20年指导经验。你的目标是帮助考生做出最适合自己的志愿选择。

## 核心能力
1. 院校专业分析 - 深入了解全国各院校特色、专业优势
2. 录取概率评估 - 基于历年数据准确评估录取可能性
3. 职业规划指导 - 结合考生兴趣特长推荐适合方向
4. 政策解读 - 熟悉各省招生政策、填报规则

## 对话风格
- 亲切专业，像一位耐心的老师
- 善于倾听，先理解再建议
- 数据驱动，用事实支撑观点
- 鼓励探索，帮助考生发现自己的兴趣

## 重要原则
- 不夸大录取概率，实事求是
- 尊重考生意愿，不强行推销
- 关注长远发展，不只看重分数
- 提醒风险，帮助做好保底方案
```

## 四、典型对话流程

### 4.1 初次咨询

```
考生: "你好，我是今年高考考生，想咨询一下志愿填报"

Agent: "你好！很高兴能帮助你。我是你的志愿填报助手。
为了给你更精准的建议，想先了解一下你的基本情况：

1. 你今年高考分数是多少？全省排名大概多少位？
2. 你是文科还是理科（或新高考选科）？
3. 你所在的省份是？
4. 有没有特别感兴趣的专业方向或职业目标？

这些信息会帮助我为你量身定制推荐方案。"
```

### 4.2 分数查询推荐

```
考生: "我考了620分，位次8000，想学计算机"

Agent: [调用 get_recommendation 工具]
"根据你的分数和位次，我为你筛选了一些计算机相关专业：

【冲刺】
- 北京邮电大学 计算机科学与技术 (录取概率约30%)
  理由：该校计算机实力强，你的分数接近往年录取线

【稳妥】  
- 西安电子科技大学 软件工程 (录取概率约65%)
  理由：计算机特色院校，专业实力强，你的分数匹配度较高

【保底】
- 重庆邮电大学 计算机科学与技术 (录取概率约85%)
  理由：专业实力不错，你的分数有优势

你对这些学校有什么了解吗？或者想了解其他方面的信息？"
```

### 4.3 深度咨询

```
考生: "北邮和西电哪个更好？"

Agent: [调用 compare_colleges 工具]
"这两所学校都是计算机领域的强校，各有特色：

【北京邮电大学】
- 优势：地理位置好（北京），互联网大厂认可度高，校友资源丰富
- 特色：通信与计算机结合，5G、人工智能方向强
- 就业：BAT、字节跳动等大厂录取率高

【西安电子科技大学】
- 优势：军工背景，科研实力强，性价比极高
- 特色：雷达、信息安全、人工智能方向国内顶尖
- 就业：华为、中兴等企业重点招聘院校

【建议】
如果你更看重：
- 实习机会和互联网氛围 → 选北邮
- 科研深造和性价比 → 选西电

你的职业规划是什么？这会影响选择。"
```

## 五、技术实现

```python
class GaokaoAgent:
    """高考志愿填报智能 Agent"""
    
    def __init__(self):
        self.llm = DeepSeekClient()
        self.memory = AgentMemory()
        self.intent_classifier = IntentClassifier()
        self.tool_executor = ToolExecutor()
        self.dialogue_manager = DialogueManager()
    
    async def chat(self, user_input: str) -> str:
        # 1. 更新记忆
        self.memory.add_message("user", user_input)
        
        # 2. 识别意图
        intent = self.intent_classifier.classify(user_input, self.memory)
        
        # 3. 管理对话状态
        self.dialogue_manager.transition(intent)
        
        # 4. 执行动作
        if intent.requires_tool:
            tool_result = self.tool_executor.execute(intent, self.memory)
            response = self.llm.generate_response(
                user_input=user_input,
                context=self.memory.summary(),
                tool_result=tool_result
            )
        else:
            response = self.llm.generate_response(
                user_input=user_input,
                context=self.memory.summary()
            )
        
        # 5. 更新记忆
        self.memory.add_message("assistant", response)
        
        return response
```

## 六、错误处理

| 场景 | 处理策略 |
|------|----------|
| 意图识别失败 | 使用通用回复，引导用户明确需求 |
| 工具调用失败 | 告知用户暂时无法查询，建议稍后重试 |
| DeepSeek API 超时 | 使用预设回复模板，保证响应速度 |
| 考生信息不足 | 主动询问缺失信息，引导补充 |

## 七、技术栈

- **LLM**: DeepSeek API
- **对话管理**: 状态机 + 上下文管理
- **记忆存储**: Redis + PostgreSQL
- **接口**: WebSocket / SSE / HTTP
- **部署**: Docker + Docker Compose

---

END OF DESIGN SPEC
