<template>
    <div class="mt-8 bg-white p-4 rounded shadow">
      <h3 class="text-lg font-semibold mb-2">📝 Wystaw opinię</h3>
  
      <form @submit.prevent="submitReview" class="space-y-4">
        <div>
          <label class="block text-sm mb-1">Ocena (1–5 ⭐)</label>
          <select v-model="rating" class="input" required>
            <option disabled value="">Wybierz ocenę</option>
            <option v-for="n in 5" :key="n" :value="n">{{ n }} ⭐</option>
          </select>
        </div>
  
        <div>
          <label class="block text-sm mb-1">Komentarz</label>
          <textarea v-model="comment" class="input" rows="3" required />
        </div>
  
        <button class="btn-primary">Dodaj opinię</button>
      </form>
  
      <div v-if="success" class="text-green-600 mt-2">{{ success }}</div>
      <div v-if="error" class="text-red-600 mt-2">{{ error }}</div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import apiClient from '../services/axios'
  import { useRoute } from 'vue-router'
  
  const route = useRoute()
  const rating = ref('')
  const comment = ref('')
  const success = ref(null)
  const error = ref(null)
  
  async function submitReview() {
    success.value = null
    error.value = null
  
    try {
      await apiClient.post('/api/reviews/', {
        workshop: route.params.id,
        rating: rating.value,
        comment: comment.value
      })
      success.value = '✅ Opinia została dodana!'
      rating.value = ''
      comment.value = ''
    } catch (err) {
      console.error(err)
      error.value = '❌ Nie udało się dodać opinii.'
    }
  }
  </script>
  
  <style scoped>
  .input {
    @apply w-full border p-2 rounded;
  }
  .btn-primary {
    @apply bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition;
  }
  </style>
  