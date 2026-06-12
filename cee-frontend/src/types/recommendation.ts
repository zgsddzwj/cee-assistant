export interface College {
  id: string
  name: string
  location: string
  logo?: string
  tags: string[]
}

export interface Recommendation {
  college: College
  major: string
  probability: number
  category: '冲刺' | '稳妥' | '保底'
  previousScores: number[]
}
