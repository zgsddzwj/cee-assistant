import { User, GraduationCap } from 'lucide-react'
import type { Message } from '@/types/chat'

function ChatMessage({ message }: { message: Message }) {
  const isUser = message.role === 'user'

  return (
    <div className={`flex gap-4 ${isUser ? 'flex-row-reverse' : ''}`}>
      {/* Avatar */}
      <div className="flex-shrink-0">
        {isUser ? (
          <div className="w-9 h-9 bg-muted rounded-full flex items-center justify-center">
            <User className="h-4.5 w-4.5 text-muted-foreground" />
          </div>
        ) : (
          <div className="w-9 h-9 bg-primary rounded-full flex items-center justify-center">
            <GraduationCap className="h-5 w-5 text-white" />
          </div>
        )}
      </div>

      {/* Content */}
      <div className={`max-w-[80%] space-y-1 ${isUser ? 'items-end' : 'items-start'}`}>
        <div className="flex items-center gap-2 mb-1">
          <span className="text-xs font-medium text-muted-foreground">
            {isUser ? '我' : '志愿顾问'}
          </span>
          <span className="text-[10px] text-muted-foreground/60">
            {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </span>
        </div>
        <div
          className={`px-4 py-3 rounded-2xl text-sm leading-relaxed ${
            isUser
              ? 'bg-primary text-white rounded-tr-sm'
              : 'bg-white border rounded-tl-sm shadow-sm'
          }`}
        >
          {message.content}
        </div>
      </div>
    </div>
  )
}

export default ChatMessage
