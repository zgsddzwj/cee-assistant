import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useUserStore } from '@/stores/userStore'
import { GraduationCap, Eye, EyeOff } from 'lucide-react'

function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const { setUser } = useUserStore()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    // 模拟登录延迟
    await new Promise((resolve) => setTimeout(resolve, 800))
    setUser({ id: '1', name: '张同学', email })
    setIsLoading(false)
  }

  return (
    <div className="min-h-[calc(100vh-12rem)] flex items-center justify-center py-12 px-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-14 h-14 bg-primary rounded-xl mb-4">
            <GraduationCap className="h-7 w-7 text-white" />
          </div>
          <h1 className="text-2xl font-bold">欢迎回来</h1>
          <p className="mt-2 text-muted-foreground text-sm">登录后保存您的志愿方案，随时查看</p>
        </div>

        {/* Form */}
        <div className="bg-white rounded-2xl border p-8 shadow-sm">
          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-sm font-medium mb-1.5">手机号 / 邮箱</label>
              <input
                type="text"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-2.5 border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-colors"
                placeholder="请输入手机号或邮箱"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1.5">密码</label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-4 py-2.5 border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-colors pr-10"
                  placeholder="请输入密码"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                >
                  {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
            </div>

            <div className="flex items-center justify-between text-sm">
              <label className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" className="rounded border-gray-300" />
                <span className="text-muted-foreground">记住我</span>
              </label>
              <span className="text-primary hover:underline cursor-pointer">忘记密码？</span>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-3 bg-primary text-white rounded-xl font-semibold hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? '登录中...' : '登录'}
            </button>
          </form>

          <div className="mt-6 text-center text-sm">
            <span className="text-muted-foreground">还没有账号？</span>{' '}
            <span className="text-primary font-medium hover:underline cursor-pointer">立即注册</span>
          </div>
        </div>

        {/* Trust Badges */}
        <div className="mt-8 flex items-center justify-center gap-6 text-xs text-muted-foreground">
          <span className="flex items-center gap-1">
            <div className="w-1.5 h-1.5 bg-green-500 rounded-full"></div>
            数据安全加密
          </span>
          <span className="flex items-center gap-1">
            <div className="w-1.5 h-1.5 bg-green-500 rounded-full"></div>
            隐私严格保护
          </span>
        </div>
      </div>
    </div>
  )
}

export default LoginPage
