<template>
  <div class="max-w-7xl mx-auto px-6 py-10 space-y-20">
    <!--  Filtry i sortowanie -->
    <section class="flex flex-col sm:flex-row sm:items-center sm:justify-center gap-4 mb-8">
      <input
        v-model="searchName"
        placeholder="🔍 Nazwa warsztatu"
        class="input w-full sm:w-64"
      />
      <input
        v-model="searchLocation"
        placeholder="📍 Lokalizacja"
        class="input w-full sm:w-48"
      />
      <input
        v-model="equipmentFilter"
        placeholder="🔧 Wyposażenie"
        class="input w-full sm:w-48"
      />
      <select v-model="sortBy" class="input w-full sm:w-44">
        <option value="">Sortuj według...</option>
        <option value="price">💰 Cena</option>
        <option value="rating">⭐ Ocena</option>
      </select>
    </section>

    <!--  Lista warsztatów -->
    <section>
      <h2 class="text-2xl font-bold text-gray-800 mb-6 text-center">Dostępne warsztaty</h2>
      <div v-if="loading" class="text-center text-gray-500">Ładowanie warsztatów...</div>
      <div v-else-if="filteredWorkshops.length === 0" class="text-center text-gray-400">Brak wyników.</div>

      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
        <Transition
          v-for="(workshop, index) in paginatedWorkshops"
          :key="workshop.id"
          enter-active-class="transition duration-500 ease-out"
          enter-from-class="opacity-0 translate-y-4"
          enter-to-class="opacity-100 translate-y-0"
        >
          <div
            class="bg-white rounded-xl shadow-md overflow-hidden transition hover:shadow-xl hover:scale-[1.015] cursor-pointer"
            :style="{ transitionDelay: `${index * 80}ms` }"
            @click="openModal(workshop)"
          >
            <img :src="getImage(workshop)" alt="" class="w-full h-48 object-cover" />
            <div class="p-4 space-y-2">
              <h3 class="text-lg font-bold text-gray-800">{{ workshop.name }}</h3>
              <p class="text-sm text-gray-500 truncate">{{ workshop.location }}</p>
              <p v-if="workshop.average_rating" class="text-yellow-500 text-sm">
                ⭐ {{ workshop.average_rating }}/5 ({{ workshop.reviews_count }})
              </p>
              <p v-else class="text-gray-400 text-sm">Brak ocen</p>
              <p class="text-sm text-gray-600 line-clamp-2">{{ workshop.description }}</p>
              <div class="flex flex-wrap gap-2 mt-2">
                <span
                  v-for="item in parseEquipment(workshop.equipment)"
                  :key="item"
                  class="inline-flex items-center gap-1 bg-blue-100 text-blue-700 px-2 py-1 rounded text-xs"
                >
                  🧰 {{ item.trim() }}
                </span>
              </div>
            </div>
          </div>
        </Transition>
      </div>

      <!-- Paginacja -->
      <div v-if="totalPages > 1" class="flex justify-center mt-10 gap-2 flex-wrap">
        <button
          @click="goToPage(currentPage - 1)"
          :disabled="currentPage === 1"
          class="px-3 py-1 rounded bg-gray-100 hover:bg-gray-200 disabled:opacity-50"
        >
          ← Poprzednia
        </button>

        <button
          v-for="n in totalPages"
          :key="n"
          @click="goToPage(n)"
          :class="[
            'px-3 py-1 rounded hover:bg-blue-200',
            currentPage === n ? 'bg-blue-500 text-white font-bold' : 'bg-gray-100'
          ]"
        >
          {{ n }}
        </button>

        <button
          @click="goToPage(currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="px-3 py-1 rounded bg-gray-100 hover:bg-gray-200 disabled:opacity-50"
        >
          Następna →
        </button>
      </div>
    </section>

    <!-- Modal szczegółów -->
    <div
      v-if="showModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div class="bg-white w-full max-w-4xl rounded-xl shadow-xl p-6 relative max-h-[90vh] overflow-y-auto">
        <button @click="closeModal" class="absolute top-2 right-3 text-xl text-gray-500 hover:text-black">&times;</button>

        <div class="flex flex-col lg:flex-row gap-6">
          <div class="w-full lg:w-1/2">
            <img
              v-if="selectedWorkshop.photos?.[0]"
              :src="selectedWorkshop.photos[0].image"
              class="w-full h-64 object-cover rounded-xl shadow mb-4"
            />
            <div class="flex flex-wrap gap-2">
              <span
                v-for="item in parseEquipment(selectedWorkshop.equipment)"
                :key="item"
                class="inline-flex items-center gap-1 bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm"
              >
                🧰 {{ item.trim() }}
              </span>
            </div>
          </div>

          <div class="w-full lg:w-1/2 space-y-2">
            <h2 class="text-3xl font-extrabold text-gray-800">{{ selectedWorkshop.name }}</h2>
            <p class="text-gray-500 text-sm">📍 {{ selectedWorkshop.location }} | {{ selectedWorkshop.area }} m²</p>
            <p class="text-gray-700 text-sm"><strong>Opis:</strong> {{ selectedWorkshop.description }}</p>
            <p class="text-gray-700 text-sm"><strong>Wyposażenie:</strong> {{ selectedWorkshop.equipment }}</p>
            <p class="text-gray-700 text-sm"><strong>Warunki:</strong> {{ selectedWorkshop.rental_terms }}</p>
            <p class="text-blue-700 text-sm font-semibold">
              <strong>Ceny:</strong>
              {{ selectedWorkshop.hourly_rate }}zł/h,
              {{ selectedWorkshop.daily_rate }}zł/dzień,
              {{ selectedWorkshop.monthly_rate }}zł/mies.
            </p>

            <div v-if="selectedWorkshop.average_rating" class="text-yellow-500 text-sm">
              ⭐ Średnia ocen: {{ selectedWorkshop.average_rating }}/5 ({{ selectedWorkshop.reviews_count }})
            </div>

            <div class="mt-4">
              <button
                v-if="isLoggedIn && selectedWorkshop.owner?.id !== user?.user_id"
                @click="goToBooking(selectedWorkshop.id)"
                class="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700 transition"
              >
                📋 Rezerwuj ten warsztat
              </button>

              <p v-else-if="selectedWorkshop.owner?.id === user?.user_id" class="mt-4 text-yellow-600 font-medium">
                👑 To Twój warsztat
              </p>

              <router-link v-else to="/login" class="mt-4 text-gray-600 hover:underline block">
                🔐 Zaloguj się, aby zarezerwować
              </router-link>
            </div>
          </div>
        </div>

        <div class="mt-8">
          <h3 class="font-semibold text-lg text-gray-800 mb-3">Oceny i opinie:</h3>
          <div v-if="selectedWorkshop.reviews?.length" class="space-y-4">
            <div
              v-for="(review, idx) in selectedWorkshop.reviews"
              :key="idx"
              class="border border-gray-200 p-4 rounded-xl shadow-sm bg-gray-50"
            >
              <p class="text-sm text-gray-800">"{{ review.comment }}"</p>
              <p class="text-yellow-500 text-xs">⭐ Ocena: {{ review.rating }}/5</p>
            </div>
          </div>
          <p v-else class="text-sm text-gray-500">Brak opinii dla tego warsztatu.</p>
        </div>
      </div>
    </div>

    <!-- Karuzela top warsztatów -->
    <section>
      <h2 class="text-xl font-semibold text-gray-700 mb-4 text-center">⭐ Najlepiej oceniane warsztaty</h2>
      <Swiper
        :slides-per-view="1"
        :loop="true"
        :autoplay="{ delay: 10000 }"
        class="rounded-xl overflow-hidden shadow-xl relative"
      >
        <SwiperSlide v-for="w in topWorkshops" :key="w.id">
          <div class="relative h-[280px]">
            <img :src="getImage(w)" class="w-full h-full object-cover" />
            <div class="absolute inset-0 bg-black bg-opacity-40 flex flex-col justify-end p-6 text-white">
              <h3 class="text-2xl font-bold">{{ w.name }}</h3>
              <p class="text-sm">{{ w.location }}</p>
            </div>
          </div>
        </SwiperSlide>
      </Swiper>
    </section>

    <!-- Stopka -->
    <footer class="bg-gray-800 text-white py-8 mt-20 rounded-xl">
      <div class="max-w-7xl mx-auto px-6 flex flex-col sm:flex-row justify-between items-center gap-4">
        <div class="text-sm">© {{ new Date().getFullYear() }} Men’s Cave. Wszelkie prawa zastrzeżone.</div>
        <div class="flex gap-4 text-sm">
          <a href="#" class="hover:underline">Polityka prywatności</a>
          <a href="#" class="hover:underline">Regulamin</a>
          <a href="#" class="hover:underline">Kontakt</a>
        </div>
      </div>
    </footer>
  </div>
