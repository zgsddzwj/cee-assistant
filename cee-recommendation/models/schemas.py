# models/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class Category(str, Enum):
    """推荐类别：冲/稳/保"""
    CHONG = "冲刺"
    WEN = "稳妥"
    BAO = "保底"


class StudentProfile(BaseModel):
    """考生档案"""
    score: float
    rank: int
    province: str
    subject_type: str
    interests: List[str] = []
    preferred_locations: List[str] = []
    career_plan: Optional[str] = None


class CollegeInfo(BaseModel):
    """院校信息"""
    code: str
    name: str
    province: str
    is_985: bool = False
    is_211: bool = False
    is_double_first: bool = False


class MajorInfo(BaseModel):
    """专业信息"""
    code: str
    name: str
    category: str
    admission_score_2023: Optional[float] = None
    admission_rank_2023: Optional[int] = None


class RecommendationResult(BaseModel):
    """推荐结果"""
    college: Optional[CollegeInfo] = None
    major: MajorInfo
    category: Category
    probability: float
    score: float
    reason: str


class RecommendationResponse(BaseModel):
    """推荐响应"""
    student_profile: StudentProfile
    recommendations: List[RecommendationResult]
    generated_at: str