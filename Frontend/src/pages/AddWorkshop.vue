<template>
  <div class="max-w-4xl mx-auto p-8 mt-8 bg-white shadow-xl rounded-3xl space-y-8 border border-gray-200">
    <h2 class="text-3xl font-extrabold text-gray-800 flex items-center gap-2">
      🛠️ Dodaj Nowy Warsztat
    </h2>

    <form @submit.prevent="handleSubmit" class="space-y-6">
      <!-- Pola formularza -->
      <div v-for="(label, key) in inputFields" :key="key">
        <label :for="key" class="block mb-1 text-gray-700 font-medium">{{ label }}</label>
        <input
          v-if="!isTextarea(key)"
          :id="key"
          v-model="form[key]"
          :type="getInputType(key)"
          step="0.01"
          class="w-full border border-gray-300 rounded-lg p-3 shadow-sm focus:ring-2 focus:ring-blue-400 transition"
        />
        <textarea
          v-else
          :id="key"
          v-model="form[key]"
          class="w-full border border-gray-300 rounded-lg p-3 shadow-sm focus:ring-2 focus:ring-blue-400 transition resize-none"
          rows="4"
        />
      </div>

      <!-- Upload zdjęć -->
      <div>
        <label class="block mb-2 text-gray-700 font-medium">📷 Zdjęcia warsztatu</label>
        <input
          type="file"
          multiple
          accept="image/*"
          @change="handleFileChange"
          class="block w-full text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-100 file:text-blue-700 hover:file:bg-blue-200 transition"
        />
        <div
          v-if="previews.length"
          class="grid grid-cols-2 sm:grid-cols-3 gap-4 mt-4"
        >
          <img
            v-for="(src, index) in previews"
            :key="index"
            :src="src"
            class="w-full h-32 object-cover rounded-xl border border-gray-200 shadow"
          />
        </div>
      </div>

      <!-- Submit -->
      <button
        type="submit"
        class="w-full bg-gradient-to-r from-blue-600 to-blue-500 text-white py-3 rounded-xl font-semibold shadow hover:from-blue-700 hover:to-blue-600 transition"
      >
        💾 Zapisz warsztat
      </button>

      <!-- Komunikaty -->
      <div v-if="error" class="text-red-600 text-sm font-medium">{{ error }}</div>
      <div v-if="success" class="text-green-600 text-sm font-medium">{{ success }}</div>
    </form>
  </div>
</template>

  <script setup>
  import { ref } from 'vue'
  import apiClient from '../services/axios'
  import { useRouter } from 'vue-router'
  
  const router = useRouter()
  
  const form = ref({
    name: '',
    description: '',
    location: '',
    area: 0,
    equipment: '',
    hourly_rate: 0,
    daily_rate: 0,
    monthly_rate: 0,
    rental_terms: ''
  })
  
  const inputFields = {
    name: 'Nazwa warsztatu',
    description: 'Opis',
    location: 'Lokalizacja',
    area: 'Metraż (m²)',
    equipment: 'Wyposażenie',
    hourly_rate: 'Stawka godzinowa',
    daily_rate: 'Stawka dzienna',
    monthly_rate: 'Stawka miesięczna',
    rental_terms: 'Warunki wynajmu'
  }
  
  function isTextarea(key) {
    return ['description', 'rental_terms'].includes(key)
  }
  function getInputType(key) {
    return ['area', 'hourly_rate', 'daily_rate', 'monthly_rate'].includes(key)
      ? 'number'
      : 'text'
  }
  
  // Obsługa zdjęć
  const selectedFiles = ref([])
  const previews = ref([])
  
  function handleFileChange(e) {
    selectedFiles.value = Array.from(e.target.files)
    previews.value = selectedFiles.value.map((file) => URL.createObjectURL(file))
  }
  
  // Upload zdjęć po utworzeniu warsztatu
  async function uploadImages(workshopId) {
    const formData = new FormData()
    selectedFiles.value.forEach((file) => formData.append('image', file))
  
    try {
      await apiClient.post(`/api/workshops/${workshopId}/upload-image/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      console.log('📷 Zdjęcia przesłane')
    } catch (err) {
      console.error('❌ Błąd przesyłania zdjęć:', err)
    }
  }
  
  // Obsługa formularza
  const error = ref(null)
  const success = ref(null)
  
  async function handleSubmit() {
    error.value = null
    success.value = null
    try {
      const response = await apiClient.post('/api/workshops/', form.value)
      const workshopId = response.data.id
  
      if (selectedFiles.value.length > 0) {
        await uploadImages(workshopId)
      }
  
      success.value = '✅ Warsztat został dodany pomyślnie!'
      // Wyczyść
      for (const key in form.value) {
        form.value[key] = typeof form.value[key] === 'number' ? 0 : ''
      }
      selectedFiles.value = []
      previews.value = []
  
      // Przejdź do profilu lub innego widoku
      setTimeout(() => {
        router.push('/profile')
      }, 1500)
    } catch (err) {
      error.value = '❌ Wystąpił błąd przy tworzeniu warsztatu.'
      console.error(err)
    }
  }
  </script>
  