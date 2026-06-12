import { create } from 'zustand'
import type { User, StudentProfile } from '@/types/user'

interface UserState {
  user: User | null
  profile: StudentProfile | null
  isLoggedIn: boolean
  setUser: (user: User | null) => void
  setProfile: (profile: StudentProfile | null) => void
  logout: () => void
}

export const useUserStore = create<UserState>((set) => ({
  user: null,
  profile: null,
  isLoggedIn: false,
  setUser: (user) => set({ user, isLoggedIn: !!user }),
  setProfile: (profile) => set({ profile }),
  logout: () => set({ user: null, profile: null, isLoggedIn: false }),
}))
