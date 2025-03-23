<template>
  <div class="max-w-6xl mx-auto px-4 py-10 space-y-12">

    <!-- KARTA: Profil użytkownika -->
    <section class="bg-white shadow-md rounded-2xl p-6">
      <div class="flex items-center space-x-4 mb-6">
        <div class="w-14 h-14 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 text-xl font-bold shadow">
          {{ user?.username?.charAt(0).toUpperCase() || 'U' }}
        </div>
        <div>
          <h2 class="text-2xl font-extrabold text-gray-800">Witaj, {{ user?.username || 'Użytkowniku' }}!</h2>
          <p class="text-gray-500 text-sm">To jest Twój profil użytkownika</p>
        </div>
      </div>

      <div class="space-y-2 text-gray-700">
        <p><strong>Login:</strong> {{ user?.username || '—' }}</p>
        <p><strong>Email:</strong> {{ user?.email || '—' }}</p>
      </div>
    </section>

    <!-- KARTA: Statystyki -->
    <section class="bg-gradient-to-r from-purple-50 to-blue-50 shadow-md rounded-2xl p-6">
      <h2 class="text-xl font-bold text-gray-800 mb-4">📊 Statystyki</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6 text-center">
        <div class="bg-white p-4 rounded-xl shadow border">
          <p class="text-gray-500 text-sm mb-1">Zrealizowane rezerwacje</p>
          <p class="text-2xl font-bold text-blue-600">{{ reservations.length }}</p>
        </div>
        <div class="bg-white p-4 rounded-xl shadow border">
          <p class="text-gray-500 text-sm mb-1">Rezerwacje Twoich warsztatów</p>
          <p class="text-2xl font-bold text-purple-600">{{ reservationsForOwner.length }}</p>
        </div>
        <div class="bg-white p-4 rounded-xl shadow border">
          <p class="text-gray-500 text-sm mb-1">Średnia ocena</p>
          <p class="text-2xl font-bold text-yellow-500">{{ averageRating ?? '—' }}</p>
        </div>
        <div class="bg-white p-4 rounded-xl shadow border">
          <p class="text-gray-500 text-sm mb-1">💸 Przychód (zł)</p>
          <p class="text-2xl font-bold text-green-600">{{ ownerIncome.toFixed(2) }}</p>
        </div>
      </div>
    </section>

    <!-- KARTA: Twoje rezerwacje -->
    <section class="bg-white shadow rounded-2xl p-6">
      <h2 class="text-xl font-semibold text-gray-800 mb-6">📅 Twoje rezerwacje</h2>
      <div v-if="loadingReservations" class="text-gray-500">Ładowanie rezerwacji...</div>
      <div v-else-if="reservations.length === 0" class="text-gray-400">Brak zrealizowanych rezerwacji.</div>
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-2 gap-6">
        <div
          v-for="res in reservations"
          :key="res.id"
          class="border border-gray-200 rounded-xl p-5 bg-gray-50 shadow-sm hover:shadow-md transition"
        >
          <h3 class="text-lg font-semibold text-gray-800 mb-2">
            🛠 {{ getWorkshopName(res.workshop) }}
          </h3>
          <p class="text-sm text-gray-600">
            📅 <strong>Od:</strong> {{ formatDate(res.start_datetime) }}<br />
            ⏰ <strong>Do:</strong> {{ formatDate(res.end_datetime) }}
          </p>
          <p class="text-sm text-gray-700 mt-1">💰 <strong>Kwota:</strong> {{ res.total_price }} zł</p>
          <div class="mt-4">
            <ReviewFormInline
              v-if="new Date(res.end_datetime) < new Date() && !hasUserReviewed(getWorkshopId(res.workshop))"
              :workshopId="getWorkshopId(res.workshop)"
            />
            <p v-else-if="new Date(res.end_datetime) < new Date()" class="text-green-700 text-sm">
              ✅ Opinia została już wystawiona
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- KARTA: Rezerwacje Twoich warsztatów -->
    <section v-if="reservationsForOwner.length > 0" class="bg-white shadow rounded-2xl p-6">
      <h2 class="text-xl font-semibold text-gray-800 mb-6">📋 Rezerwacje Twoich warsztatów</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
        <div
          v-for="res in reservationsForOwner"
          :key="res.id"
          class="bg-gray-50 border border-gray-200 rounded-xl p-5 shadow-sm hover:shadow-md transition"
        >
          <h3 class="text-lg font-bold text-gray-800 mb-1">{{ getWorkshopName(res.workshop) }}</h3>
          <p class="text-sm text-gray-600">
            📅 <strong>Od:</strong> {{ formatDate(res.start_datetime) }}<br />
            ⏰ <strong>Do:</strong> {{ formatDate(res.end_datetime) }}
          </p>
          <p class="text-sm text-gray-700 mt-1">👤 <strong>Najemca:</strong> {{ res.renter.username }}</p>
          <p class="text-sm text-gray-700 mt-1">💰 <strong>Kwota:</strong> {{ res.total_price }} zł</p>
        </div>
      </div>
    </section>

    <!-- KARTA: Twoje warsztaty -->
    <section>
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-xl font-semibold text-gray-800">🔧 Twoje warsztaty</h2>
        <router-link
          to="/my-workshops/add"
          class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition"
        >
          ➕ Dodaj warsztat
        </router-link>
      </div>
      <div v-if="loadingWorkshops" class="text-gray-500">Ładowanie warsztatów...</div>
      <div v-else-if="userWorkshops.length === 0" class="text-gray-400">Nie masz jeszcze żadnych warsztatów.</div>
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="workshop in userWorkshops"
          :key="workshop.id"
          class="bg-white shadow rounded-xl p-5 space-y-2 hover:shadow-lg transition"
        >
          <h3 class="text-lg font-bold text-gray-800">{{ workshop.name }}</h3>
          <p class="text-sm text-gray-600 line-clamp-2">{{ workshop.description }}</p>
          <div class="flex justify-between mt-2 text-sm text-gray-500">
            <span>📍 {{ workshop.location }}</span>
            <span>{{ workshop.hourly_rate }} zł/h</span>
          </div>
          <div class="flex space-x-2 mt-4">
            <router-link
              :to="`/my-workshops/edit/${workshop.id}`"
              class="text-blue-600 hover:underline text-sm"
            >
              ✏️ Edytuj
            </router-link>
            <button
              @click="deleteWorkshop(workshop.id)"
              class="text-red-600 hover:underline text-sm"
            >
              🗑 Usuń
            </button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import apiClient from '../services/axios'
