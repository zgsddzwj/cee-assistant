export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: string
}

export interface ChatSession {
  id: string
  title: string
  messages: Message[]
  createdAt: string
}
