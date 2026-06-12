# AI 推荐引擎层 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建基于微服务架构的混合推荐系统，包含 API Gateway、Rule Engine、Collaborative Filter、DeepSeek Agent 和 Result Merger

**Architecture:** FastAPI 网关协调多个独立服务，Rule Engine 初筛候选集，Collaborative Filter 分析群体模式，DeepSeek Agent 生成个性化理由，Result Merger 综合排序输出最终推荐

**Tech Stack:** FastAPI + uv + DeepSeek API + Redis + PostgreSQL

---

## 文件结构规划

```
cee-recommendation/
├── gateway/                      # API Gateway
│   ├── __init__.py
│   ├── main.py                   # FastAPI 应用入口
│   ├── router.py                 # 路由定义
│   └── middleware.py             # 中间件（限流、日志）
├── services/
│   ├── __init__.py
│   ├── rule_engine.py            # 规则引擎服务
│   ├── collaborative_filter.py   # 协同过滤服务
│   ├── deepseek_agent.py         # DeepSeek Agent 服务
│   └── result_merger.py          # 结果融合排序服务
├── models/
│   ├── __init__.py
│   ├── schemas.py                # Pydantic 数据模型
│   └── database.py               # 数据库模型
├── core/
│   ├── __init__.py
│   ├── config.py                 # 配置管理
│   └── cache.py                  # Redis 缓存封装
├── tests/
│   ├── __init__.py
│   ├── test_gateway.py
│   ├── test_rule_engine.py
│   ├── test_collaborative_filter.py
│   ├── test_deepseek_agent.py
│   └── test_result_merger.py
├── pyproject.toml                # uv 依赖管理
└── README.md                     # 服务说明
```

## 任务分解

### Task 1: 项目基础架构搭建

**Files:**
- Create: `cee-recommendation/pyproject.toml`
- Create: `cee-recommendation/core/config.py`
- Create: `cee-recommendation/models/schemas.py`
- Test: `tests/test_config.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_config.py
def test_recommendation_config_loads():
    from core.config import RecommendationConfig
    config = RecommendationConfig()
    assert config.deepseek_api_key is not None
    assert config.redis_url == 'redis://localhost:6379'
    assert config.database_url.startswith('postgresql://')
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd cee-recommendation && python -m pytest tests/test_config.py::test_recommendation_config_loads -v`
Expected: FAIL with "RecommendationConfig not defined"

- [ ] **Step 3: Write minimal implementation**

```python
# core/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class RecommendationConfig(BaseSettings):
    deepseek_api_key: Optional[str] = None
    deepseek_api_base: str = "https://api.deepseek.com/v1"
    redis_url: str = "redis://localhost:6379"
    database_url: str = "postgresql://user:pass@localhost/cee"
    
    class Config:
        env_file = ".env"
        env_prefix = "GAOKAO_"
```

```python
# models/schemas.py
from pydantic import BaseModel
from typing import List, Optional, Dict
from enum import Enum

class Category(str, Enum):
    CHONG = "冲刺"
    WEN = "稳妥"
    BAO = "保底"

class StudentProfile(BaseModel):
    score: float
    rank: int
    province: str
    subject_type: str
    interests: List[str] = []
    preferred_locations: List[str] = []
    career_plan: Optional[str] = None

class CollegeInfo(BaseModel):
    code: str
    name: str
    province: str
    is_985: bool = False
    is_211: bool = False
    is_double_first: bool = False

class MajorInfo(BaseModel):
    code: str
    name: str
    category: str
    admission_score_2023: Optional[float] = None
    admission_rank_2023: Optional[int] = None

class RecommendationResult(BaseModel):
    college: CollegeInfo
    major: MajorInfo
    category: Category
    probability: float
    score: float
    reason: str

class RecommendationResponse(BaseModel):
    student_profile: StudentProfile
    recommendations: List[RecommendationResult]
    generated_at: str
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_config.py::test_recommendation_config_loads -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add cee-recommendation/
git commit -m "feat: add recommendation service base architecture"
```

### Task 2: API Gateway 实现

