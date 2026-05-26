<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { Activity, Eye, EyeOff, ArrowRight, Loader2, AlertCircle } from 'lucide-vue-next'

const router = useRouter()
const auth = useAuthStore()

const name = ref('')
const username = ref('')
const hospital = ref('')
const role = ref('radiologist')
const password = ref('')
const showPassword = ref(false)
const isLoading = ref(false)
const error = ref('')

const roles = ['radiologist','admin','researcher','clinician','technician']

const handleRegister = async () => {
  if (!name.value || !username.value || !password.value) {
    error.value = 'Please fill in all required fields.'
    return
  }
  isLoading.value = true
  error.value = ''
  await new Promise(r => setTimeout(r, 800))
  const success = await auth.register(name.value, username.value, hospital.value || 'St. Luke Medical Center', role.value, password.value)
  isLoading.value = false
  if (success) {
    router.push('/app')
  } else {
    error.value = 'Registration failed. Please try again.'
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center auth-bg p-6">
    <div class="auth-card w-full max-w-md p-8">

      <div class="flex items-center gap-2.5 mb-7">
        <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-teal-500 to-sky-600 flex items-center justify-center">
          <Activity class="w-4 h-4 text-white" />
        </div>
        <span class="font-black text-slate-800 text-sm">
          LiverSeg<span class="bg-gradient-to-r from-teal-600 to-sky-500 bg-clip-text text-transparent">AI</span>
        </span>
      </div>

      <div class="mb-6">
        <h2 class="text-xl font-black text-slate-900">Create Workspace</h2>
        <p class="text-xs text-slate-500 font-medium mt-1">Register your clinical account</p>
      </div>

      <form @submit.prevent="handleRegister" class="space-y-4">
        <div class="grid grid-cols-2 gap-3">
          <div class="col-span-2">
            <label class="section-title block mb-1.5">Full Name *</label>
            <input v-model="name" type="text" placeholder="Dr. Jane Smith" class="clinical-input w-full px-3.5 py-2.5 text-sm" />
          </div>
          <div class="col-span-2">
            <label class="section-title block mb-1.5">Username *</label>
            <input v-model="username" type="text" placeholder="dr_smith" class="clinical-input w-full px-3.5 py-2.5 text-sm" />
          </div>
          <div>
            <label class="section-title block mb-1.5">Clinical Role</label>
            <select v-model="role" class="clinical-input w-full px-3 py-2.5 text-sm capitalize">
              <option v-for="r in roles" :key="r" :value="r" class="capitalize">{{ r }}</option>
            </select>
          </div>
          <div>
            <label class="section-title block mb-1.5">Password *</label>
            <div class="relative">
              <input v-model="password" :type="showPassword ? 'text' : 'password'" placeholder="••••••••" class="clinical-input w-full px-3.5 py-2.5 text-sm pr-9" />
              <button type="button" @click="showPassword = !showPassword" class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400">
                <EyeOff v-if="showPassword" class="w-4 h-4" />
                <Eye v-else class="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>

        <div v-if="error" class="flex items-center gap-2 p-3 bg-rose-50 border border-rose-200 rounded-lg text-xs text-rose-700 font-medium">
          <AlertCircle class="w-3.5 h-3.5" />{{ error }}
        </div>

        <button type="submit" :disabled="isLoading" class="clinical-btn-primary w-full flex items-center justify-center gap-2 py-2.5 rounded-xl text-sm font-bold">
          <Loader2 v-if="isLoading" class="w-4 h-4 animate-spin" />
          <span v-else class="flex items-center gap-2">Create Account <ArrowRight class="w-4 h-4" /></span>
        </button>
      </form>

      <p class="text-center text-xs text-slate-500 font-medium mt-5">
        Already have access?
        <router-link to="/login" class="text-teal-600 font-bold hover:text-teal-700 ml-1">Sign in</router-link>
      </p>
    </div>
  </div>
</template>
