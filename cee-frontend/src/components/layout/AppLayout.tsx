import NavHeader from './NavHeader'
import Footer from './Footer'

function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-background flex flex-col">
      <NavHeader />
      <main className="flex-1">{children}</main>
      <Footer />
    </div>
  )
}

export default AppLayout
