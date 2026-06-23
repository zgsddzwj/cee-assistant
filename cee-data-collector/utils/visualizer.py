# utils/visualizer.py
"""数据可视化 - 生成图表和报表

支持：
1. 分数线趋势图
2. 院校分布图
3. 专业热度图
4. 分数段分布图
"""

from typing import Dict, List, Any, Optional
import json
import os
from datetime import datetime

class DataVisualizer:
    """数据可视化器"""
    
    def __init__(self, output_dir: str = './reports'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_score_trend_report(self, scores: List[Dict], province: str) -> str:
        """生成分数线趋势报表（HTML）"""
        # 按年份和批次分组
        data_by_batch = {}
        for score in scores:
            if score.get('province') == province:
                batch = score.get('batch', '')
                year = score.get('year', '')
                if batch not in data_by_batch:
                    data_by_batch[batch] = {}
                data_by_batch[batch][year] = score.get('score', 0)
        
        # 生成HTML
        html = self._generate_html_report(
            title=f"{province} 分数线趋势",
            data=data_by_batch,
            chart_type="line"
        )
        
        filepath = os.path.join(self.output_dir, f"score_trend_{province}.html")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return filepath
    
    def generate_university_distribution(self, universities: List[Dict]) -> str:
        """生成院校分布报表"""
        # 按省份统计
        province_stats = {}
        tier_stats = {1: 0, 2: 0, 3: 0}
        
        for uni in universities:
            province = uni.get('province', '未知')
            province_stats[province] = province_stats.get(province, 0) + 1
            tier = uni.get('tier', 3)
            tier_stats[tier] = tier_stats.get(tier, 0) + 1
        
        report = {
            "title": "院校分布统计",
            "generated_at": datetime.now().isoformat(),
            "province_distribution": province_stats,
            "tier_distribution": tier_stats,
            "total": len(universities)
        }
        
        filepath = os.path.join(self.output_dir, "university_distribution.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return filepath
    
    def _generate_html_report(self, title: str, data: Dict, chart_type: str = "line") -> str:
        """生成HTML报表"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        .chart {{ width: 100%; height: 400px; margin: 20px 0; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <p>生成时间: {datetime.now().isoformat()}</p>
    <div class="chart">
        <table>
            <tr><th>批次</th><th>年份</th><th>分数</th></tr>
            {self._generate_table_rows(data)}
        </table>
    </div>
</body>
</html>
        """
    
    def _generate_table_rows(self, data: Dict) -> str:
        """生成表格行"""
        rows = []
        for batch, years in data.items():
            for year, score in years.items():
                rows.append(f"<tr><td>{batch}</td><td>{year}</td><td>{score}</td></tr>")
        return "\n".join(rows)
