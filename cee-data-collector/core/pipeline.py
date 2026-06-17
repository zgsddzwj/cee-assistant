# core/pipeline.py
from typing import Dict, List, Any, Optional, Callable
import logging
from dataclasses import dataclass
from enum import Enum

class DataType(Enum):
    """数据类型枚举"""
    SCORE = "score"
    RANK = "rank"
    UNIVERSITY = "university"
    MAJOR = "major"

class ValidationError(Exception):
    """数据验证错误"""
    pass

@dataclass
class ValidationResult:
    """验证结果"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []

class DataPipeline:
    """数据清洗管道 - 质量检查、格式校验、数据标准化
    
    支持：
    1. 数据验证（类型、范围、格式）
    2. 数据清洗（去重、缺失值处理）
    3. 数据标准化（格式统一、编码转换）
    4. 质量评分
    """
    
    # 有效的批次类型
    VALID_BATCHES = ['本科一批', '本科二批', '本科批', '专科批', '提前批']
    
    # 有效的科目类型
    VALID_SUBJECTS = ['文科', '理科', '综合']
    
    # 分数范围
    MIN_SCORE = 0
    MAX_SCORE = 750
    
    # 年份范围
    MIN_YEAR = 2010
    MAX_YEAR = 2030
    
    def __init__(self, log_level: int = logging.INFO):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        
        # 验证方法映射
        self.validators: Dict[DataType, Callable] = {
            DataType.SCORE: self.validate_score_data,
            DataType.RANK: self.validate_rank_data,
            DataType.UNIVERSITY: self.validate_university_data,
            DataType.MAJOR: self.validate_major_data,
        }
    
    def validate_score_data(self, data: Dict[str, Any]) -> ValidationResult:
        """验证分数线数据"""
        errors = []
        warnings = []
        
        # 必需字段检查
        required_fields = ['province', 'year', 'batch', 'score']
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")
        
        # 分数范围检查
        if 'score' in data:
            score = data['score']
            if not isinstance(score, (int, float)):
                errors.append(f"Score must be numeric, got {type(score)}")
            elif score < self.MIN_SCORE or score > self.MAX_SCORE:
                errors.append(f"Score {score} out of range [{self.MIN_SCORE}, {self.MAX_SCORE}]")
        
        # 年份检查
        if 'year' in data:
            year = data['year']
            if not isinstance(year, int):
                errors.append(f"Year must be integer, got {type(year)}")
            elif year < self.MIN_YEAR or year > self.MAX_YEAR:
                errors.append(f"Year {year} out of range [{self.MIN_YEAR}, {self.MAX_YEAR}]")
        
        # 批次检查
        if 'batch' in data and data['batch'] not in self.VALID_BATCHES:
            errors.append(f"Invalid batch: {data['batch']}. Valid: {self.VALID_BATCHES}")
        
        # 科目类型检查
        if 'subject_type' in data and data['subject_type'] not in self.VALID_SUBJECTS:
            warnings.append(f"Unknown subject_type: {data['subject_type']}")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    def validate_rank_data(self, data: Dict[str, Any]) -> ValidationResult:
        """验证一分一段表数据"""
        errors = []
        warnings = []
        
        required_fields = ['province', 'year', 'score', 'count', 'cumulative_count']
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")
        
        # 分数检查
        if 'score' in data:
            score = data['score']
            if not isinstance(score, (int, float)):
                errors.append(f"Score must be numeric, got {type(score)}")
            elif score < self.MIN_SCORE or score > self.MAX_SCORE:
                errors.append(f"Score {score} out of range")
        
        # 人数检查
        if 'count' in data:
            count = data['count']
            if not isinstance(count, int) or count < 0:
                errors.append(f"Count must be non-negative integer, got {count}")
        
        # 累计人数检查
        if 'cumulative_count' in data and 'count' in data:
            if data['cumulative_count'] < data['count']:
                errors.append("Cumulative count must be >= count")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    def validate_university_data(self, data: Dict[str, Any]) -> ValidationResult:
        """验证院校数据"""
        errors = []
        warnings = []
        
        required_fields = ['university_name', 'province', 'tier']
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")
        
        # tier 检查
        if 'tier' in data:
            tier = data['tier']
            if not isinstance(tier, int) or tier < 1 or tier > 3:
                errors.append(f"Tier must be 1-3, got {tier}")
        
        # 专业列表检查
        if 'majors' in data:
            if not isinstance(data['majors'], list):
                errors.append("Majors must be a list")
            elif len(data['majors']) == 0:
                warnings.append("University has no majors")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    def validate_major_data(self, data: Dict[str, Any]) -> ValidationResult:
        """验证专业数据"""
        errors = []
        warnings = []
        
        required_fields = ['name', 'code', 'admission_score']
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")
        
        # 分数检查
        if 'admission_score' in data:
            score = data['admission_score']
            if not isinstance(score, (int, float)):
                errors.append(f"Admission score must be numeric, got {type(score)}")
            elif score < self.MIN_SCORE or score > self.MAX_SCORE:
                errors.append(f"Admission score {score} out of range")
        
        # 招生人数检查
        if 'plan_count' in data:
            plan = data['plan_count']
            if not isinstance(plan, int) or plan < 0:
                errors.append(f"Plan count must be non-negative integer, got {plan}")
        
        # 学费检查
        if 'tuition' in data:
            tuition = data['tuition']
            if not isinstance(tuition, (int, float)) or tuition < 0:
                errors.append(f"Tuition must be non-negative, got {tuition}")
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    def validate_data(self, data: Dict[str, Any], data_type: DataType) -> ValidationResult:
        """统一验证入口"""
        validator = self.validators.get(data_type)
        if not validator:
            return ValidationResult(
                is_valid=False,
                errors=[f"Unknown data type: {data_type}"],
                warnings=[]
            )
        
        return validator(data)
    
    def validate_batch(self, data_list: List[Dict[str, Any]], data_type: DataType) -> Dict[str, Any]:
        """批量验证数据"""
        valid_items = []
        invalid_items = []
        
        for item in data_list:
            result = self.validate_data(item, data_type)
            if result.is_valid:
                valid_items.append(item)
            else:
                invalid_items.append({
                    'data': item,
                    'errors': result.errors
                })
        
        return {
            'valid': valid_items,
            'invalid': invalid_items,
            'valid_count': len(valid_items),
            'invalid_count': len(invalid_items),
            'success_rate': len(valid_items) / len(data_list) if data_list else 1.0
        }
    
    def deduplicate_data(self, data_list: List[Dict[str, Any]], key_fields: List[str]) -> List[Dict[str, Any]]:
        """根据指定字段去重"""
        seen = set()
        deduplicated = []
        
        for item in data_list:
            # 创建基于指定字段的哈希键
            key_values = tuple(str(item.get(field, '')) for field in key_fields)
            if key_values not in seen:
                seen.add(key_values)
                deduplicated.append(item)
        
        self.logger.info(f"Deduplicated: {len(data_list)} -> {len(deduplicated)} (removed {len(data_list) - len(deduplicated)})")
        return deduplicated
    
    def clean_data(self, data_list: List[Dict[str, Any]], data_type: DataType) -> List[Dict[str, Any]]:
        """完整的数据清洗流程：验证 + 去重"""
        # 1. 验证数据
        validation_result = self.validate_batch(data_list, data_type)
        
        if validation_result['invalid_count'] > 0:
            self.logger.warning(
                f"Found {validation_result['invalid_count']} invalid items "
                f"({validation_result['success_rate']:.1%} success rate)"
            )
        
        # 2. 去重
        if data_type == DataType.SCORE:
            key_fields = ['province', 'year', 'batch', 'subject_type']
        elif data_type == DataType.RANK:
            key_fields = ['province', 'year', 'score', 'subject_type']
        elif data_type == DataType.UNIVERSITY:
            key_fields = ['university_name']
        elif data_type == DataType.MAJOR:
            key_fields = ['name', 'code']
        else:
            key_fields = []
        
        cleaned = self.deduplicate_data(validation_result['valid'], key_fields)
        
        self.logger.info(f"Data cleaning complete: {len(data_list)} -> {len(cleaned)}")
        return cleaned
    
    def process_data(self, data: Dict[str, Any], data_type: str) -> Dict[str, Any]:
        """处理单条数据（兼容旧接口）"""
        try:
            dt = DataType(data_type)
        except ValueError:
            raise ValidationError(f"Unknown data type: {data_type}")
        
        result = self.validate_data(data, dt)
        if not result.is_valid:
            raise ValidationError(f"Validation failed: {', '.join(result.errors)}")
        
        return data
