# 高考志愿填报智能咨询 Agent

多轮对话式智能咨询 Agent，为高考考生提供全流程志愿填报咨询服务。

## 功能特性

- **意图识别**：基于关键词匹配自动识别用户咨询意图（分数查询、专业咨询、院校对比等）
- **多轮对话**：支持上下文感知的连续对话，自动管理对话阶段（问候→信息收集→推荐→解释）
- **记忆系统**：记住考生分数、位次、省份、兴趣等信息，避免重复询问
- **工具调用**：可集成推荐引擎进行院校专业推荐

## 项目结构

```
cee-agent/
├── agent/
│   ├── core.py              # Agent 核心类，协调各组件
│   ├── intent_classifier.py # 意图识别器
│   ├── dialogue_manager.py  # 对话状态管理
│   └── memory.py            # 记忆存储
├── models/
│   └── schemas.py           # 数据模型（意图类型、消息、记忆等）
├── tests/                   # 测试用例
├── pyproject.toml           # 项目配置
└── README.md                # 本文档
```

## 快速开始

### 安装依赖

```bash
cd cee-agent
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

### 运行测试

```bash
python -m pytest tests/ -v
```

### 使用示例

```python
from agent.core import CeeAgent

agent = CeeAgent()

# 第一轮：问候
response = agent.chat("你好，我想咨询志愿填报")
print(response)
# 输出：你好！我是你的高考志愿填报助手...

# 第二轮：提供分数信息
response = agent.chat("我考了600分，位次15000")
print(response)
# 输出：收到！我已经记录了你的信息...

# 第三轮：请求推荐
response = agent.chat("给我推荐几个学校")
print(response)
# 输出：根据你的分数(600.0分)和位次(15000)，我为你推荐...
```

## 支持的意图类型

| 意图 | 示例 | 说明 |
|------|------|------|
| `query_score` | "600分能上什么学校" | 基于分数的院校查询 |
| `query_major` | "计算机专业怎么样" | 专业信息咨询 |
| `query_college` | "清华大学好吗" | 院校信息咨询 |
| `career_planning` | "我想当医生该学什么" | 职业规划 |
| `policy_question` | "平行志愿怎么填" | 政策解读 |
| `recommendation` | "给我推荐几个学校" | 主动推荐 |
| `comparison` | "A大学和B大学哪个好" | 院校对比 |
| `general_chat` | "你好" / "谢谢" | 闲聊/情感支持 |

## 对话阶段

```
[问候] → [信息收集] → [意图确认] → [执行动作] → [结果呈现] → [结束]
   ↑                                    │
   └──────────── 追问/澄清 ←────────────┘
```

## 开发计划

- [x] 基础架构搭建
- [x] 意图识别实现
- [x] 记忆系统实现
- [x] 对话管理实现
- [x] Agent 核心实现
- [ ] DeepSeek LLM 集成
- [ ] 工具调用（推荐引擎对接）
- [ ] WebSocket 实时对话接口
- [ ] Redis 持久化存储

## 技术栈

- **Python** 3.8+
- **Pydantic** - 数据模型验证
- **pytest** - 单元测试
- **DeepSeek API** - LLM 驱动（待集成）

## License

MIT
