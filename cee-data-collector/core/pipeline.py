# core/pipeline.py
from typing import Dict, List, Any
import logging

class DataPipeline:
    """数据清洗管道 - 质量检查、格式校验、数据标准化"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def validate_score_data(self, data: Dict[str, Any]) -> bool:
        """Validate score data format and logic"""
        # Check if score is within valid range
        if 'score' not in data:
            return False
        
        score = data['score']
        if not isinstance(score, (int, float)):
            return False
        
        if score < 0 or score > 750:  # Reasonable score range
            return False
        
        # Check if year is valid
        if 'year' in data:
            year = data['year']
            if not isinstance(year, int) or year < 2010 or year > 2030:
                return False
        
        # Check if batch is valid
        valid_batches = ['本科一批', '本科二批', '专科批', '提前批']
        if 'batch' in data and data['batch'] not in valid_batches:
            return False
        
        return True
    
    def validate_university_data(self, data: Dict[str, Any]) -> bool:
        """Validate university data format"""
        required_fields = ['code', 'name']
        for field in required_fields:
            if field not in data or not data[field]:
                return False
        return True
    
    def deduplicate_data(self, data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate data entries"""
        seen = set()
        deduplicated = []
        
        for item in data_list:
            # Create a hashable representation of the data
            item_hash = str(sorted(item.items()))
            if item_hash not in seen:
                seen.add(item_hash)
                deduplicated.append(item)
        
        return deduplicated
    
    def process_data(self, data: Dict[str, Any], data_type: str) -> Dict[str, Any]:
        """Main processing method for data"""
        validation_methods = {
            'score': self.validate_score_data,
            'university': self.validate_university_data
        }
        
        validator = validation_methods.get(data_type)
        if validator and not validator(data):
            raise ValueError(f"Invalid {data_type} data")
        
        return data