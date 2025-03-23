import apiClient from './axios'

// 🔓 Pomocnicza funkcja do dekodowania tokena JWT
function parseJwt(token) {
  try {
    return JSON.parse(atob(token.split('.')[1]))
  } catch (e) {
    console.warn(' Nie udało się zdekodować tokena:', e)
    return null
  }
}

export async function registerUser({ username, email, password }) {
  const response = await apiClient.post('/api/register/', {
    username,
    email,
    password,
  })
  return response.data
}

export async function loginUser({ username, password }) {
  try {
    const response = await apiClient.post('/api/token/', { username, password })

    console.log('✅ Odpowiedź z serwera (tokeny):', response.data)

    const { access, refresh } = response.data

    // Zapisz tokeny
    localStorage.setItem('token', access)
    localStorage.setItem('refreshToken', refresh)
    console.log('📦 Token zapisany w localStorage:', localStorage.getItem('token'))

    // 🔍 Dekoduj usera z access tokena
    const user = parseJwt(access)
    console.log('👤 Użytkownik z tokena:', user)
    if (user) {
      localStorage.setItem('user', JSON.stringify(user))
    }

    return response.data
  } catch (err) {
    console.error('❌ Błąd logowania:', err.response?.data || err.message)
    throw err
  }
}

export function logoutUser() {
  console.log('🚪 Wylogowanie – usuwanie tokenów')
  localStorage.removeItem('token')
  localStorage.removeItem('refreshToken')
  localStorage.removeItem('user')
}
