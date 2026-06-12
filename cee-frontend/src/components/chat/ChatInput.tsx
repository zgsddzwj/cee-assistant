import { useState } from 'react'
import { Send, Loader2 } from 'lucide-react'

function ChatInput({
  onSend,
  disabled,
}: {
  onSend: (msg: string) => void
  disabled?: boolean
}) {
  const [input, setInput] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (input.trim() && !disabled) {
      onSend(input.trim())
      setInput('')
    }
  }

  return (
    <form onSubmit={handleSubmit} className="relative">
      <div className="flex items-end gap-2 bg-white border rounded-2xl p-2 shadow-sm focus-within:ring-2 focus-within:ring-primary/20 focus-within:border-primary transition-all">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault()
              handleSubmit(e)
            }
          }}
          placeholder="请输入您的问题，例如：我考了600分，想报计算机专业..."
          disabled={disabled}
          rows={1}
          className="flex-1 px-3 py-2.5 resize-none outline-none text-sm max-h-32 min-h-[44px]"
          style={{ height: 'auto' }}
        />
        <button
          type="submit"
          disabled={disabled || !input.trim()}
          className="p-2.5 bg-primary text-white rounded-xl hover:bg-primary/90 transition-colors disabled:opacity-40 disabled:cursor-not-allowed flex-shrink-0"
        >
          {disabled ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
        </button>
      </div>
      <p className="text-[10px] text-muted-foreground/60 mt-1.5 text-center">
        志愿填报顾问仅供参考，请以各省教育考试院公布信息为准
      </p>
    </form>
  )
}

export default ChatInput