import ReviewFormInline from '../components/ReviewFormInline.vue'

const user = ref(null)
const reservations = ref([])
const reservationsForOwner = ref([])
const userWorkshops = ref([])
const userReviews = ref([])
const allReviews = ref([])
const loadingReservations = ref(false)
const loadingWorkshops = ref(false)
const workshopMap = ref({})

// Statystyki
const averageRating = computed(() => {
  const myWorkshopIds = userWorkshops.value.map(w => w.id)
  const relatedReviews = allReviews.value.filter(r => myWorkshopIds.includes(r.workshop?.id || r.workshop))
  if (!relatedReviews.length) return null
  const total = relatedReviews.reduce((sum, r) => sum + r.rating, 0)
  return (total / relatedReviews.length).toFixed(1)
})

const ownerIncome = computed(() => {
  return reservationsForOwner.value.reduce((sum, r) => sum + Number(r.total_price), 0)
})

//  JWT decoding (do pobrania ID)
function parseJwt(token) {
  try {
    return JSON.parse(atob(token.split('.')[1]))
  } catch (e) {
    return null
  }
}

//  Inicjalizacja
onMounted(async () => {
  const token = localStorage.getItem('token')
  const decoded = token ? parseJwt(token) : null

  if (decoded?.user_id) {
    await fetchUserDetails(decoded.user_id)
    fetchReservations(decoded.user_id)
    fetchUserWorkshops(decoded.user_id)
    fetchUserReviews()
  }
})

//  API
async function fetchUserDetails(id) {
  try {
    const res = await apiClient.get(`/api/users/${id}/`)
    user.value = res.data
  } catch (err) {
    console.error('❌ Błąd ładowania danych użytkownika:', err)
  }
}

async function fetchReservations(userId) {
  loadingReservations.value = true
  try {
    const response = await apiClient.get('/api/reservations/')
    const all = response.data
    reservations.value = all.filter(r => r.renter.id === userId)
    reservationsForOwner.value = all.filter(r => r.workshop?.owner?.id === userId)

    // Mapowanie ID warsztatów
    for (const r of all) {
      const w = r.workshop
      if (typeof w === 'object' && w.id && w.name) {
        workshopMap.value[w.id] = w.name
      }
    }
  } catch (err) {
    console.error('❌ Błąd ładowania rezerwacji:', err)
  } finally {
    loadingReservations.value = false
  }
}

async function fetchUserWorkshops(userId) {
  loadingWorkshops.value = true
  try {
    const response = await apiClient.get('/api/workshops/')
    userWorkshops.value = response.data.filter(w => w.owner.id === userId)
  } catch (err) {
    console.error('❌ Błąd ładowania warsztatów:', err)
  } finally {
    loadingWorkshops.value = false
  }
}

async function fetchUserReviews() {
  try {
    const response = await apiClient.get('/api/reviews/')
    allReviews.value = response.data
    userReviews.value = response.data.filter(r => r.user.id === user.value.id)
  } catch (err) {
    console.error('❌ Błąd ładowania opinii:', err)
  }
}

// Helpers
function hasUserReviewed(workshopId) {
  return userReviews.value.some(r => r.workshop === workshopId || r.workshop.id === workshopId)
}

function getWorkshopId(workshop) {
  return typeof workshop === 'object' ? workshop.id : workshop
}

function getWorkshopName(workshop) {
  if (typeof workshop === 'object' && workshop.name) return workshop.name
  if (typeof workshop === 'number') return workshopMap.value[workshop] || `Warsztat ID: ${workshop}`
  return '—'
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleString('pl-PL')
}

async function deleteWorkshop(id) {
  if (!confirm('Czy na pewno chcesz usunąć ten warsztat?')) return
  try {
    await apiClient.delete(`/api/workshops/${id}/`)
    userWorkshops.value = userWorkshops.value.filter(w => w.id !== id)
  } catch (err) {
    console.error('❌ Nie udało się usunąć warsztatu:', err)
  }
}
</script>
