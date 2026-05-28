<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Activity, User, KeyRound, ArrowRight, ArrowLeft, Loader2, AlertCircle } from 'lucide-vue-next'
import api from '../../api'

const router = useRouter()
const route = useRoute()

const username = ref('')
const newPassword = ref('')
const isSubmitted = ref(false)
const isLoading = ref(false)
const error = ref('')

onMounted(() => {
  if (route.query.username) {
    username.value = route.query.username
  }
})

const handleReset = async () => {
  if (!username.value || !newPassword.value) {
    error.value = 'Please enter both username and new password.'
    return
  }
  
  isLoading.value = true
  error.value = ''
  
  try {
    await api.post('/users/reset_password/', {
      username: username.value,
      new_password: newPassword.value
    })
    isSubmitted.value = true
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to reset password.'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="relative min-h-screen flex items-center justify-center p-6 clinical-workspace overflow-hidden">
    <!-- Immersive clinical glow backdrops -->
    <div class="absolute top-[10%] right-[10%] w-[400px] h-[400px] bg-teal-500/5 rounded-full blur-[100px] pointer-events-none"></div>
    <div class="absolute bottom-[10%] left-[10%] w-[400px] h-[400px] bg-sky-500/5 rounded-full blur-[100px] pointer-events-none"></div>

    <div class="w-full max-w-md frosted-glass-panel p-8 sm:p-10 shadow-xl border border-slate-200/60 bg-white/70 relative z-10 space-y-6">
      
      <!-- Brand Logo Header -->
      <div class="text-center space-y-3">
        <router-link to="/" class="inline-flex items-center gap-2 group">
          <div class="flex items-center justify-center w-9 h-9 rounded-lg bg-gradient-to-tr from-teal-500 to-sky-600 text-white shadow-sm">
            <Activity class="w-5 h-5" />
          </div>
          <span class="text-lg font-black text-slate-800 tracking-tight">
            LiverSeg<span class="bg-gradient-to-r from-teal-600 to-sky-600 bg-clip-text text-transparent">AI</span>
          </span>
        </router-link>
        <h2 class="text-xl font-black text-slate-900 tracking-tight">Reset Password</h2>
        <p class="text-xs text-slate-500 font-semibold">Update your clinical workspace credentials directly.</p>
      </div>

      <!-- Success display -->
      <div v-if="isSubmitted" class="p-5 bg-teal-50/60 border border-teal-200/55 rounded-2xl text-center space-y-3">
        <div class="text-xs text-teal-800 font-black">Password Reset Successful</div>
        <p class="text-[11px] text-teal-600 font-semibold leading-relaxed">
          Your credentials have been securely updated in the database. You can now access your workspace with the new password.
        </p>
        <router-link to="/login" class="inline-flex items-center justify-center gap-1.5 text-xs text-teal-700 hover:text-teal-900 font-bold pt-2">
          <ArrowLeft class="w-3.5 h-3.5" /> Return to Login
        </router-link>
      </div>

      <!-- Reset Form -->
      <form v-else class="space-y-4" @submit.prevent="handleReset">
        <div>
          <label class="block text-[9px] font-bold uppercase tracking-wider text-slate-500 mb-1.5">Username</label>
          <div class="relative">
            <User class="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input 
              v-model="username"
              type="text" 
              placeholder="dr_smith" 
              class="clinical-input w-full pl-10 pr-4 py-2.5 text-xs font-semibold"
              required
            />
          </div>
        </div>

        <div>
          <label class="block text-[9px] font-bold uppercase tracking-wider text-slate-500 mb-1.5">New Password</label>
          <div class="relative">
            <KeyRound class="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input 
              v-model="newPassword"
              type="password" 
              placeholder="••••••••" 
              class="clinical-input w-full pl-10 pr-4 py-2.5 text-xs font-semibold"
              required
              minlength="6"
            />
          </div>
        </div>

        <!-- Error -->
        <div v-if="error" class="flex items-center gap-2 p-3 bg-rose-50 border border-rose-100 rounded-xl text-xs text-rose-700 font-semibold">
          <AlertCircle class="w-4 h-4 flex-shrink-0" />
          {{ error }}
        </div>

        <button 
          type="submit" 
          :disabled="isLoading"
          class="clinical-btn-primary w-full flex items-center justify-center gap-2 py-3 rounded-xl text-xs font-bold uppercase tracking-wider active-shrink"
        >
          <Loader2 v-if="isLoading" class="w-4 h-4 animate-spin" />
          <span v-else class="flex items-center gap-2">
            Reset Password
            <ArrowRight class="w-4 h-4" />
          </span>
        </button>

        <div class="text-center pt-2">
          <router-link to="/login" class="inline-flex items-center justify-center gap-1 text-xs font-bold text-slate-500 hover:text-slate-700">
            <ArrowLeft class="w-3.5 h-3.5" /> Back to Login
          </router-link>
        </div>
      </form>

    </div>
  </div>
</template>