</template>


<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '../services/axios'
import { Swiper, SwiperSlide } from 'swiper/vue'
import 'swiper/swiper-bundle.css'

const router = useRouter()
const workshops = ref([])
const loading = ref(false)
const isLoggedIn = ref(!!localStorage.getItem('token'))
const user = ref(null)
const searchName = ref('')
const searchLocation = ref('')
const sortBy = ref('')
const equipmentFilter = ref('')
const currentPage = ref(1)
const itemsPerPage = 6
const selectedWorkshop = ref(null)
const showModal = ref(false)

function openModal(workshop) {
  selectedWorkshop.value = workshop
  showModal.value = true
}

function closeModal() {
  selectedWorkshop.value = null
  showModal.value = false
}

function goToBooking(id) {
  closeModal()
  router.push(`/booking/${id}`)
}

function parseJwt(token) {
  try {
    return JSON.parse(atob(token.split('.')[1]))
  } catch {
    return null
  }
}

function getImage(workshop) {
  if (workshop.photos?.length) return workshop.photos[0].image
  return '/placeholder.avif'
}

function parseEquipment(equipmentString) {
  return equipmentString?.split(',') || []
}

const topWorkshops = computed(() => {
  return [...workshops.value]
    .filter(w => w.reviews_count > 0)
    .sort((a, b) => b.average_rating - a.average_rating)
    .slice(0, 5)
})

