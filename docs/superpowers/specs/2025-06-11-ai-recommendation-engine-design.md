# AI 推荐引擎层设计方案

## 概述

基于微服务架构的混合推荐系统，结合规则引擎、协同过滤和 DeepSeek 大模型，实现高考志愿填报的"千人千面"个性化推荐。

## 一、系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    API Gateway (FastAPI)                     │
│         统一入口 / 认证授权 / 请求路由 / 限流熔断              │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼──────┐    ┌────────▼────────┐   ┌──────▼──────┐
│  Rule Engine │    │ Collaborative   │   │  DeepSeek   │
│   Service    │    │ Filter Service  │   │Agent Service│
│              │    │                 │   │             │
│ • 分数匹配    │    │ • 相似考生分析   │   │ • 个性化推荐 │
│ • 位次筛选    │    │ • 群体选择模式   │   │ • 理由生成   │
│ • 批次过滤    │    │ • 热门专业发现   │   │ • 风险评估   │
└───────┬──────┘    └────────┬────────┘   └──────┬──────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                    ┌─────────▼──────────┐
                    │   Result Merger    │
                    │    & Ranker        │
                    │                    │
                    │ • 多源结果融合      │
                    │ • 综合排序算法      │
                    │ • 推荐列表生成      │
                    └─────────┬──────────┘
                              │
                    ┌─────────▼──────────┐
                    │   Response Cache   │
                    │      (Redis)       │
                    └────────────────────┘
```

## 二、服务组件详解

### 2.1 API Gateway

**职责**：统一入口，路由请求到各服务

**接口**：`POST /api/v1/recommend` — 主推荐接口

**输入**：考生信息（分数、位次、兴趣、地域偏好等）

**输出**：排序后的推荐院校专业列表

### 2.2 Rule Engine Service

**职责**：基于规则的初筛，确保"够得着"

**算法**：
- 分数段匹配：±20分浮动范围
- 位次对比：历年录取位次 vs 考生位次
- 批次过滤：根据分数确定可报批次

**输出**：符合条件的候选院校列表（100-200所）

### 2.3 Collaborative Filter Service

**职责**：发现"相似考生"的选择模式

**算法**：
- 用户画像聚类（分数段、地域、兴趣标签）
- 协同过滤：相似考生报考的院校专业
- 热门趋势：当年报考热度分析

**输出**：基于群体智能的推荐权重

### 2.4 DeepSeek Agent Service

**职责**：生成个性化推荐理由和风险评估

**Prompt 工程**：
```
考生特征：{分数}分，位次{rank}，兴趣{interests}，
         地域偏好{location}，职业规划{career}
候选院校：{college_list}

请分析：
1. 每个候选院校的录取概率（冲/稳/保）
2. 专业与考生兴趣的匹配度
3. 院校特色与职业规划的契合度
4. 潜在风险和注意事项
5. 给出最终的推荐排序和理由
```

**输出**：自然语言推荐理由 + 结构化评分

### 2.5 Result Merger & Ranker

**职责**：融合多源结果，生成最终推荐

**算法**：
- 加权评分：规则得分 × 0.4 + 协同过滤得分 × 0.3 + DeepSeek 得分 × 0.3
- 多样性保证：避免推荐过于集中
- "冲稳保"分布：20%冲刺 + 50%稳妥 + 30%保底

## 三、数据流

```
考生请求
  │
  ▼
┌─────────────┐
│  信息收集    │ ← 分数、位次、兴趣、地域、职业倾向
│  (前端表单)  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Rule Engine │ ← 查询历年分数线数据库
│  初筛候选集  │ → 输出：200所候选院校
└──────┬──────┘
       │
       ▼
┌─────────────┐     ┌─────────────────┐
│ Collaborative│ ← → │   DeepSeek      │
│   Filter     │     │   Agent         │
│ 群体智能推荐  │     │  个性化分析      │
└──────┬──────┘     └────────┬────────┘
       │                      │
       └──────────┬───────────┘
                  ▼
         ┌─────────────┐
         │ Result Merger│
         │  综合排序    │ → 输出：Top 50 推荐
         └──────┬──────┘
                │
                ▼
         ┌─────────────┐
         │  推荐理由生成 │ ← DeepSeek 生成自然语言解释
         │  (千人千面)  │
         └──────┬──────┘
                │
                ▼
         ┌─────────────┐
         │  前端展示    │ ← 可视化推荐结果
         │  (卡片/对比) │
         └─────────────┘
```

## 四、核心算法

### 4.1 录取概率计算

```python
def calculate_admission_probability(
    candidate_score: float,
    candidate_rank: int,
    historical_scores: List[float],
    historical_ranks: List[int]
) -> Tuple[str, float]:
    """
    返回: (类别, 概率)
    类别: "冲刺" | "稳妥" | "保底"
    """
    # 基于位次的概率计算（位次比分数更稳定）
    rank_prob = calculate_rank_probability(candidate_rank, historical_ranks)
    
    # 基于分数的概率计算
    score_prob = calculate_score_probability(candidate_score, historical_scores)
    
    # 综合概率
    combined_prob = 0.7 * rank_prob + 0.3 * score_prob
    
    if combined_prob < 0.3:
        return "冲刺", combined_prob
    elif combined_prob < 0.7:
        return "稳妥", combined_prob
    else:
        return "保底", combined_prob
```

### 4.2 综合评分

```python
def calculate_final_score(
    rule_score: float,      # 规则引擎得分 (0-100)
    cf_score: float,        # 协同过滤得分 (0-100)
    deepseek_score: float,  # DeepSeek 得分 (0-100)
    interest_match: float   # 兴趣匹配度 (0-1)
) -> float:
    """
    综合评分 = 规则×0.3 + 协同×0.2 + DeepSeek×0.3 + 兴趣×0.2
    """
    return (
        rule_score * 0.3 +
        cf_score * 0.2 +
        deepseek_score * 0.3 +
        interest_match * 100 * 0.2
    )
```

## 五、错误处理

| 场景 | 处理策略 |
|------|----------|
| DeepSeek API 超时 | 降级为规则引擎 + 协同过滤推荐 |
| 数据缺失 | 使用相近省份/年份数据估算 |
| 考生信息不完整 | 引导补充，或使用默认值 |
| 高并发请求 | Redis 缓存 + 请求队列 |

## 六、技术栈

- **API Gateway**: FastAPI
- **服务通信**: HTTP/REST + Redis 消息队列
- **缓存**: Redis
- **数据库**: PostgreSQL (考生数据 + 推荐结果)
- **LLM**: DeepSeek API
- **部署**: Docker + Docker Compose

---

END OF DESIGN SPEC
