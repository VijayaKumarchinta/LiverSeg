import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

// Layouts
import AppLayout from '../layouts/AppLayout.vue'
import DashboardLayout from '../layouts/DashboardLayout.vue'

// Public marketing pages
import Home from '../pages/public/Home.vue'
import About from '../pages/public/About.vue'
import Contact from '../pages/public/Contact.vue'
import Platform from '../pages/public/Platform.vue'
import ResearchPublic from '../pages/public/ResearchPublic.vue'

// Auth layouts
import Login from '../pages/auth/Login.vue'
import Register from '../pages/auth/Register.vue'
import ForgotPassword from '../pages/auth/ForgotPassword.vue'

// App pages
import Dashboard from '../pages/app/Dashboard.vue'
import Upload from '../pages/app/Upload.vue'
import Analysis from '../pages/app/Analysis.vue'
import Reports from '../pages/app/Reports.vue'
import Patients from '../pages/app/Patients.vue'
import ResearchApp from '../pages/app/ResearchApp.vue'
import Settings from '../pages/app/Settings.vue'
import Admin from '../pages/app/Admin.vue'

const routes = [
  // Public marketing pages with AppLayout navbar/footer
  {
    path: '/',
    component: AppLayout,
    children: [
      { path: '', name: 'home', component: Home },
      { path: 'about', name: 'about', component: About },
      { path: 'contact', name: 'contact', component: Contact },
      { path: 'platform', name: 'platform', component: Platform },
      { path: 'research', name: 'research', component: ResearchPublic }
    ]
  },

  // Guest-only auth routes
  { path: '/login', name: 'login', component: Login, meta: { guest: true } },
  { path: '/register', name: 'register', component: Register, meta: { guest: true } },
  { path: '/forgot-password', name: 'forgot-password', component: ForgotPassword, meta: { guest: true } },

  // Protected app routes
  {
    path: '/app',
    component: DashboardLayout,
    meta: { requiresAuth: true },
    children: [
      { path: '', name: 'dashboard', component: Dashboard, meta: { title: 'Clinical Dashboard' } },
      { path: 'upload', name: 'upload', component: Upload, meta: { title: 'Upload Scan', roles: ['radiologist', 'technician'] } },
      { path: 'analysis', name: 'analysis', component: Analysis, meta: { title: 'AI Analysis', roles: ['radiologist'] } },
      { path: 'reports', name: 'reports', component: Reports, meta: { title: 'Reports' } },
      { path: 'patients', name: 'patients', component: Patients, meta: { title: 'Patients' } },
      { path: 'research', name: 'research-app', component: ResearchApp, meta: { title: 'Research & AI', roles: ['researcher'] } },
      { path: 'settings', name: 'settings', component: Settings, meta: { title: 'Settings' } },
      { path: 'admin', name: 'admin', component: Admin, meta: { title: 'Admin Panel', roles: ['admin'] } },
    ]
  },

  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { top: 0 }
  }
})

// Navigation guard — role-based access control
router.beforeEach((to, from, next) => {
  const auth = useAuthStore()

  // Redirect authenticated users away from guest-only pages
  if (to.meta.guest && auth.isAuthenticated) {
    return next('/app')
  }

  // Require auth for protected routes
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return next('/login')
  }

  // Role-based route restriction
  if (to.meta.roles && auth.isAuthenticated) {
    if (auth.userRole.value !== 'admin' && auth.userRole.value !== 'researcher' && to.meta.roles.includes(auth.userRole.value)) {
      return next('/app') // redirect to dashboard if role is not allowed
    }
  }

  next()
})

export default router
