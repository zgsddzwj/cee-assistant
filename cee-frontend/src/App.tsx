import { BrowserRouter, Routes, Route } from 'react-router-dom'
import AppLayout from './components/layout/AppLayout'
import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import ChatPage from './pages/ChatPage'
import RecommendationPage from './pages/RecommendationPage'

function App() {
  return (
    <BrowserRouter>
      <AppLayout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/recommendations" element={<RecommendationPage />} />
        </Routes>
      </AppLayout>
    </BrowserRouter>
  )
}

export default App