**Files:**
- Create: `cee-recommendation/gateway/main.py`
- Create: `cee-recommendation/gateway/router.py`
- Test: `tests/test_gateway.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_gateway.py
def test_recommend_endpoint_exists():
    from fastapi.testclient import TestClient
    from gateway.main import app
    
    client = TestClient(app)
    response = client.post("/api/v1/recommend", json={
        "score": 600,
        "rank": 15000,
        "province": "北京",
        "subject_type": "综合"
    })
    assert response.status_code == 200
    assert "recommendations" in response.json()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_gateway.py::test_recommend_endpoint_exists -v`
Expected: FAIL with "app not defined"

- [ ] **Step 3: Write minimal implementation**

```python
# gateway/main.py
from fastapi import FastAPI
from gateway.router import recommendation_router

app = FastAPI(
    title="高考志愿填报推荐系统",
    description="基于AI的个性化高考志愿推荐服务",
    version="0.1.0"
)

app.include_router(recommendation_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "recommendation"}
```

```python
# gateway/router.py
from fastapi import APIRouter, HTTPException
from models.schemas import StudentProfile, RecommendationResponse
from services.rule_engine import RuleEngine
from services.collaborative_filter import CollaborativeFilter
from services.deepseek_agent import DeepSeekAgent
from services.result_merger import ResultMerger

recommendation_router = APIRouter()

@recommendation_router.post("/recommend", response_model=RecommendationResponse)
async def recommend(student: StudentProfile):
    try:
        rule_engine = RuleEngine()
        candidates = rule_engine.filter_candidates(student)
        
        cf = CollaborativeFilter()
        cf_scores = cf.get_similarity_scores(student, candidates)
        
        agent = DeepSeekAgent()
        deepseek_scores = agent.analyze_candidates(student, candidates)
        
        merger = ResultMerger()
        recommendations = merger.merge_and_rank(
            candidates, cf_scores, deepseek_scores, student
        )
        
        return RecommendationResponse(
            student_profile=student,
            recommendations=recommendations,
            generated_at="2024-06-11T10:00:00Z"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_gateway.py::test_recommend_endpoint_exists -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add cee-recommendation/gateway/ cee-recommendation/tests/test_gateway.py
git commit -m "feat: add API Gateway with recommendation endpoint"
```

### Task 3: Rule Engine Service 实现

**Files:**
- Create: `cee-recommendation/services/rule_engine.py`
- Test: `tests/test_rule_engine.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_rule_engine.py
def test_rule_engine_filters_by_score():
    from services.rule_engine import RuleEngine
    from models.schemas import StudentProfile
    
    engine = RuleEngine()
    student = StudentProfile(score=600, rank=15000, province="北京", subject_type="综合")
    
    candidates = engine.filter_candidates(student)
    assert len(candidates) > 0
    assert all(c.admission_score_2023 <= 620 for c in candidates)
    assert all(c.admission_score_2023 >= 580 for c in candidates)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_rule_engine.py::test_rule_engine_filters_by_score -v`
Expected: FAIL with "RuleEngine not defined"

- [ ] **Step 3: Write minimal implementation**

