import client from './client'

export interface RegisterPayload {
  email: string
  full_name: string
  password: string
}

export interface LoginPayload {
  email: string
  password: string
}

export async function registerUser(payload: RegisterPayload) {
  const res = await client.post('/auth/register', payload)
  return res.data
}

export async function loginUser(payload: LoginPayload) {
  const form = new URLSearchParams()
  form.append('username', payload.email)
  form.append('password', payload.password)
  const res = await client.post('/auth/login', form, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  })
  return res.data
}

export async function getCurrentUser() {
  const res = await client.get('/auth/me')
  return res.data
}

export async function forgotPassword(email: string) {
  const res = await client.post('/auth/forgot-password', { email })
  return res.data
}

export async function resetPassword(token: string, newPassword: string) {
  const res = await client.post('/auth/reset-password', { token, new_password: newPassword })
  return res.data
}
