import { GraduationCap } from 'lucide-react'

function Footer() {
  return (
    <footer className="border-t bg-white mt-auto">
      <div className="container-main py-8">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2 text-muted-foreground">
            <GraduationCap className="h-5 w-5" />
            <span className="text-sm">高考志愿通 · 专业志愿填报服务平台</span>
          </div>
          <div className="flex items-center gap-6 text-sm text-muted-foreground">
            <span>关于我们</span>
            <span>使用指南</span>
            <span>隐私政策</span>
            <span>联系客服</span>
          </div>
        </div>
        <div className="mt-4 pt-4 border-t text-center text-xs text-muted-foreground">
          © 2024 高考志愿通. 数据仅供参考，请以各省教育考试院公布信息为准.
        </div>
      </div>
    </footer>
  )
}

export default Footer
