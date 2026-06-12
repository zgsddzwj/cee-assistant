# data_generator.py
"""数据生成器 - 生成模拟的高考数据供开发和测试使用

使用方法:
    python data_generator.py --all          # 生成所有数据
    python data_generator.py --scores       # 只生成分数线
    python data_generator.py --universities  # 只生成院校数据
    python data_generator.py --year 2024    # 指定年份
"""

import json
import os
import random
from datetime import datetime
from typing import Dict, List

# 全国31省市
PROVINCES = [
    'beijing', 'shanghai', 'tianjin', 'chongqing',
    'hebei', 'shanxi', 'neimenggu', 'liaoning', 'jilin', 'heilongjiang',
    'jiangsu', 'zhejiang', 'anhui', 'fujian', 'jiangxi', 'shandong',
    'henan', 'hubei', 'hunan', 'guangdong', 'guangxi', 'hainan',
    'sichuan', 'guizhou', 'yunnan', 'xizang', 'shanxi2', 'gansu', 'qinghai', 'ningxia', 'xinjiang'
]

PROVINCE_NAMES = {
    'beijing': '北京', 'shanghai': '上海', 'tianjin': '天津', 'chongqing': '重庆',
    'hebei': '河北', 'shanxi': '山西', 'neimenggu': '内蒙古', 'liaoning': '辽宁', 
    'jilin': '吉林', 'heilongjiang': '黑龙江',
    'jiangsu': '江苏', 'zhejiang': '浙江', 'anhui': '安徽', 'fujian': '福建', 
    'jiangxi': '江西', 'shandong': '山东',
    'henan': '河南', 'hubei': '湖北', 'hunan': '湖南', 'guangdong': '广东', 
    'guangxi': '广西', 'hainan': '海南',
    'sichuan': '四川', 'guizhou': '贵州', 'yunnan': '云南', 'xizang': '西藏', 
    'shanxi2': '陕西', 'gansu': '甘肃', 'qinghai': '青海', 'ningxia': '宁夏', 'xinjiang': '新疆'
}

BATCHES = ['本科一批', '本科二批', '本科批', '专科批', '提前批']

SUBJECT_TYPES = ['文科', '理科', '综合']


def generate_score_data(province: str, year: int = 2024) -> List[Dict]:
    """生成分数线数据"""
    # 基于省份生成合理的基准分数
    base_scores = {
        'beijing': 550, 'shanghai': 545, 'tianjin': 540,
        'jiangsu': 535, 'zhejiang': 530, 'shandong': 525,
        'guangdong': 520, 'fujian': 515, 'hubei': 510,
        'sichuan': 505, 'hunan': 500, 'henan': 495,
        'anhui': 490, 'jiangxi': 485, 'hebei': 480,
        'shanxi': 475, 'shanxi2': 470, 'liaoning': 465,
        'jilin': 460, 'heilongjiang': 455, 'chongqing': 450,
    }
    
    base = base_scores.get(province, 500)
    scores = []
    
    for batch in BATCHES:
        if '一批' in batch:
            score = base + random.randint(20, 40)
        elif '二批' in batch:
            score = base - random.randint(10, 30)
        elif '专科' in batch:
            score = base - random.randint(80, 120)
        elif '提前批' in batch:
            score = base + random.randint(30, 60)
        else:
            score = base
        
        for subject in SUBJECT_TYPES:
            scores.append({
                'province': province,
                'province_name': PROVINCE_NAMES.get(province, province),
                'year': year,
                'batch': batch,
                'score': score + random.randint(-5, 5),
                'subject_type': subject,
                'updated_at': datetime.now().isoformat()
            })
    
    return scores


