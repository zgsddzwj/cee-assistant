import { Link } from 'react-router-dom'
import { MessageCircle, BarChart3, School, BookOpen, Shield, TrendingUp, ArrowRight, CheckCircle2 } from 'lucide-react'

function HomePage() {
  const features = [
    {
      icon: MessageCircle,
      title: '志愿咨询',
      description: '资深专家一对一解答，结合个人情况提供针对性建议',
      link: '/chat',
    },
    {
      icon: BarChart3,
      title: '智能推荐',
      description: '基于历年录取数据和考生信息，科学匹配适合院校',
      link: '/recommendations',
    },
    {
      icon: School,
      title: '院校查询',
      description: '全国高校信息库，招生政策、专业介绍、历年分数线',
      link: '#',
    },
  ]

  const highlights = [
    { icon: BookOpen, title: '数据全面', desc: '覆盖全国 3000+ 所高校' },
    { icon: Shield, title: '科学评估', desc: '多维度录取概率分析' },
    { icon: TrendingUp, title: '趋势预测', desc: '历年分数线走势分析' },
  ]

  return (
    <div>
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-primary via-primary to-primary/90 text-white overflow-hidden">
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiNmZmZmZmYiIGZpbGwtb3BhY2l0eT0iMC4wNSI+PGNpcmNsZSBjeD0iMzAiIGN5PSIzMCIgcj0iMiIvPjwvZz48L2c+PC9zdmc+')] opacity-20"></div>
        <div className="container-main relative py-20 md:py-28">
          <div className="max-w-3xl">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 bg-white/10 rounded-full text-sm mb-6 backdrop-blur-sm">
              <span className="w-2 h-2 bg-accent rounded-full animate-pulse"></span>
              2024 年高考志愿填报服务已开启
            </div>
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold leading-tight">
              科学填报
              <span className="text-accent"> 精准录取</span>
            </h1>
            <p className="mt-6 text-lg md:text-xl text-white/80 leading-relaxed max-w-2xl">
              基于历年招生录取数据与考生个人情况，提供科学、专业的志愿填报方案，
              助力每一位考生实现理想大学梦。
            </p>
            <div className="mt-10 flex flex-wrap gap-4">
              <Link
                to="/chat"
                className="inline-flex items-center gap-2 px-8 py-3.5 bg-accent text-white rounded-xl font-semibold hover:bg-accent/90 transition-colors shadow-lg shadow-accent/25"
              >
                开始咨询
                <ArrowRight className="h-4 w-4" />
              </Link>
              <Link
                to="/recommendations"
                className="inline-flex items-center gap-2 px-8 py-3.5 bg-white/10 text-white rounded-xl font-semibold hover:bg-white/20 transition-colors backdrop-blur-sm border border-white/20"
              >
                查看推荐方案
              </Link>
            </div>
            <div className="mt-10 flex items-center gap-6 text-sm text-white/70">
              <span className="flex items-center gap-1.5"><CheckCircle2 className="h-4 w-4 text-accent" /> 数据权威可靠</span>
              <span className="flex items-center gap-1.5"><CheckCircle2 className="h-4 w-4 text-accent" /> 方案个性定制</span>
              <span className="flex items-center gap-1.5"><CheckCircle2 className="h-4 w-4 text-accent" /> 录取概率评估</span>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Bar */}
      <section className="bg-white border-b">
        <div className="container-main py-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="text-3xl font-bold text-primary">3000+</div>
              <div className="text-sm text-muted-foreground mt-1">合作院校</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-primary">500+</div>
              <div className="text-sm text-muted-foreground mt-1">专业覆盖</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-primary">10万+</div>
              <div className="text-sm text-muted-foreground mt-1">服务考生</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-primary">95%</div>
              <div className="text-sm text-muted-foreground mt-1">满意度</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container-main py-16 md:py-20">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold">核心服务</h2>
          <p className="mt-3 text-muted-foreground">全方位助力高考志愿填报</p>
        </div>
        <div className="grid md:grid-cols-3 gap-6">
          {features.map((f) => (
            <Link
              key={f.title}
              to={f.link}
              className="group bg-white p-8 rounded-2xl border hover:border-primary/30 hover:shadow-xl hover:shadow-primary/5 transition-all duration-300"
            >
              <div className="w-14 h-14 bg-primary/5 rounded-xl flex items-center justify-center mb-5 group-hover:bg-primary group-hover:scale-110 transition-all duration-300">
                <f.icon className="h-7 w-7 text-primary group-hover:text-white transition-colors" />
              </div>
              <h3 className="text-xl font-semibold group-hover:text-primary transition-colors">
                {f.title}
              </h3>
              <p className="mt-2 text-muted-foreground leading-relaxed">{f.description}</p>
              <div className="mt-4 inline-flex items-center gap-1 text-sm font-medium text-primary opacity-0 group-hover:opacity-100 transition-opacity">
                了解更多 <ArrowRight className="h-3.5 w-3.5" />
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* Highlights Section */}
      <section className="bg-white border-y">
        <div className="container-main py-16">
          <div className="grid md:grid-cols-3 gap-8">
            {highlights.map((h) => (
              <div key={h.title} className="flex items-start gap-4">
                <div className="w-12 h-12 bg-accent/10 rounded-xl flex items-center justify-center flex-shrink-0">
                  <h.icon className="h-6 w-6 text-accent" />
                </div>
                <div>
                  <h3 className="font-semibold text-lg">{h.title}</h3>
                  <p className="mt-1 text-muted-foreground text-sm">{h.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container-main py-16 md:py-20">
        <div className="bg-primary rounded-3xl p-8 md:p-12 text-center text-white">
          <h2 className="text-3xl font-bold">开启您的志愿填报之旅</h2>
          <p className="mt-3 text-white/80 max-w-xl mx-auto">
            输入您的分数和意向，获取个性化的院校推荐方案
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-4">
            <Link
              to="/chat"
              className="inline-flex items-center gap-2 px-8 py-3.5 bg-accent text-white rounded-xl font-semibold hover:bg-accent/90 transition-colors"
            >
              免费咨询
              <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}

export default HomePage
