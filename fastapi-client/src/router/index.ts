import Dashboard from '@/pages/Dashboard.vue'
import Register from '@/pages/Register.vue'
import { useAuthStore } from '@/stores/auth'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/register', component: Register, name: "register" },
    { path: '/dashboard', component: Dashboard, name: "dashboard", meta: { requiresAuth: true } }
  ],
})

router.beforeEach(async (to) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.currentUser) {
    try {
      await authStore.getMe()
    } catch {
      return { name: 'login' }
    }
  }
})

export default router