def generate_rank_data(province: str, year: int = 2024) -> List[Dict]:
    """生成一分一段表数据"""
    ranks = []
    
    for score in range(750, 200, -1):
        # 分数越高，人数越少
        if score >= 700:
            count = random.randint(1, 10)
        elif score >= 650:
            count = random.randint(10, 50)
        elif score >= 600:
            count = random.randint(50, 200)
        elif score >= 550:
            count = random.randint(200, 1000)
        elif score >= 500:
            count = random.randint(1000, 3000)
        elif score >= 450:
            count = random.randint(3000, 8000)
        elif score >= 400:
            count = random.randint(8000, 15000)
        else:
            count = random.randint(15000, 30000)
        
        for subject in SUBJECT_TYPES:
            ranks.append({
                'province': province,
                'province_name': PROVINCE_NAMES.get(province, province),
                'year': year,
                'score': score,
                'count': count,
                'cumulative_count': 0,  # 稍后计算
                'subject_type': subject,
                'updated_at': datetime.now().isoformat()
            })
    
    # 计算累计人数
    for subject in SUBJECT_TYPES:
        subject_ranks = [r for r in ranks if r['subject_type'] == subject]
        subject_ranks.sort(key=lambda x: x['score'], reverse=True)
        cumulative = 0
        for rank in subject_ranks:
            cumulative += rank['count']
            rank['cumulative_count'] = cumulative
    
    return ranks


def generate_university_data(uni_id: int, year: int = 2024) -> Dict:
    """生成院校数据"""
    universities_pool = [
        {'name': '清华大学', 'province': '北京', 'tier': 1},
        {'name': '北京大学', 'province': '北京', 'tier': 1},
        {'name': '复旦大学', 'province': '上海', 'tier': 1},
        {'name': '上海交通大学', 'province': '上海', 'tier': 1},
        {'name': '浙江大学', 'province': '浙江', 'tier': 1},
        {'name': '南京大学', 'province': '江苏', 'tier': 1},
        {'name': '中国科学技术大学', 'province': '安徽', 'tier': 1},
        {'name': '华中科技大学', 'province': '湖北', 'tier': 1},
        {'name': '武汉大学', 'province': '湖北', 'tier': 1},
        {'name': '西安交通大学', 'province': '陕西', 'tier': 1},
        {'name': '四川大学', 'province': '四川', 'tier': 2},
        {'name': '中山大学', 'province': '广东', 'tier': 1},
        {'name': '哈尔滨工业大学', 'province': '黑龙江', 'tier': 1},
        {'name': '北京航空航天大学', 'province': '北京', 'tier': 1},
        {'name': '同济大学', 'province': '上海', 'tier': 1},
        {'name': '南开大学', 'province': '天津', 'tier': 1},
        {'name': '山东大学', 'province': '山东', 'tier': 2},
        {'name': '厦门大学', 'province': '福建', 'tier': 2},
        {'name': '天津大学', 'province': '天津', 'tier': 1},
        {'name': '华东师范大学', 'province': '上海', 'tier': 2},
    ]
    
    if uni_id >= len(universities_pool):
        # 生成随机院校
        uni = {
            'name': f'大学{uni_id}',
            'province': random.choice(list(PROVINCE_NAMES.values())),
            'tier': random.choice([2, 3])
        }
    else:
        uni = universities_pool[uni_id]
    
    # 根据 tier 确定基础分数
    if uni['tier'] == 1:
        base_score = random.randint(620, 680)
    elif uni['tier'] == 2:
        base_score = random.randint(580, 640)
    else:
        base_score = random.randint(520, 600)
    
    # 常见专业
    majors_pool = [
        {'name': '计算机科学与技术', 'code': '080901', 'category': '工学', 'hot': True},
        {'name': '软件工程', 'code': '080902', 'category': '工学', 'hot': True},
        {'name': '人工智能', 'code': '080717', 'category': '工学', 'hot': True},
        {'name': '电子信息工程', 'code': '080701', 'category': '工学', 'hot': True},
        {'name': '金融学', 'code': '020301', 'category': '经济学', 'hot': True},
        {'name': '临床医学', 'code': '100201', 'category': '医学', 'hot': True},
        {'name': '法学', 'code': '030101', 'category': '法学', 'hot': True},
        {'name': '工商管理', 'code': '120201', 'category': '管理学', 'hot': True},
        {'name': '会计学', 'code': '120203', 'category': '管理学', 'hot': True},
        {'name': '英语', 'code': '050201', 'category': '文学', 'hot': True},
        {'name': '数学与应用数学', 'code': '070101', 'category': '理学', 'hot': False},
        {'name': '物理学', 'code': '070201', 'category': '理学', 'hot': False},
        {'name': '化学', 'code': '070301', 'category': '理学', 'hot': False},
        {'name': '汉语言文学', 'code': '050101', 'category': '文学', 'hot': False},
        {'name': '土木工程', 'code': '081001', 'category': '工学', 'hot': False},
        {'name': '机械工程', 'code': '080201', 'category': '工学', 'hot': False},
    ]
    
    num_majors = random.randint(8, 16)
    selected_majors = random.sample(majors_pool, min(num_majors, len(majors_pool)))
    
    majors = []
    for major in selected_majors:
        if major['hot']:
            score_offset = random.randint(0, 30)
        else:
            score_offset = random.randint(-20, 10)
        
        admission_score = base_score + score_offset
        
        majors.append({
            'name': major['name'],
            'code': major['code'],
            'category': major['category'],
            'admission_score': admission_score,
            'plan_count': random.randint(30, 200),
            'tuition': random.choice([5000, 5500, 6000, 8000, 10000]),
            'duration': 4 if major['category'] != '医学' else 5,
            'hot': major['hot'],
        })
    
    majors.sort(key=lambda x: x['admission_score'], reverse=True)
    
    return {
        'university_id': uni_id,
        'university_name': uni['name'],
        'province': uni['province'],
        'tier': uni['tier'],
        'year': year,
        'majors': majors,
        'total_plan': sum(m['plan_count'] for m in majors),
        'updated_at': datetime.now().isoformat()
    }


