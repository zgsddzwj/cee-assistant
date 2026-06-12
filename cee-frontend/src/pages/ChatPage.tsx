import { useChatStore } from '@/stores/chatStore'
import ChatMessage from '@/components/chat/ChatMessage'
import ChatInput from '@/components/chat/ChatInput'
import { GraduationCap, Sparkles } from 'lucide-react'

function ChatPage() {
  const { messages, isLoading, addMessage, setLoading } = useChatStore()

  const handleSend = async (text: string) => {
    const userMsg = {
      id: Date.now().toString(),
      role: 'user' as const,
      content: text,
      timestamp: new Date().toISOString(),
    }
    addMessage(userMsg)
    setLoading(true)

    // Mock AI response
    setTimeout(() => {
      const responses = [
        `根据您提供的信息，我建议您可以关注以下几所院校：\n\n1. 北京邮电大学 - 计算机类（冲刺）\n2. 西安电子科技大学 - 软件工程（稳妥）\n3. 重庆邮电大学 - 计算机科学与技术（保底）\n\n请问您有特别倾向的城市或专业方向吗？`,
        `您的分数和位次很有竞争力。从历年数据来看，您可以重点考虑 211 院校中的计算机相关专业。\n\n需要我为您详细分析某所学校的录取概率吗？`,
        `收到您的问题。填报志愿时建议采用「冲稳保」策略：\n\n• 冲刺：录取概率 30-50% 的院校\n• 稳妥：录取概率 50-80% 的院校\n• 保底：录取概率 80% 以上的院校\n\n我可以根据您的具体情况生成推荐方案。`,
      ]
      const randomResponse = responses[Math.floor(Math.random() * responses.length)]
      const aiMsg = {
        id: (Date.now() + 1).toString(),
        role: 'assistant' as const,
        content: randomResponse,
        timestamp: new Date().toISOString(),
      }
      addMessage(aiMsg)
      setLoading(false)
    }, 1200)
  }

  return (
    <div className="container-main h-[calc(100vh-8rem)] flex flex-col">
      {/* Header */}
      <div className="flex items-center gap-3 py-4 border-b">
        <div className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center">
          <GraduationCap className="h-5 w-5 text-white" />
        </div>
        <div>
          <h2 className="font-semibold">志愿填报咨询</h2>
          <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
            <span className="w-1.5 h-1.5 bg-green-500 rounded-full"></span>
            在线服务中
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto py-6 space-y-6">
        {messages.length === 0 && (
          <div className="h-full flex flex-col items-center justify-center text-center px-4">
            <div className="w-16 h-16 bg-primary/5 rounded-2xl flex items-center justify-center mb-5">
              <Sparkles className="h-8 w-8 text-primary" />
            </div>
            <h3 className="text-lg font-semibold mb-2">欢迎使用志愿填报咨询</h3>
            <p className="text-muted-foreground text-sm max-w-md leading-relaxed">
              我是您的志愿填报顾问，可以帮您分析院校录取概率、推荐适合的专业方向、解答填报政策疑问。
            </p>
            <div className="mt-6 flex flex-wrap justify-center gap-2">
              {['600分能上什么学校', '计算机专业推荐', '冲稳保怎么填'].map((q) => (
                <button
                  key={q}
                  onClick={() => handleSend(q)}
                  className="px-4 py-2 bg-white border rounded-lg text-sm text-muted-foreground hover:border-primary hover:text-primary transition-colors"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        )}
        {messages.map((msg) => (
          <ChatMessage key={msg.id} message={msg} />
        ))}
        {isLoading && (
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <div className="w-2 h-2 bg-primary rounded-full animate-bounce"></div>
            <div className="w-2 h-2 bg-primary rounded-full animate-bounce [animation-delay:0.1s]"></div>
            <div className="w-2 h-2 bg-primary rounded-full animate-bounce [animation-delay:0.2s]"></div>
            <span className="ml-1">正在分析...</span>
          </div>
        )}
      </div>

      {/* Input */}
      <div className="py-4 border-t">
        <ChatInput onSend={handleSend} disabled={isLoading} />
      </div>
    </div>
  )
}

export default ChatPage