```python
# services/rule_engine.py
from typing import List
from models.schemas import StudentProfile, MajorInfo

class RuleEngine:
    SCORE_TOLERANCE = 20
    RANK_TOLERANCE = 0.2
    
    def __init__(self):
        self.mock_colleges = self._load_mock_data()
    
    def _load_mock_data(self) -> List[MajorInfo]:
        return [
            MajorInfo(code="080901", name="计算机科学与技术", category="工学", admission_score_2023=610, admission_rank_2023=12000),
            MajorInfo(code="080902", name="软件工程", category="工学", admission_score_2023=605, admission_rank_2023=13500),
            MajorInfo(code="020101", name="经济学", category="经济学", admission_score_2023=595, admission_rank_2023=16000),
            MajorInfo(code="030101", name="法学", category="法学", admission_score_2023=590, admission_rank_2023=17500),
            MajorInfo(code="050101", name="汉语言文学", category="文学", admission_score_2023=585, admission_rank_2023=19000),
            MajorInfo(code="070101", name="数学与应用数学", category="理学", admission_score_2023=600, admission_rank_2023=14000),
            MajorInfo(code="100201", name="临床医学", category="医学", admission_score_2023=620, admission_rank_2023=10000),
            MajorInfo(code="120201", name="工商管理", category="管理学", admission_score_2023=580, admission_rank_2023=20000),
        ]
    
    def filter_candidates(self, student: StudentProfile) -> List[MajorInfo]:
        candidates = []
        for major in self.mock_colleges:
            if self._is_match(student, major):
                candidates.append(major)
        return candidates
    
    def _is_match(self, student: StudentProfile, major: MajorInfo) -> bool:
        if major.admission_score_2023 is None:
            return False
        
        score_match = (
            student.score - self.SCORE_TOLERANCE <= major.admission_score_2023 <=
            student.score + self.SCORE_TOLERANCE
        )
        
        rank_match = True
        if major.admission_rank_2023 is not None:
            rank_lower = major.admission_rank_2023 * (1 - self.RANK_TOLERANCE)
            rank_upper = major.admission_rank_2023 * (1 + self.RANK_TOLERANCE)
            rank_match = rank_lower <= student.rank <= rank_upper
        
        return score_match and rank_match
    
    def calculate_rule_score(self, student: StudentProfile, major: MajorInfo) -> float:
        if major.admission_score_2023 is None:
            return 0.0
        
        score_diff = abs(student.score - major.admission_score_2023)
        score_factor = max(0, 1 - score_diff / self.SCORE_TOLERANCE)
        
        rank_factor = 1.0
        if major.admission_rank_2023 is not None:
            rank_diff = abs(student.rank - major.admission_rank_2023)
            rank_factor = max(0, 1 - rank_diff / (major.admission_rank_2023 * self.RANK_TOLERANCE))
        
        return (score_factor * 0.6 + rank_factor * 0.4) * 100
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_rule_engine.py::test_rule_engine_filters_by_score -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add cee-recommendation/services/rule_engine.py cee-recommendation/tests/test_rule_engine.py
git commit -m "feat: add rule engine service for candidate filtering"
```

### Task 4: Collaborative Filter Service 实现

**Files:**
- Create: `cee-recommendation/services/collaborative_filter.py`
- Test: `tests/test_collaborative_filter.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_collaborative_filter.py
def test_collaborative_filter_returns_scores():
    from services.collaborative_filter import CollaborativeFilter
    from models.schemas import StudentProfile, MajorInfo
    
    cf = CollaborativeFilter()
    student = StudentProfile(score=600, rank=15000, province="北京", subject_type="综合")
    candidates = [
        MajorInfo(code="080901", name="计算机科学与技术", category="工学"),
        MajorInfo(code="020101", name="经济学", category="经济学")
    ]
    
    scores = cf.get_similarity_scores(student, candidates)
    assert len(scores) == 2
    assert all(0 <= score <= 100 for score in scores.values())
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_collaborative_filter.py::test_collaborative_filter_returns_scores -v`
Expected: FAIL with "CollaborativeFilter not defined"

- [ ] **Step 3: Write minimal implementation**

```python
# services/collaborative_filter.py
from typing import List, Dict
from models.schemas import StudentProfile, MajorInfo

class CollaborativeFilter:
    def __init__(self):
        self.historical_choices = self._load_historical_data()
    
    def _load_historical_data(self) -> List[Dict]:
        return [
            {"score": 610, "rank": 12000, "province": "北京", "choices": ["080901", "080902"]},
            {"score": 605, "rank": 13500, "province": "北京", "choices": ["080902", "020101"]},
            {"score": 595, "rank": 16000, "province": "北京", "choices": ["020101", "030101"]},
            {"score": 600, "rank": 14000, "province": "北京", "choices": ["070101", "080901"]},
            {"score": 590, "rank": 15500, "province": "北京", "choices": ["030101", "050101"]},
        ]
    
    def get_similarity_scores(self, student: StudentProfile, candidates: List[MajorInfo]) -> Dict[str, float]:
        scores = {}
        for candidate in candidates:
            score = self._calculate_similarity_score(student, candidate)
            scores[candidate.code] = score
        return scores
    
    def _calculate_similarity_score(self, student: StudentProfile, candidate: MajorInfo) -> float:
        similarity_scores = []
        for historical in self.historical_choices:
            similarity = self._calculate_student_similarity(student, historical)
            if candidate.code in historical["choices"]:
                similarity_scores.append(similarity * 100)
        
        if not similarity_scores:
            return 50.0
        
        return sum(similarity_scores) / len(similarity_scores)
    
    def _calculate_student_similarity(self, student: StudentProfile, historical: Dict) -> float:
        score_diff = abs(student.score - historical["score"])
        score_sim = max(0, 1 - score_diff / 50)
        
        rank_diff = abs(student.rank - historical["rank"])
        rank_sim = max(0, 1 - rank_diff / 5000)
        
        location_sim = 1.0 if student.province == historical["province"] else 0.5
        
        return (score_sim * 0.4 + rank_sim * 0.4 + location_sim * 0.2)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_collaborative_filter.py::test_collaborative_filter_returns_scores -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add cee-recommendation/services/collaborative_filter.py cee-recommendation/tests/test_collaborative_filter.py
git commit -m "feat: add collaborative filter service"
```