def generate_all_data(year: int = 2024, data_dir: str = './data') -> Dict:
    """生成所有模拟数据"""
    os.makedirs(data_dir, exist_ok=True)
    
    print(f"=== Generating Mock Data for {year} ===\n")
    
    # 1. 生成分数线数据
    print("Generating score lines...")
    all_scores = []
    for province in PROVINCES:
        scores = generate_score_data(province, year)
        all_scores.extend(scores)
    
    scores_file = os.path.join(data_dir, f'all_scores_{year}.json')
    with open(scores_file, 'w', encoding='utf-8') as f:
        json.dump(all_scores, f, ensure_ascii=False, indent=2)
    print(f"  Score lines: {len(all_scores)} records -> {scores_file}")
    
    # 2. 生成一分一段表
    print("\nGenerating rank data...")
    all_ranks = []
    for province in PROVINCES:
        ranks = generate_rank_data(province, year)
        all_ranks.extend(ranks)
    
    ranks_file = os.path.join(data_dir, f'all_ranks_{year}.json')
    with open(ranks_file, 'w', encoding='utf-8') as f:
        json.dump(all_ranks, f, ensure_ascii=False, indent=2)
    print(f"  Rank entries: {len(all_ranks)} records -> {ranks_file}")
    
    # 3. 生成院校数据
    print("\nGenerating university data...")
    all_universities = []
    for i in range(50):  # 生成50所院校
        uni = generate_university_data(i, year)
        all_universities.append(uni)
    
    universities_file = os.path.join(data_dir, f'all_universities_{year}.json')
    with open(universities_file, 'w', encoding='utf-8') as f:
        json.dump(all_universities, f, ensure_ascii=False, indent=2)
    print(f"  Universities: {len(all_universities)} -> {universities_file}")
    
    total_majors = sum(len(u['majors']) for u in all_universities)
    print(f"  Total majors: {total_majors}")
    
    # 4. 生成汇总文件
    summary = {
        'year': year,
        'generated_at': datetime.now().isoformat(),
        'statistics': {
            'provinces': len(PROVINCES),
            'score_records': len(all_scores),
            'rank_records': len(all_ranks),
            'universities': len(all_universities),
            'majors': total_majors,
        },
        'files': {
            'scores': scores_file,
            'ranks': ranks_file,
            'universities': universities_file,
        }
    }
    
    summary_file = os.path.join(data_dir, f'summary_{year}.json')
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"\nSummary: {summary_file}")
    
    return summary


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='CEE Data Generator')
    parser.add_argument('--year', type=int, default=2024, help='Year to generate data for')
    parser.add_argument('--dir', type=str, default='./data', help='Output directory')
    parser.add_argument('--all', action='store_true', help='Generate all data')
    
    args = parser.parse_args()
    
    if args.all or True:  # 默认生成所有
        summary = generate_all_data(args.year, args.dir)
        print("\n=== Data Generation Complete ===")
        print(json.dumps(summary['statistics'], ensure_ascii=False, indent=2))
