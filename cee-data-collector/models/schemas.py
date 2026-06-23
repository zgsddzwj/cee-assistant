# models/schemas.py
"""数据模型定义 - 使用 Pydantic 进行数据验证和序列化

包含：
1. 分数线数据模型
2. 一分一段表模型
3. 院校数据模型
4. 专业数据模型
5. 用户查询模型
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class SubjectType(str, Enum):
    """科目类型"""
    WENKE = "文科"
    LIKE = "理科"
    ZONGHE = "综合"

class BatchType(str, Enum):
    """批次类型"""
    BENKE_YI = "本科一批"
    BENKE_ER = "本科二批"
    BENKE = "本科批"
    ZHUANKE = "专科批"
    TI_QIAN = "提前批"

class UniversityTier(int, Enum):
    """院校层次"""
    TOP = 1  # 985/211/双一流
    KEY = 2  # 省重点
    GENERAL = 3  # 普通本科

class ScoreLine(BaseModel):
    """分数线数据模型"""
    province: str = Field(..., description="省份代码")
    province_name: Optional[str] = Field(None, description="省份名称")
    year: int = Field(..., ge=2010, le=2030, description="年份")
    batch: BatchType = Field(..., description="批次")
    score: int = Field(..., ge=0, le=750, description="分数线")
    subject_type: SubjectType = Field(..., description="科目类型")
    updated_at: Optional[str] = Field(None, description="更新时间")
    
    class Config:
        json_schema_extra = {
            "example": {
                "province": "beijing",
                "province_name": "北京",
                "year": 2024,
                "batch": "本科一批",
                "score": 580,
                "subject_type": "综合",
                "updated_at": "2024-06-01T00:00:00"
            }
        }

class RankEntry(BaseModel):
    """一分一段表数据模型"""
    province: str = Field(..., description="省份代码")
    province_name: Optional[str] = Field(None, description="省份名称")
    year: int = Field(..., ge=2010, le=2030, description="年份")
    score: int = Field(..., ge=0, le=750, description="分数")
    count: int = Field(..., ge=0, description="同分人数")
    cumulative_count: int = Field(..., ge=0, description="累计人数")
    subject_type: SubjectType = Field(..., description="科目类型")
    updated_at: Optional[str] = Field(None, description="更新时间")
    
    @validator('cumulative_count')
    def validate_cumulative(cls, v, values):
        if 'count' in values and v < values['count']:
            raise ValueError('cumulative_count must be >= count')
        return v

class Major(BaseModel):
    """专业数据模型"""
    name: str = Field(..., description="专业名称")
    code: str = Field(..., description="专业代码")
    category: str = Field(..., description="学科门类")
    admission_score: int = Field(..., ge=0, le=750, description="录取分数")
    plan_count: int = Field(..., ge=0, description="招生人数")
    tuition: int = Field(..., ge=0, description="学费")
    duration: int = Field(default=4, ge=2, le=8, description="学制")
    hot: bool = Field(default=False, description="是否热门")
    description: Optional[str] = Field(None, description="专业介绍")
    career_prospects: Optional[List[str]] = Field(None, description="就业方向")

class University(BaseModel):
    """院校数据模型"""
    university_id: str = Field(..., description="院校代码")
    university_name: str = Field(..., description="院校名称")
    province: str = Field(..., description="所在省份")
    city: Optional[str] = Field(None, description="所在城市")
    tier: UniversityTier = Field(..., description="院校层次")
    is_985: bool = Field(default=False, description="是否985")
    is_211: bool = Field(default=False, description="是否211")
    is_double_first: bool = Field(default=False, description="是否双一流")
    year: int = Field(..., ge=2010, le=2030, description="年份")
    majors: List[Major] = Field(default=[], description="开设专业")
    total_plan: int = Field(default=0, ge=0, description="总招生人数")
    website: Optional[str] = Field(None, description="官网")
    updated_at: Optional[str] = Field(None, description="更新时间")
    
    @validator('total_plan', always=True)
    def calculate_total_plan(cls, v, values):
        if 'majors' in values:
            return sum(m.plan_count for m in values['majors'])
        return v

class QueryRequest(BaseModel):
    """用户查询请求模型"""
    score: int = Field(..., ge=0, le=750, description="高考分数")
    rank: Optional[int] = Field(None, ge=1, description="全省排名")
    province: str = Field(..., description="考生省份")
    subject_type: SubjectType = Field(..., description="科目类型")
    year: int = Field(default=2024, ge=2010, le=2030, description="年份")
    interests: Optional[List[str]] = Field(None, description="兴趣方向")
    career_plan: Optional[str] = Field(None, description="职业规划")
    preferred_provinces: Optional[List[str]] = Field(None, description="意向省份")
    preferred_categories: Optional[List[str]] = Field(None, description="意向学科门类")
    
    class Config:
        json_schema_extra = {
            "example": {
                "score": 600,
                "rank": 15000,
                "province": "beijing",
                "subject_type": "综合",
                "year": 2024,
                "interests": ["编程", "数学"],
                "career_plan": "软件工程师"
            }
        }

class RecommendationResult(BaseModel):
    """推荐结果模型"""
    university: University = Field(..., description="院校信息")
    major: Major = Field(..., description="专业信息")
    match_score: float = Field(..., ge=0, le=100, description="匹配分数")
    probability: str = Field(..., description="录取概率")
    recommendation_type: str = Field(..., description="推荐类型（冲/稳/保）")
    reasons: List[str] = Field(default=[], description="推荐理由")

class DataSummary(BaseModel):
    """数据汇总模型"""
    year: int = Field(..., description="年份")
    generated_at: str = Field(..., description="生成时间")
    statistics: Dict[str, Any] = Field(..., description="统计数据")
    files: Dict[str, str] = Field(..., description="文件列表")

# 便捷类型别名
ScoreData = List[ScoreLine]
RankData = List[RankEntry]
UniversityData = List[University]
