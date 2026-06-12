import { Link, useLocation } from 'react-router-dom'
import { useUserStore } from '@/stores/userStore'
import { GraduationCap, User, LogOut, Menu, X } from 'lucide-react'
import { useState } from 'react'

function NavHeader() {
  const { isLoggedIn, user, logout } = useUserStore()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const location = useLocation()

  const navItems = [
    { path: '/chat', label: '志愿咨询' },
    { path: '/recommendations', label: '智能推荐' },
  ]

  const isActive = (path: string) => location.pathname === path

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-white/95 backdrop-blur-sm shadow-sm">
      <div className="container-main">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2.5">
            <div className="w-9 h-9 bg-primary rounded-lg flex items-center justify-center">
              <GraduationCap className="h-5 w-5 text-white" />
            </div>
            <div className="flex flex-col">
              <span className="text-lg font-bold text-foreground leading-tight">高考志愿通</span>
              <span className="text-[10px] text-muted-foreground leading-tight tracking-wider">专业志愿填报服务平台</span>
            </div>
          </Link>

          {/* Desktop Nav */}
          <nav className="hidden md:flex items-center gap-1">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  isActive(item.path)
                    ? 'bg-primary/10 text-primary'
                    : 'text-muted-foreground hover:text-foreground hover:bg-muted'
                }`}
              >
                {item.label}
              </Link>
            ))}
          </nav>

          {/* User Section */}
          <div className="hidden md:flex items-center gap-3">
            {isLoggedIn ? (
              <div className="flex items-center gap-3">
                <div className="flex items-center gap-2 px-3 py-1.5 bg-muted rounded-full">
                  <div className="w-6 h-6 bg-primary/10 rounded-full flex items-center justify-center">
                    <User className="h-3.5 w-3.5 text-primary" />
                  </div>
                  <span className="text-sm font-medium">{user?.name}</span>
                </div>
                <button
                  onClick={logout}
                  className="p-2 text-muted-foreground hover:text-destructive hover:bg-destructive/10 rounded-lg transition-colors"
                  title="退出登录"
                >
                  <LogOut className="h-4 w-4" />
                </button>
              </div>
            ) : (
              <Link
                to="/login"
                className="px-5 py-2 bg-primary text-white text-sm font-medium rounded-lg hover:bg-primary/90 transition-colors"
              >
                登录 / 注册
              </Link>
            )}
          </div>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden p-2 text-muted-foreground hover:text-foreground"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden py-4 border-t space-y-2">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`block px-4 py-2 rounded-lg text-sm font-medium ${
                  isActive(item.path) ? 'bg-primary/10 text-primary' : 'text-muted-foreground'
                }`}
                onClick={() => setMobileMenuOpen(false)}
              >
                {item.label}
              </Link>
            ))}
            {!isLoggedIn && (
              <Link
                to="/login"
                className="block px-4 py-2 bg-primary text-white text-sm font-medium rounded-lg text-center"
                onClick={() => setMobileMenuOpen(false)}
              >
                登录 / 注册
              </Link>
            )}
          </div>
        )}
      </div>
    </header>
  )
}

export default NavHeader
