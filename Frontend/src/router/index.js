// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

// Import widoków (na razie przykładowe „puste”)
import Home from '../pages/Home.vue'
import About from '../pages/About.vue'
import Workshops from '../pages/Workshops.vue'
import Register from '../pages/Register.vue'
import Login from '../pages/Login.vue'
import AddWorkshop from '../pages/AddWorkshop.vue'
import Profile from '../pages/Profile.vue'
import Booking from '../pages/Booking.vue'



const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'Home', component: Home },
    { path: '/about', name: 'About', component: About },
    { path: '/workshops', name: 'Workshops', component: Workshops },
    { path: '/my-workshops/add', name: 'AddWorkshop', component: AddWorkshop },
    { path: '/register', name: 'Register', component: Register },
    { path: '/login', name: 'Login', component: Login },
    { path: '/booking/:id', name: 'Booking', component: Booking },
    { path: '/profile', component: Profile }


  ],
})

export default router
