<template>
    <div class="bg-white border rounded-lg p-4 shadow mt-4">
      <h4 class="text-sm font-semibold text-gray-800 mb-3">📝 Wystaw swoją opinię</h4>
  
      <form @submit.prevent="submitReview" class="space-y-3">
        <!-- Ocena -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Ocena (1–5 ⭐)</label>
          <select v-model="rating" class="input" required>
            <option disabled value="">Wybierz ocenę</option>
            <option v-for="n in 5" :key="n" :value="n">{{ n }} ⭐</option>
          </select>
        </div>
  
        <!-- Komentarz -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Komentarz</label>
          <textarea
            v-model="comment"
            rows="3"
            placeholder="Podziel się swoją opinią..."
            class="input"
            required
          ></textarea>
        </div>
  
        <!-- Akcja -->
        <button
          type="submit"
          class="btn-primary w-full"
          :disabled="loading"
        >
          {{ loading ? 'Wysyłanie...' : 'Zatwierdź opinię' }}
        </button>
      </form>
  
      <!-- Komunikaty -->
      <p v-if="success" class="mt-3 text-sm text-green-600">✅ {{ success }}</p>
      <p v-if="error" class="mt-3 text-sm text-red-600">❌ {{ error }}</p>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import apiClient from '../services/axios'
  
  const props = defineProps({
    workshopId: {
      type: Number,
      required: true
    }
  })
  
  const rating = ref('')
  const comment = ref('')
  const success = ref(null)
  const error = ref(null)
  const loading = ref(false)
  
  async function submitReview() {
    success.value = null
    error.value = null
    loading.value = true
  
    try {
      await apiClient.post('/api/reviews/', {
        workshop: props.workshopId,
        rating: rating.value,
        comment: comment.value
      })
  
      success.value = 'Opinia została pomyślnie dodana!'
      rating.value = ''
      comment.value = ''
    } catch (err) {
      if (err.response?.data?.non_field_errors) {
        error.value = err.response.data.non_field_errors[0]
      } else if (err.response?.data?.detail) {
        error.value = err.response.data.detail
      } else if (err.response?.data?.rating) {
        error.value = err.response.data.rating[0]
      } else {
        error.value = 'Nie udało się dodać opinii.'
      }
      console.error(err)
    } finally {
      loading.value = false
    }
  }
  </script>
  
  <style scoped>
  .input {
    @apply w-full border border-gray-300 p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500;
  }
  .btn-primary {
    @apply bg-blue-600 text-white font-semibold py-2 px-4 rounded hover:bg-blue-700 transition disabled:opacity-60;
  }
  </style>
  