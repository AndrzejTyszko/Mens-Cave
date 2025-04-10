<template>
  <header class="sticky top-0 z-50 bg-white/80 backdrop-blur-md shadow-lg border-b border-gray-100 transition-all">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        
        <!-- Logo -->
        <router-link 
          to="/" 
          class="flex items-center space-x-2 group"
          @mouseenter="logoHover = true"
          @mouseleave="logoHover = false"
        >
          <div class="relative h-8 w-8">
            <transition name="bounce">
              <span v-if="logoHover" class="absolute text-3xl">🛠️</span>
              <span v-else class="absolute text-2xl">🔧</span>
            </transition>
          </div>
          <span class="text-2xl font-bold bg-gradient-to-r from-blue-600 to-fuchsia-600 bg-clip-text text-transparent tracking-wide">
            Men's Cave
          </span>
        </router-link>

        <!-- Nawigacja (desktop) -->
        <nav class="hidden md:flex space-x-6">
          <router-link
            v-for="link in mainLinks"
            :key="link.path"
            :to="link.path"
            class="nav-link"
            active-class="text-blue-600 font-semibold"
          >
            {{ link.name }}
          </router-link>
        </nav>

        <!-- Akcje użytkownika -->
        <div class="flex items-center space-x-3 relative">
          <!-- Ikona dzwonka -->
          <button v-if="isLoggedIn" class="relative p-2 hover:bg-gray-100 rounded-full group transition">
            <svg class="w-5 h-5 text-gray-600 group-hover:text-blue-600 transition" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
            <span class="absolute top-0 right-0 w-2 h-2 bg-red-500 rounded-full animate-ping"></span>
          </button>

          <!-- Avatar / dropdown -->
          <div v-if="isLoggedIn" class="relative group">
            <button @click="userMenuOpen = !userMenuOpen" class="flex items-center space-x-1">
              <div class="w-9 h-9 rounded-full bg-gradient-to-tr from-blue-400 to-purple-500 shadow-inner flex items-center justify-center text-white font-semibold animate-pulse">
                {{ userInitial }}
              </div>
            </button>

            <!-- Dropdown -->
            <transition name="fade">
              <div v-if="userMenuOpen" class="absolute right-0 mt-3 w-56 bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden z-50">
                <router-link to="/profile" class="block px-4 py-3 hover:bg-blue-50 text-sm" @click="userMenuOpen = false">
                  👤 Mój profil
                </router-link>
                <router-link to="/my-workshops/add" class="block px-4 py-3 hover:bg-blue-50 text-sm" @click="userMenuOpen = false">
                  ➕ Dodaj warsztat
                </router-link>
                <button @click="handleLogout" class="w-full text-left px-4 py-3 hover:bg-red-50 text-sm text-red-600">
                  🚪 Wyloguj
                </button>
              </div>
            </transition>
          </div>

          <!-- Gdy niezalogowany -->
          <template v-else>
            <router-link to="/login" class="action-btn border border-blue-600 text-blue-600 hover:bg-blue-50">
              Zaloguj
            </router-link>
            <router-link to="/register" class="action-btn bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:shadow-lg">
              Rejestracja
            </router-link>
          </template>
        </div>

        <!-- Mobile toggle -->
        <button @click="mobileMenuOpen = !mobileMenuOpen" class="md:hidden p-2 hover:bg-gray-100 rounded-lg">
          <svg class="w-6 h-6 text-gray-600 transform transition-transform" :class="{ 'rotate-90': mobileMenuOpen }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- Mobile nav -->
    <transition enter-active-class="transition-all duration-300" leave-active-class="transition-all duration-300" enter-from-class="opacity-0 max-h-0" leave-to-class="opacity-0 max-h-0">
      <div v-if="mobileMenuOpen" class="md:hidden bg-white border-t">
        <div class="px-4 py-3 space-y-2">
          <router-link
            v-for="link in mobileLinks"
            :key="link.path"
            :to="link.path"
            class="mobile-link"
            active-class="text-blue-600 bg-blue-50"
            @click="mobileMenuOpen = false"
          >
            {{ link.name }}
          </router-link>
        </div>
      </div>
    </transition>
  </header>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { logoutUser } from '../services/auth.js'

const router = useRouter()
const isLoggedIn = ref(!!localStorage.getItem('token'))
const mobileMenuOpen = ref(false)
const userMenuOpen = ref(false)
const logoHover = ref(false)

const mainLinks = ref([
  { name: 'Strona Główna', path: '/' },
  { name: 'Warsztaty', path: '/workshops' }
])

const mobileLinks = computed(() => [
  ...mainLinks.value,
  ...(isLoggedIn.value
    ? [
        { name: 'Profil', path: '/profile' },
        { name: 'Dodaj Warsztat', path: '/my-workshops/add' },
        { name: 'Wyloguj', path: '/logout' }
      ]
    : [
        { name: 'Zaloguj się', path: '/login' },
        { name: 'Rejestracja', path: '/register' }
      ])
])

const userInitial = computed(() => {
  try {
    const token = localStorage.getItem('token')
    if (!token) return 'U'
    const payload = JSON.parse(atob(token.split('.')[1]))
    return payload?.username?.charAt(0).toUpperCase() || 'U'
  } catch {
    return 'U'
  }
})

function handleLogout() {
  logoutUser()
  isLoggedIn.value = false
  userMenuOpen.value = false
  mobileMenuOpen.value = false
  router.push('/login')
}
</script>

<style scoped>
.nav-link {
  @apply text-gray-600 px-2 py-1.5 hover:text-blue-600 transition-colors;
}
.mobile-link {
  @apply block px-4 py-2.5 rounded-lg text-gray-600 hover:text-blue-600 hover:bg-blue-50 transition-colors;
}
.action-btn {
  @apply px-4 py-1.5 rounded-lg text-sm font-medium transition-all transform hover:-translate-y-0.5;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s, transform 0.2s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
.bounce-enter-active {
  animation: bounce-in 0.3s;
}
.bounce-leave-active {
  animation: bounce-in 0.3s reverse;
}
@keyframes bounce-in {
  0% { transform: scale(0); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}
</style>
