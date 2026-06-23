# services/analytics_service.py
"""数据分析服务 - 分数线趋势和统计分析

支持：
1. 历年分数线趋势
2. 分数段分布
3. 院校录取难度排名
4. 专业热度分析
"""

from typing import Dict, List, Any, Optional
from collections import defaultdict
import statistics

class AnalyticsService:
    """数据分析服务"""
    
    def __init__(self, scores: List[Dict] = None, universities: List[Dict] = None):
        self.scores = scores or []
        self.universities = universities or []
    
    def analyze_score_trend(self, province: str, batch: str, years: List[int]) -> Dict[str, Any]:
        """分析分数线趋势"""
        trend_data = []
        
        for year in years:
            year_scores = [
                s for s in self.scores 
                if s.get('province') == province 
                and s.get('batch') == batch 
                and s.get('year') == year
            ]
            
            if year_scores:
                avg_score = statistics.mean(s.get('score', 0) for s in year_scores)
                trend_data.append({
                    "year": year,
                    "avg_score": round(avg_score, 1),
                    "count": len(year_scores)
                })
        
        # 计算变化趋势
        if len(trend_data) >= 2:
            changes = []
            for i in range(1, len(trend_data)):
                change = trend_data[i]['avg_score'] - trend_data[i-1]['avg_score']
                changes.append(change)
            
            avg_change = statistics.mean(changes) if changes else 0
            trend = "上升" if avg_change > 0 else "下降" if avg_change < 0 else "稳定"
        else:
            avg_change = 0
            trend = "未知"
        
        return {
            "province": province,
            "batch": batch,
            "years": years,
            "trend": trend,
            "avg_change": round(avg_change, 1),
            "data": trend_data
        }
    
    def analyze_score_distribution(self, scores: List[int], bins: List[int] = None) -> Dict[str, int]:
        """分析分数段分布"""
        if bins is None:
            bins = [300, 400, 450, 500, 550, 600, 650, 700, 750]
        
        distribution = defaultdict(int)
        
        for score in scores:
            for i in range(len(bins) - 1):
                if bins[i] <= score < bins[i + 1]:
                    distribution[f"{bins[i]}-{bins[i+1]}"] += 1
                    break
            else:
                if score >= bins[-1]:
                    distribution[f"{bins[-1]}+"] += 1
        
        return dict(distribution)
    
    def analyze_university_difficulty(self) -> List[Dict[str, Any]]:
        """分析院校录取难度排名"""
        difficulty_list = []
        
        for uni in self.universities:
            majors = uni.get('majors', [])
            if not majors:
                continue
            
            scores = [m.get('admission_score', 0) for m in majors]
            avg_score = statistics.mean(scores) if scores else 0
            
            difficulty_list.append({
                "university_name": uni.get('university_name', ''),
                "province": uni.get('province', ''),
                "tier": uni.get('tier', 3),
                "avg_score": round(avg_score, 1),
                "max_score": max(scores) if scores else 0,
                "min_score": min(scores) if scores else 0,
                "major_count": len(majors)
            })
        
        # 按平均分数排序
        difficulty_list.sort(key=lambda x: x['avg_score'], reverse=True)
        
        return difficulty_list
    
    def analyze_major_popularity(self) -> List[Dict[str, Any]]:
        """分析专业热度"""
        major_stats = defaultdict(lambda: {"count": 0, "total_score": 0, "hot_count": 0})
        
        for uni in self.universities:
            for major in uni.get('majors', []):
                name = major.get('name', '')
                score = major.get('admission_score', 0)
                is_hot = major.get('hot', False)
                
                major_stats[name]['count'] += 1
                major_stats[name]['total_score'] += score
                if is_hot:
                    major_stats[name]['hot_count'] += 1
        
        # 计算平均分和热度
        popularity_list = []
        for name, stats in major_stats.items():
            avg_score = stats['total_score'] / stats['count'] if stats['count'] > 0 else 0
            hot_rate = stats['hot_count'] / stats['count'] if stats['count'] > 0 else 0
            
            popularity_list.append({
                "major_name": name,
                "university_count": stats['count'],
                "avg_score": round(avg_score, 1),
                "hot_rate": round(hot_rate, 2),
                "is_popular": hot_rate > 0.5
            })
        
        # 按热度排序
        popularity_list.sort(key=lambda x: x['hot_rate'], reverse=True)
        
        return popularity_list