const filteredWorkshops = computed(() => {
  let list = [...workshops.value]

  if (searchName.value) {
    const nameQ = searchName.value.toLowerCase()
    list = list.filter(w => w.name.toLowerCase().includes(nameQ))
  }

  if (searchLocation.value) {
    const locQ = searchLocation.value.toLowerCase()
    list = list.filter(w => w.location.toLowerCase().includes(locQ))
  }

  if (equipmentFilter.value) {
    const eq = equipmentFilter.value.toLowerCase()
    list = list.filter(w => w.equipment?.toLowerCase().includes(eq))
  }

  if (sortBy.value === 'price') {
    list.sort((a, b) => parseFloat(a.hourly_rate) - parseFloat(b.hourly_rate))
  } else if (sortBy.value === 'rating') {
    list.sort((a, b) => b.average_rating - a.average_rating)
  }

  return list
})

const paginatedWorkshops = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return filteredWorkshops.value.slice(start, start + itemsPerPage)
})

const totalPages = computed(() => Math.ceil(filteredWorkshops.value.length / itemsPerPage))

function goToPage(page) {
  if (page >= 1 && page <= totalPages.value) currentPage.value = page
}

async function fetchWorkshops() {
  loading.value = true
  try {
    const token = localStorage.getItem('token')
    if (token) user.value = parseJwt(token)

    const response = await apiClient.get('/api/workshops/')
    const raw = Array.isArray(response.data) ? response.data : response.data.results

    workshops.value = raw.map(w => {
      const reviews = w.reviews || []
      const avg =
        reviews.length > 0
          ? (reviews.reduce((s, r) => s + r.rating, 0) / reviews.length).toFixed(1)
          : null
      return { ...w, average_rating: avg, reviews_count: reviews.length, reviews }
    })
  } catch (err) {
    console.error('❌ Błąd pobierania warsztatów:', err)
  } finally {
    loading.value = false
  }
}

onMounted(fetchWorkshops)
</script>

<style scoped>
.input {
  @apply border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 w-full;
}
.line-clamp-2 {
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}
</style>
