export interface User {
  id: string
  name: string
  email: string
  phone?: string
}

export interface StudentProfile {
  province: string
  subjectType: string
  score: number
  rank: number
  interests: string[]
  preferredLocations: string[]
}
