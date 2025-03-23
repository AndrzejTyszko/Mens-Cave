<template>
    <div class="bg-white rounded-lg p-6 shadow">
      <h2 class="text-xl font-semibold mb-4">📷 Dodaj zdjęcia do warsztatu</h2>
  
      <input
        type="file"
        multiple
        accept="image/*"
        @change="handleFileChange"
        class="mb-4"
      />
  
      <button
        @click="upload"
        :disabled="!files.length"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
      >
        Prześlij zdjęcia
      </button>
  
      <div v-if="preview.length" class="mt-6 grid grid-cols-2 md:grid-cols-4 gap-4">
        <img
          v-for="(src, index) in preview"
          :key="index"
          :src="src"
          class="w-full h-40 object-cover rounded shadow"
        />
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import apiClient from '../services/axios'
  import { useRoute } from 'vue-router'
  
  const route = useRoute()
  const workshopId = route.params.id
  
  const files = ref([])
  const preview = ref([])
  
  function handleFileChange(e) {
    files.value = Array.from(e.target.files)
    preview.value = files.value.map(file => URL.createObjectURL(file))
  }
  
  async function upload() {
    if (!files.value.length) return
  
    const formData = new FormData()
    files.value.forEach(file => formData.append('images', file)) // nazwane `images`
  
    try {
      await apiClient.post(`/api/workshops/${workshopId}/upload-image/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      alert('✅ Zdjęcia przesłane!')
      files.value = []
      preview.value = []
    } catch (err) {
      console.error('❌ Błąd przesyłania:', err)
      alert('Błąd przesyłania zdjęć')
    }
  }
  </script>
  