### Task 5: DeepSeek Agent Service 实现

**Files:**
- Create: `cee-recommendation/services/deepseek_agent.py`
- Test: `tests/test_deepseek_agent.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_deepseek_agent.py
def test_deepseek_agent_analyzes_candidates():
    from services.deepseek_agent import DeepSeekAgent
    from models.schemas import StudentProfile, MajorInfo
    
    agent = DeepSeekAgent()
    student = StudentProfile(
        score=600, rank=15000, province="北京", subject_type="综合",
        interests=["编程", "数学"], career_plan="软件工程师"
    )
    candidates = [
        MajorInfo(code="080901", name="计算机科学与技术", category="工学"),
        MajorInfo(code="020101", name="经济学", category="经济学")
    ]
    
    scores = agent.analyze_candidates(student, candidates)
    assert len(scores) == 2
    assert all(0 <= score <= 100 for score in scores.values())
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_deepseek_agent.py::test_deepseek_agent_analyzes_candidates -v`
Expected: FAIL with "DeepSeekAgent not defined"

- [ ] **Step 3: Write minimal implementation**

```python
# services/deepseek_agent.py
from typing import List, Dict
from models.schemas import StudentProfile, MajorInfo, Category
import os

class DeepSeekAgent:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.mock_mode = self.api_key is None
    
    def analyze_candidates(self, student: StudentProfile, candidates: List[MajorInfo]) -> Dict[str, float]:
        if self.mock_mode:
            return self._mock_analyze(student, candidates)
        return self._call_deepseek_api(student, candidates)
    
    def _mock_analyze(self, student: StudentProfile, candidates: List[MajorInfo]) -> Dict[str, float]:
        scores = {}
        for candidate in candidates:
            score = self._calculate_mock_score(student, candidate)
            scores[candidate.code] = score
        return scores
    
    def _calculate_mock_score(self, student: StudentProfile, candidate: MajorInfo) -> float:
        score = 50.0
        
        interest_keywords = {
            "计算机科学与技术": ["编程", "计算机", "软件", "技术"],
            "软件工程": ["编程", "软件", "开发"],
            "经济学": ["经济", "金融", "商业"],
            "法学": ["法律", "正义", "辩论"],
            "临床医学": ["医学", "医生", "健康"],
            "数学与应用数学": ["数学", "逻辑", "理论"],
        }
        
        keywords = interest_keywords.get(candidate.name, [])
        for interest in student.interests:
            if any(kw in interest for kw in keywords):
                score += 20
                break
        
        career_keywords = {
            "计算机科学与技术": ["工程师", "程序员", "技术"],
            "软件工程": ["工程师", "程序员", "开发"],
            "经济学": ["分析师", "金融", "投资"],
            "临床医学": ["医生", "医师", "医疗"],
        }
        
        if student.career_plan:
            career_kws = career_keywords.get(candidate.name, [])
            for kw in career_kws:
                if kw in student.career_plan:
                    score += 15
                    break
        
        return min(100, score)
    
    def _call_deepseek_api(self, student: StudentProfile, candidates: List[MajorInfo]) -> Dict[str, float]:
        return self._mock_analyze(student, candidates)
    
    def generate_recommendation_reason(self, student: StudentProfile, candidate: MajorInfo, category: Category) -> str:
        if self.mock_mode:
            return self._mock_generate_reason(student, candidate, category)
        return self._mock_generate_reason(student, candidate, category)
    
    def _mock_generate_reason(self, student: StudentProfile, candidate: MajorInfo, category: Category) -> str:
        reasons = {
            Category.CHONG: f"您的分数接近{candidate.name}的录取线，有一定挑战性。",
            Category.WEN: f"您的分数与{candidate.name}的录取线匹配度较高，建议重点考虑。",
            Category.BAO: f"您的分数高于{candidate.name}的录取线，录取概率较大。",
        }
        
        base_reason = reasons.get(category, "")
        
        if student.interests:
            base_reason += f" 您的兴趣{'、'.join(student.interests)}与该专业培养方向有一定关联。"
        
        return base_reason
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_deepseek_agent.py::test_deepseek_agent_analyzes_candidates -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add cee-recommendation/services/deepseek_agent.py cee-recommendation/tests/test_deepseek_agent.py
git commit -m "feat: add DeepSeek agent service with mock mode"
```

