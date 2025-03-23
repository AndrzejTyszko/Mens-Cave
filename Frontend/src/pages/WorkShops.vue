<template>
    <div class="p-4">
      <h2 class="text-xl font-bold mb-2">Lista warsztatów</h2>
      <div v-if="loading">Ładowanie...</div>
      <div v-else>
        <ul>
          <li 
            v-for="workshop in workshops" 
            :key="workshop.id" 
            class="border p-2 mb-2 rounded"
          >
            <h3 class="font-semibold">{{ workshop.name }}</h3>
            <p>{{ workshop.description }}</p>
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import apiClient from '../services/axios.js'
  
  const workshops = ref([])
  const loading = ref(false)
  
  async function fetchWorkshops() {
  console.log('📡 fetchWorkshops startuje')
  loading.value = true
  try {
    const response = await apiClient.get('/api/workshops/')
    console.log('✅ Odpowiedź z API:', response)
    workshops.value = response.data
  } catch (err) {
    console.error('❌ Błąd pobierania warsztatów:', err)
  } finally {
    loading.value = false
  }
}

  
  onMounted(() => {
    fetchWorkshops()
  })
  </script>
  