<template>
    <div>
      <label class="block mb-1 font-medium text-sm">Wybierz termin rezerwacji</label>
      <flat-pickr
        v-model="selectedRange"
        :config="config"
        class="w-full border rounded p-2"
      />
    </div>
  </template>
  
  <script setup>
  import { ref, watch, onMounted } from 'vue'
  import FlatPickr from 'vue-flatpickr-component'
  import 'flatpickr/dist/flatpickr.css'
  import apiClient from '../services/axios'
  import { useRoute } from 'vue-router'
  
  const selectedRange = defineModel()
  const route = useRoute()
  const availability = ref([])
  
  const config = ref({
    mode: 'range',
    minDate: 'today',
    enable: [],
    dateFormat: 'Y-m-d H:i',
    enableTime: true,
    time_24hr: true,
  })
  
  async function fetchAvailability() {
    try {
      const response = await apiClient.get(`/api/availability/${route.params.id}/`)
      availability.value = response.data.map(a => ({
        from: a.available_from,
        to: a.available_to,
      }))
  
      config.value.enable = availability.value.map(a => ({
        from: a.from,
        to: a.to,
      }))
    } catch (err) {
      console.error('❌ Błąd ładowania dostępności:', err)
    }
  }
  
  onMounted(fetchAvailability)
  </script>
  