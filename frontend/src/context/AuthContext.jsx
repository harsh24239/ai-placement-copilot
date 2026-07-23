import { createContext, useContext, useState } from 'react'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [token, setToken] = useState(null)
  const [credits, setCredits] = useState(null)
  const [email, setEmail] = useState(null)

  const login = (newToken, newCredits, userEmail) => {
    setToken(newToken)
    setCredits(newCredits)
    setEmail(userEmail)
  }

  const logout = () => {
    setToken(null)
    setCredits(null)
    setEmail(null)
  }

  const updateCredits = (newCredits) => setCredits(newCredits)

  return (
    <AuthContext.Provider value={{ token, credits, email, login, logout, updateCredits }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}
