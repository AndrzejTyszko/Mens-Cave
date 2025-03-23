<template>
  <div class="max-w-4xl mx-auto px-4 py-10 bg-white/90 rounded-3xl shadow-xl backdrop-blur-md relative overflow-hidden">
    <div class="grid md:grid-cols-2 gap-8">
      
      <!-- Zdjęcie warsztatu -->
      <div class="relative rounded-xl overflow-hidden shadow">
        <img :src="workshop.photos?.[0]?.image" alt="Zdjęcie warsztatu" class="object-cover w-full h-80" v-if="workshop.photos?.length" />
        <div v-else class="bg-gray-100 w-full h-80 flex items-center justify-center text-gray-500">Brak zdjęcia</div>
      </div>

      <!-- Dane warsztatu + formularz -->
      <div>
        <h2 class="text-3xl font-bold text-gray-800 mb-2">{{ workshop.name }}</h2>
        <p class="text-gray-600 mb-1"><span class="font-semibold">📍 Lokalizacja:</span> {{ workshop.location }}</p>
        <p class="text-gray-600 mb-1"><span class="font-semibold">📐 Powierzchnia:</span> {{ workshop.area }} m²</p>

        <!-- Wyposażenie jako lista -->
        <div class="mb-4">
          <p class="font-semibold text-gray-700 mb-1">🛠️ Wyposażenie:</p>
          <ul class="list-disc list-inside text-gray-600 space-y-1">
            <li v-for="(item, index) in formattedEquipment" :key="index">{{ item }}</li>
          </ul>
        </div>

        <p class="text-gray-700 mb-6">{{ workshop.description }}</p>

        <!-- Formularz rezerwacji -->
        <form @submit.prevent="handleBooking" class="space-y-4">
          <div>
            <label class="block mb-1 font-medium text-sm">📅 Data i godzina rozpoczęcia</label>
            <input
              type="datetime-local"
              v-model="start"
              class="input"
              :min="minDateTime"
              required
            />
          </div>

          <div>
            <label class="block mb-1 font-medium text-sm">📅 Data i godzina zakończenia</label>
            <input
              type="datetime-local"
              v-model="end"
              class="input"
              :min="start || minDateTime"
              required
            />
          </div>

          <div v-if="totalPrice !== null" class="text-green-700 font-semibold">
            💰 Cena całkowita: {{ totalPrice.toFixed(2) }} zł
          </div>

          <div v-if="success" class="text-green-600 mt-3">{{ success }}</div>
          <div v-if="submitError" class="text-red-600 mt-3">{{ submitError }}</div>

          <button type="submit" class="btn-primary">Zarezerwuj</button>
        </form>
      </div>
    </div>

    <!-- Sekcja opinii -->
    <div class="mt-12 border-t pt-8">
      <h3 class="text-2xl font-bold text-gray-800 mb-4">⭐ Opinie o warsztacie</h3>
      <div v-if="reviews.length === 0" class="text-gray-500">Brak jeszcze opinii.</div>
      <div v-else class="space-y-4">
        <div v-for="review in reviews" :key="review.id" class="bg-gray-50 p-4 rounded-lg border border-gray-200">
          <div class="flex items-center justify-between mb-2">
            <p class="font-semibold text-gray-800">{{ review.user.username }}</p>
            <p class="text-yellow-500">Ocena: {{ review.rating }}/5</p>
          </div>
          <p class="text-gray-600 italic">"{{ review.comment }}"</p>
        </div>
      </div>
    </div>

    <!-- Loader i błąd -->
    <div v-if="loading" class="absolute inset-0 flex items-center justify-center bg-white/80 z-10">
      ⏳ Ładowanie danych warsztatu...
    </div>
    <div v-else-if="error" class="absolute inset-0 flex items-center justify-center bg-red-50 text-red-600 font-medium z-10">
      {{ error }}
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import apiClient from '../services/axios'

const route = useRoute()
const router = useRouter()

const workshop = ref({})
const reviews = ref([])

const start = ref('')
const end = ref('')
const totalPrice = ref(null)
const success = ref(null)
const submitError = ref(null)
const error = ref(null)
const loading = ref(true)

const minDateTime = computed(() => {
  const now = new Date()
  now.setMinutes(now.getMinutes() - now.getTimezoneOffset())
  return now.toISOString().slice(0, 16)
})

// Formatowanie wyposażenia do listy
const formattedEquipment = computed(() => {
  if (!workshop.value.equipment) return []
  return workshop.value.equipment.split(',').map(item => item.trim()).filter(Boolean)
})

// Obliczanie ceny
watch([start, end], () => {
  if (start.value && end.value) {
    const s = new Date(start.value)
    const e = new Date(end.value)
    const durationH = (e - s) / 1000 / 60 / 60
    if (durationH > 0) {
      totalPrice.value = durationH * parseFloat(workshop.value.hourly_rate)
    } else {
      totalPrice.value = null
    }
  } else {
    totalPrice.value = null
  }
})

// Pobierz dane warsztatu i opinie
onMounted(async () => {
  try {
    const workshopRes = await apiClient.get(`/api/workshops/${route.params.id}/`)
    workshop.value = workshopRes.data

    const reviewRes = await apiClient.get(`/api/reviews/?workshop=${route.params.id}`)
    reviews.value = reviewRes.data
  } catch (err) {
    error.value = '❌ Nie udało się pobrać danych warsztatu lub opinii.'
    console.error(err)
  } finally {
    loading.value = false
  }
})

// Rezerwacja
async function handleBooking() {
  submitError.value = null
  success.value = null

  if (!start.value || !end.value) {
    submitError.value = '📅 Wybierz poprawny przedział czasowy.'
    return
  }

  try {
    await apiClient.post('/api/reservations/', {
      workshop: workshop.value.id,
      start_datetime: start.value,
      end_datetime: end.value
    })
    success.value = '✅ Rezerwacja została zapisana!'
    setTimeout(() => router.push('/profile'), 2000)
  } catch (err) {
    console.error(err)
    submitError.value = '❌ Nie udało się utworzyć rezerwacji. Sprawdź dane lub spróbuj ponownie.'
  }
}
</script>

<style scoped>
.input {
  @apply w-full border border-gray-300 px-4 py-2 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition;
}
.btn-primary {
  @apply bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold px-6 py-3 rounded-lg shadow-md hover:shadow-lg transition-all duration-200 hover:-translate-y-0.5;
}
</style>