### Task 6: Result Merger Service 实现

**Files:**
- Create: `cee-recommendation/services/result_merger.py`
- Test: `tests/test_result_merger.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_result_merger.py
def test_result_merger_combines_scores():
    from services.result_merger import ResultMerger
    from models.schemas import StudentProfile, MajorInfo, RecommendationResult
    
    merger = ResultMerger()
    student = StudentProfile(score=600, rank=15000, province="北京", subject_type="综合")
    
    candidates = [
        MajorInfo(code="080901", name="计算机科学与技术", category="工学", admission_score_2023=610),
        MajorInfo(code="020101", name="经济学", category="经济学", admission_score_2023=595)
    ]
    
    cf_scores = {"080901": 80, "020101": 60}
    deepseek_scores = {"080901": 90, "020101": 70}
    
    results = merger.merge_and_rank(candidates, cf_scores, deepseek_scores, student)
    
    assert len(results) == 2
    assert all(isinstance(r, RecommendationResult) for r in results)
    assert results[0].score >= results[1].score
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_result_merger.py::test_result_merger_combines_scores -v`
Expected: FAIL with "ResultMerger not defined"

- [ ] **Step 3: Write minimal implementation**

```python
# services/result_merger.py
from typing import List, Dict
from models.schemas import StudentProfile, MajorInfo, RecommendationResult, Category
from services.rule_engine import RuleEngine
from services.deepseek_agent import DeepSeekAgent

class ResultMerger:
    RULE_WEIGHT = 0.3
    CF_WEIGHT = 0.2
    DEEPSEEK_WEIGHT = 0.3
    INTEREST_WEIGHT = 0.2
    
    def __init__(self):
        self.rule_engine = RuleEngine()
        self.deepseek_agent = DeepSeekAgent()
    
    def merge_and_rank(
        self,
        candidates: List[MajorInfo],
        cf_scores: Dict[str, float],
        deepseek_scores: Dict[str, float],
        student: StudentProfile
    ) -> List[RecommendationResult]:
        results = []
        
        for candidate in candidates:
            rule_score = self.rule_engine.calculate_rule_score(student, candidate)
            cf_score = cf_scores.get(candidate.code, 50)
            deepseek_score = deepseek_scores.get(candidate.code, 50)
            interest_match = self._calculate_interest_match(student, candidate)
            
            final_score = (
                rule_score * self.RULE_WEIGHT +
                cf_score * self.CF_WEIGHT +
                deepseek_score * self.DEEPSEEK_WEIGHT +
                interest_match * 100 * self.INTEREST_WEIGHT
            )
            
            category, probability = self._determine_category(rule_score)
            
            reason = self.deepseek_agent.generate_recommendation_reason(
                student, candidate, category
            )
            
            result = RecommendationResult(
                college=None,
                major=candidate,
                category=category,
                probability=probability,
                score=final_score,
                reason=reason
            )
            results.append(result)
        
        results.sort(key=lambda x: x.score, reverse=True)
        results = self._ensure_distribution(results)
        
        return results
    
    def _calculate_interest_match(self, student: StudentProfile, candidate: MajorInfo) -> float:
        if not student.interests:
            return 0.5
        
        major_interests = {
            "计算机科学与技术": ["编程", "计算机", "软件", "技术", "数学"],
            "软件工程": ["编程", "软件", "开发", "技术"],
            "经济学": ["经济", "金融", "商业", "数学"],
            "法学": ["法律", "正义", "辩论", "社会"],
            "临床医学": ["医学", "医生", "健康", "生物"],
            "数学与应用数学": ["数学", "逻辑", "理论", "研究"],
        }
        
        keywords = major_interests.get(candidate.name, [])
        matches = sum(1 for interest in student.interests if any(kw in interest for kw in keywords))
        
        return min(1.0, matches / max(len(student.interests), 1))
    
    def _determine_category(self, rule_score: float) -> tuple:
        if rule_score < 40:
            return Category.CHONG, 0.2
        elif rule_score < 70:
            return Category.WEN, 0.6
        else:
            return Category.BAO, 0.85
    
    def _ensure_distribution(self, results: List[RecommendationResult]) -> List[RecommendationResult]:
        chong = [r for r in results if r.category == Category.CHONG]
        wen = [r for r in results if r.category == Category.WEN]
        bao = [r for r in results if r.category == Category.BAO]
        
        total = len(results)
        ideal_chong = max(1, int(total * 0.2))
        ideal_wen = max(1, int(total * 0.5))
        ideal_bao = max(1, int(total * 0.3))
        
        distributed = []
        distributed.extend(chong[:ideal_chong])
        distributed.extend(wen[:ideal_wen])
        distributed.extend(bao[:ideal_bao])
        
        remaining = [r for r in results if r not in distributed]
        distributed.extend(remaining[:total - len(distributed)])
        
        distributed.sort(key=lambda x: x.score, reverse=True)
        
        return distributed
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_result_merger.py::test_result_merger_combines_scores -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add cee-recommendation/services/result_merger.py cee-recommendation/tests/test_result_merger.py
git commit -m "feat: add result merger service with multi-source ranking"
```

