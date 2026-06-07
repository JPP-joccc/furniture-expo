import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api'
import type { RegisterPayload, LoginPayload } from '@/api'
import type { User } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const user = ref<User | null>(
    localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')!) : null,
  )

  const isLoggedIn = computed(() => !!token.value && !!user.value)
  const isCustomer = computed(() => user.value?.role === 'customer')
  const isMerchant = computed(() => user.value?.role === 'merchant')

  function setSession(accessToken: string, userData: User) {
    token.value = accessToken
    user.value = userData
    localStorage.setItem('token', accessToken)
    localStorage.setItem('user', JSON.stringify(userData))
  }

  function clearSession() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  async function login(data: LoginPayload) {
    const res = await authApi.login(data)
    setSession(res.data.access_token, res.data.user)
    return res.data.user
  }

  async function register(data: RegisterPayload) {
    const res = await authApi.register(data)
    setSession(res.data.access_token, res.data.user)
    return res.data.user
  }

  async function fetchMe() {
    if (!token.value) return null
    try {
      const res = await authApi.me()
      user.value = res.data
      localStorage.setItem('user', JSON.stringify(res.data))
      return res.data
    } catch {
      clearSession()
      return null
    }
  }

  function logout() {
    clearSession()
  }

  return {
    token,
    user,
    isLoggedIn,
    isCustomer,
    isMerchant,
    login,
    register,
    fetchMe,
    logout,
    setSession,
  }
})
