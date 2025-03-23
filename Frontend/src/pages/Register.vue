<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-purple-50 p-4">
    <div class="relative w-full max-w-md bg-white/95 backdrop-blur-lg rounded-3xl shadow-xl overflow-hidden transition-all duration-300 hover:shadow-2xl">
      <div class="absolute inset-0 bg-gradient-to-br from-blue-100/50 to-purple-100/50" />
      
      <div class="relative px-8 py-12">
        <div class="mb-10 text-center space-y-2">
          <div class="inline-flex items-center justify-center w-16 h-16 bg-blue-600/10 rounded-2xl mb-4">
            <UserPlusIcon class="w-8 h-8 text-blue-600" />
          </div>
          <h2 class="text-3xl font-bold text-gray-900">Dołącz do społeczności</h2>
          <p class="text-gray-500">Stwórz swoje konto w 30 sekund</p>
        </div>

        <form @submit.prevent="handleRegister" class="space-y-6">
          <!-- Nazwa użytkownika -->
          <div class="relative group">
            <div class="absolute inset-0.5 bg-blue-50/50 rounded-lg blur opacity-0 group-focus-within:opacity-100 transition"></div>
            <div class="relative">
              <label class="sr-only">Nazwa użytkownika</label>
              <div class="flex items-center space-x-3 bg-white/50 border border-gray-200 rounded-lg px-4 py-3 shadow-sm hover:border-blue-400 transition">
                <UserCircleIcon class="w-5 h-5 text-gray-400" />
                <input
                  v-model="form.username"
                  type="text"
                  class="w-full bg-transparent focus:outline-none placeholder-gray-400"
                  placeholder="Nazwa użytkownika"
                  required
                />
              </div>
            </div>
          </div>

          <!-- Email -->
          <div class="relative group">
            <div class="absolute inset-0.5 bg-blue-50/50 rounded-lg blur opacity-0 group-focus-within:opacity-100 transition"></div>
            <div class="relative">
              <label class="sr-only">Adres email</label>
              <div class="flex items-center space-x-3 bg-white/50 border border-gray-200 rounded-lg px-4 py-3 shadow-sm hover:border-blue-400 transition">
                <EnvelopeIcon class="w-5 h-5 text-gray-400" />
                <input
                  v-model="form.email"
                  type="email"
                  class="w-full bg-transparent focus:outline-none placeholder-gray-400"
                  placeholder="Adres email"
                  required
                />
              </div>
            </div>
          </div>

          <!-- Hasło -->
          <div class="relative group">
            <div class="absolute inset-0.5 bg-blue-50/50 rounded-lg blur opacity-0 group-focus-within:opacity-100 transition"></div>
            <div class="relative">
              <label class="sr-only">Hasło</label>
              <div class="flex items-center space-x-3 bg-white/50 border border-gray-200 rounded-lg px-4 py-3 shadow-sm hover:border-blue-400 transition">
                <LockClosedIcon class="w-5 h-5 text-gray-400" />
                <input
                  v-model="form.password"
                  type="password"
                  class="w-full bg-transparent focus:outline-none placeholder-gray-400"
                  placeholder="Hasło"
                  required
                />
              </div>
            </div>
          </div>

          <!-- Komunikaty błędów -->
          <transition
            enter-active-class="transition duration-200 ease-out"
            enter-from-class="transform opacity-0"
            enter-to-class="transform opacity-100"
            leave-active-class="transition duration-150 ease-in"
            leave-from-class="transform opacity-100"
            leave-to-class="transform opacity-0"
          >
            <div v-if="error" class="flex items-center space-x-2 text-red-600 bg-red-50/80 px-4 py-3 rounded-lg">
              <ExclamationCircleIcon class="w-5 h-5 flex-shrink-0" />
              <span class="text-sm">{{ error }}</span>
            </div>
          </transition>

          <!-- Przycisk rejestracji -->
          <button
            type="submit"
            :disabled="loading"
            class="w-full flex items-center justify-center space-x-2 py-4 px-6 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold rounded-lg shadow-md hover:shadow-lg transform transition-all duration-200 hover:-translate-y-0.5"
          >
            <span v-if="!loading">Zarejestruj się</span>
            <span v-else class="flex items-center">
              <svg class="animate-spin h-5 w-5 mr-3 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Rejestracja...
            </span>
          </button>
        </form>

        <!-- Link do logowania -->
        <div class="mt-8 text-center text-sm text-gray-500">
          Masz już konto?
          <router-link
            to="/login"
            class="font-medium text-blue-600 hover:text-blue-700 transition-colors"
          >
            Zaloguj się
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { registerUser, loginUser } from '../services/auth.js'
import {
  UserCircleIcon,
  LockClosedIcon,
  EnvelopeIcon,
  ExclamationCircleIcon,
  UserPlusIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const form = ref({
  username: '',
  email: '',
  password: ''
})
const error = ref(null)
const loading = ref(false)

async function handleRegister() {
  error.value = null
  loading.value = true
  try {
    await registerUser(form.value)
    await loginUser({ username: form.value.username, password: form.value.password })
    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.message || 'Rejestracja nie powiodła się. Sprawdź dane.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* Dodatkowe style dla płynnych przejść */
input {
  transition: all 0.3s ease;
}

input:focus {
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.25);
}
</style>