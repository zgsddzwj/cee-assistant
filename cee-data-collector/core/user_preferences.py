# core/user_preferences.py
"""用户偏好配置管理

支持：
1. 考生信息配置
2. 偏好设置
3. 历史查询记录
4. 配置文件持久化
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import json
import os

@dataclass
class UserProfile:
    """用户档案"""
    user_id: str
    name: str = ""
    province: str = ""
    subject_type: str = ""
    score: Optional[int] = None
    rank: Optional[int] = None
    interests: List[str] = None
    career_plan: str = ""
    preferred_provinces: List[str] = None
    preferred_categories: List[str] = None
    
    def __post_init__(self):
        if self.interests is None:
            self.interests = []
        if self.preferred_provinces is None:
            self.preferred_provinces = []
        if self.preferred_categories is None:
            self.preferred_categories = []

class UserPreferenceManager:
    """用户偏好管理器"""
    
    def __init__(self, config_dir: str = './config'):
        self.config_dir = config_dir
        os.makedirs(config_dir, exist_ok=True)
        self._profiles: Dict[str, UserProfile] = {}
    
    def save_profile(self, profile: UserProfile) -> str:
        """保存用户档案"""
        filepath = os.path.join(self.config_dir, f"{profile.user_id}.json")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(asdict(profile), f, ensure_ascii=False, indent=2)
        
        self._profiles[profile.user_id] = profile
        return filepath
    
    def load_profile(self, user_id: str) -> Optional[UserProfile]:
        """加载用户档案"""
        if user_id in self._profiles:
            return self._profiles[user_id]
        
        filepath = os.path.join(self.config_dir, f"{user_id}.json")
        if not os.path.exists(filepath):
            return None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        profile = UserProfile(**data)
        self._profiles[user_id] = profile
        return profile
    
    def update_preferences(self, user_id: str, **kwargs) -> bool:
        """更新用户偏好"""
        profile = self.load_profile(user_id)
        if not profile:
            return False
        
        for key, value in kwargs.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
        
        self.save_profile(profile)
        return True
    
    def get_query_history(self, user_id: str) -> List[Dict]:
        """获取查询历史"""
        history_file = os.path.join(self.config_dir, f"{user_id}_history.json")
        if not os.path.exists(history_file):
            return []
        
        with open(history_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def add_query_history(self, user_id: str, query: Dict):
        """添加查询记录"""
        history = self.get_query_history(user_id)
        history.append({
            "timestamp": __import__('datetime').datetime.now().isoformat(),
            "query": query
        })
        
        # 只保留最近50条
        history = history[-50:]
        
        history_file = os.path.join(self.config_dir, f"{user_id}_history.json")
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
