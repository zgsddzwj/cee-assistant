import { useState } from 'react'
import type { Recommendation } from '@/types/recommendation'
import RecommendationCard from '@/components/recommendation/RecommendationCard'
import { Filter, SlidersHorizontal, GraduationCap } from 'lucide-react'

function RecommendationPage() {
  const [activeTab, setActiveTab] = useState<'冲刺' | '稳妥' | '保底'>('稳妥')

  const recommendations: Recommendation[] = [
    {
      college: { id: '1', name: '北京邮电大学', location: '北京市', tags: ['211', '双一流'] },
      major: '计算机科学与技术',
      probability: 35,
      category: '冲刺',
      previousScores: [628, 631, 625],
    },
    {
      college: { id: '2', name: '西安电子科技大学', location: '陕西西安', tags: ['211', '双一流'] },
      major: '软件工程',
      probability: 65,
      category: '稳妥',
      previousScores: [608, 612, 605],
    },
    {
      college: { id: '3', name: '重庆邮电大学', location: '重庆市', tags: ['省重点'] },
      major: '计算机科学与技术',
      probability: 88,
      category: '保底',
      previousScores: [585, 589, 582],
    },
    {
      college: { id: '4', name: '杭州电子科技大学', location: '浙江杭州', tags: ['省重点'] },
      major: '电子信息工程',
      probability: 72,
      category: '稳妥',
      previousScores: [598, 602, 595],
    },
    {
      college: { id: '5', name: '桂林电子科技大学', location: '广西桂林', tags: ['省重点'] },
      major: '计算机类',
      probability: 92,
      category: '保底',
      previousScores: [565, 570, 562],
    },
  ]

  const filtered = recommendations.filter((r) => r.category === activeTab)

  const tabs = [
    { key: '冲刺' as const, label: '冲刺院校', desc: '录取概率 30-50%', color: 'text-amber-600', bgColor: 'bg-amber-50', borderColor: 'border-amber-200' },
    { key: '稳妥' as const, label: '稳妥院校', desc: '录取概率 50-80%', color: 'text-sky-600', bgColor: 'bg-sky-50', borderColor: 'border-sky-200' },
    { key: '保底' as const, label: '保底院校', desc: '录取概率 80%+', color: 'text-emerald-600', bgColor: 'bg-emerald-50', borderColor: 'border-emerald-200' },
  ]

  return (
    <div className="container-main py-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-10 h-10 bg-primary/10 rounded-xl flex items-center justify-center">
            <GraduationCap className="h-5 w-5 text-primary" />
          </div>
          <div>
            <h1 className="text-2xl font-bold">志愿推荐方案</h1>
            <p className="text-sm text-muted-foreground">
              基于您的分数 600分 / 位次 15000 / 北京市 / 理科
            </p>
          </div>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
        <div className="flex gap-2">
          {tabs.map((tab) => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`px-5 py-2.5 rounded-xl text-sm font-medium transition-all ${
                activeTab === tab.key
                  ? `${tab.bgColor} ${tab.color} ${tab.borderColor} border-2 shadow-sm`
                  : 'bg-white border text-muted-foreground hover:text-foreground hover:border-gray-300'
              }`}
            >
              <div className="font-semibold">{tab.label}</div>
              <div className="text-[10px] opacity-70 mt-0.5">{tab.desc}</div>
            </button>
          ))}
        </div>
        <button className="flex items-center gap-2 px-4 py-2.5 bg-white border rounded-xl text-sm text-muted-foreground hover:text-foreground transition-colors">
          <SlidersHorizontal className="h-4 w-4" />
          筛选条件
        </button>
      </div>

      {/* Results Count */}
      <div className="flex items-center gap-2 mb-4 text-sm text-muted-foreground">
        <Filter className="h-4 w-4" />
        <span>共找到 {filtered.length} 所{activeTab}院校</span>
      </div>

      {/* Cards */}
      <div className="space-y-4">
        {filtered.map((rec) => (
          <RecommendationCard key={rec.college.id} rec={rec} />
        ))}
      </div>

      {/* Empty State */}
      {filtered.length === 0 && (
        <div className="text-center py-16">
          <div className="w-16 h-16 bg-muted rounded-2xl flex items-center justify-center mx-auto mb-4">
            <Filter className="h-8 w-8 text-muted-foreground" />
          </div>
          <h3 className="font-semibold text-lg">暂无{activeTab}院校</h3>
          <p className="text-muted-foreground text-sm mt-1">建议调整筛选条件或分数预期</p>
        </div>
      )}

      {/* Tips */}
      <div className="mt-8 p-4 bg-amber-50 border border-amber-200 rounded-xl">
        <h4 className="font-semibold text-amber-800 text-sm mb-1">填报建议</h4>
        <p className="text-amber-700 text-sm leading-relaxed">
          建议按照「冲稳保」比例 2:5:3 进行填报，即 2 所冲刺 + 5 所稳妥 + 3 所保底，
          确保既有理想追求又有稳妥保障。具体方案可咨询专业顾问。
        </p>
      </div>
    </div>
  )
}

export default RecommendationPage