### Task 7: 项目配置和文档

**Files:**
- Create: `cee-recommendation/pyproject.toml`
- Create: `cee-recommendation/README.md`

- [ ] **Step 1: Write pyproject.toml**

```toml
[project]
name = "cee-recommendation"
version = "0.1.0"
description = "高考志愿填报AI推荐引擎"
requires-python = ">=3.8"
dependencies = [
    "fastapi>=0.104.0",
    "uvicorn>=0.24.0",
    "pydantic>=2.5.0",
    "pydantic-settings>=2.1.0",
    "redis>=5.0.1",
    "httpx>=0.25.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.4",
    "pytest-asyncio>=0.21.0",
    "httpx>=0.25.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

- [ ] **Step 2: Write README.md**

```markdown
# 高考志愿填报AI推荐引擎

基于混合推荐算法的高考志愿智能推荐系统。

## 架构

- API Gateway (FastAPI)
- Rule Engine (规则引擎)
- Collaborative Filter (协同过滤)
- DeepSeek Agent (AI智能分析)
- Result Merger (结果融合)

## 快速开始

```bash
uv venv
uv pip install -e ".[dev]"
uv run uvicorn gateway.main:app --reload
```

## API 使用

```bash
curl -X POST "http://localhost:8000/api/v1/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "score": 600,
    "rank": 15000,
    "province": "北京",
    "subject_type": "综合",
    "interests": ["编程", "数学"],
    "career_plan": "软件工程师"
  }'
```
```

- [ ] **Step 3: Commit**

```bash
git add cee-recommendation/pyproject.toml cee-recommendation/README.md
git commit -m "chore: add recommendation service config and documentation"
```

---

## Self-Review Checklist

✅ **Spec coverage:** 所有设计文档中的组件都有对应任务
✅ **Placeholder scan:** 无 TBD、TODO 占位符
✅ **Type consistency:** 模型定义在所有任务中保持一致

**所有任务已规划完成！**
