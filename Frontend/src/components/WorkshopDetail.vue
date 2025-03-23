<template>
    <div class="max-w-6xl mx-auto px-4 py-10">
      <div v-if="loading" class="text-gray-500">Ładowanie...</div>
      <div v-else-if="error" class="text-red-600">{{ error }}</div>
      <div v-else>
        <!-- Nazwa i lokalizacja -->
        <div class="mb-6">
          <h1 class="text-3xl font-bold text-gray-800 mb-1">{{ workshop.name }}</h1>
          <p class="text-gray-500">📍 {{ workshop.location }}</p>
        </div>
  
        <!-- Galeria zdjęć -->
        <div v-if="workshop.photos?.length" class="grid grid-cols-2 md:grid-cols-3 gap-4 mb-8">
          <img
            v-for="photo in workshop.photos"
            :key="photo.id"
            :src="photo.image"
            class="w-full h-48 object-cover rounded-lg shadow-sm"
          />
        </div>
        <div v-else class="text-gray-400 italic mb-6">Brak zdjęć tego warsztatu.</div>
  
        <!-- Opis i szczegóły -->
        <div class="bg-white shadow rounded-lg p-6 space-y-3 mb-10">
          <p><strong>📐 Powierzchnia:</strong> {{ workshop.area }} m²</p>
          <p><strong>🧰 Wyposażenie:</strong> {{ workshop.equipment }}</p>
          <p><strong>📄 Warunki wynajmu:</strong> {{ workshop.rental_terms }}</p>
          <div class="flex flex-wrap gap-4 text-sm mt-4">
            <span class="bg-blue-100 text-blue-800 px-3 py-1 rounded">💸 {{ workshop.hourly_rate }} zł / godz</span>
            <span class="bg-blue-100 text-blue-800 px-3 py-1 rounded">📅 {{ workshop.daily_rate }} zł / dzień</span>
            <span class="bg-blue-100 text-blue-800 px-3 py-1 rounded">🗓 {{ workshop.monthly_rate }} zł / miesiąc</span>
          </div>
        </div>
  
        <!-- Przycisk rezerwacji -->
        <router-link
          :to="`/booking/${workshop.id}`"
          class="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700 transition"
        >
          Zarezerwuj warsztat
        </router-link>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  import apiClient from '../services/axios'
  
  const route = useRoute()
  const workshop = ref({})
  const loading = ref(true)
  const error = ref(null)
  
  onMounted(fetchWorkshop)
  
  async function fetchWorkshop() {
    loading.value = true
    try {
      const response = await apiClient.get(`/api/workshops/${route.params.id}/`)
      workshop.value = response.data
    } catch (err) {
      error.value = '❌ Nie udało się pobrać danych warsztatu.'
      console.error(err)
    } finally {
      loading.value = false
    }
  }
  </script>
  