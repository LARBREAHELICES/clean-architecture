import React, { createContext, useEffect, useContext } from 'react'
import { useAuthStore } from '@/stores/users/useAuthStore'

// Typage simplifié pour usage React Context
interface AuthContextType {
  isAuthenticated: boolean
  user: ReturnType<typeof useAuthStore>['user']
  login: (username: string, password: string) => Promise<boolean>
  logout: () => Promise<void>
  checkAuth: () => Promise<void>
  refresh: () => Promise<boolean>
}

// Le context
const AuthContext = createContext<AuthContextType | undefined>(undefined)

// Provider React
export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const { user, login, logout, checkAuth, refresh } = useAuthStore()

  const isAuthenticated = !!user

  useEffect(() => {
    console.log('AuthProvider effect triggered', user)
  }, [user])

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated,
        user,
        login,
        logout,
        checkAuth,
        refresh,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

// Hook custom
export const useAuth = () => {
  const context = useContext(AuthContext)

  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
