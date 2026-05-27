<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { Activity, Eye, EyeOff, ArrowRight, CheckCircle2, User, Loader2, AlertCircle } from 'lucide-vue-next'

const router = useRouter()
const auth = useAuthStore()

const username = ref('')
const password = ref('')
const rememberMe = ref(false)
const showPassword = ref(false)
const isLoading = ref(false)
const error = ref('')

const handleLogin = async () => {
  if (!username.value || !password.value) {
    error.value = 'Please enter your credentials.'
    return
  }
  isLoading.value = true
  error.value = ''
  await new Promise(r => setTimeout(r, 600))
  const success = await auth.login(username.value, password.value)
  isLoading.value = false
  if (success) router.push('/app')
  else error.value = 'Invalid credentials. Please try again.'
}
</script>

<template>
  <div class="min-h-screen flex clinical-workspace overflow-hidden">
    <!-- Immersive clinical glow backdrops -->
    <div class="absolute top-[10%] left-[5%] w-[400px] h-[400px] bg-teal-500/5 rounded-full blur-[100px] pointer-events-none"></div>

    <!-- LEFT — Clinical Visual Panel (Light themed) -->
    <div class="hidden lg:flex flex-col justify-between w-1/2 p-12 relative z-10 border-r border-slate-200/50 bg-white/40 backdrop-blur-sm">
      
      <!-- Logo -->
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-teal-500 to-sky-600 flex items-center justify-center shadow-md">
          <Activity class="w-5 h-5 text-white" />
        </div>
        <div>
          <div class="font-black text-slate-800 text-lg tracking-tight">
            LiverSeg<span class="bg-gradient-to-r from-teal-600 to-sky-500 bg-clip-text text-transparent">AI</span>
          </div>
          <div class="text-[10px] text-slate-400 font-bold uppercase tracking-widest">Clinical Imaging Platform</div>
        </div>
      </div>

      <!-- Center graphic (Light Mode CT scan illustration) -->
      <div class="flex flex-col items-center">
        <!-- CT Scanner Ring Mockup -->
        <div class="relative w-72 h-72 flex items-center justify-center">
          <div class="absolute inset-0 rounded-full border border-teal-500/10 animate-pulse"></div>
          <div class="absolute inset-4 rounded-full border border-slate-200/60"></div>
          <div class="absolute inset-8 rounded-full border border-sky-500/5"></div>

          <!-- Scanning beam effect -->
          <div class="absolute inset-0 rounded-full overflow-hidden">
            <div class="scan-beam opacity-40"></div>
          </div>

          <!-- Center scan canvas -->
          <div class="w-44 h-44 rounded-full bg-slate-900 border border-slate-850 flex items-center justify-center shadow-inner relative overflow-hidden">
            <div class="absolute inset-0 bg-[radial-gradient(rgba(255,255,255,0.015)_1px,transparent_1px)] bg-[size:10px_10px] pointer-events-none"></div>
            
            <svg viewBox="0 0 100 100" class="w-32 h-32 opacity-95">
              <!-- Body boundary -->
              <circle cx="50" cy="50" r="42" fill="none" stroke="#27272a" stroke-width="0.8" />
              <path 
                d="M16,50 Q13,32 35,26 Q60,21 63,35 Q66,50 58,62 Q45,72 32,68 Q23,64 16,50 Z" 
                fill="#0c0c0e" 
                stroke="#27272a" 
                stroke-width="0.6" 
              />
              
              <!-- Liver contour -->
              <path 
                d="M19,50 Q16,35 35,29 Q58,24 61,36 Q64,50 56,60 Q45,69 33,66 Q24,63 19,50 Z" 
                fill="rgba(20, 184, 166, 0.25)" 
                stroke="#14b8a6" 
                stroke-width="1.0" 
              />

              <!-- Lesion -->
              <circle cx="34" cy="42" r="4.5" fill="rgba(239, 68, 68, 0.45)" stroke="#ef4444" stroke-width="0.5" />
            </svg>
          </div>

          <!-- Labels -->
          <div class="absolute top-2 left-1/2 -translate-x-1/2 text-[9px] font-mono text-teal-600 font-bold uppercase tracking-widest">Axial CT</div>
          <div class="absolute bottom-2 left-1/2 -translate-x-1/2 text-[9px] font-mono text-slate-400 font-bold">512 × 512 px</div>
          <div class="absolute left-2 top-1/2 -translate-y-1/2 text-[9px] font-mono text-slate-400 font-bold">R</div>
          <div class="absolute right-2 top-1/2 -translate-y-1/2 text-[9px] font-mono text-slate-400 font-bold">L</div>
        </div>

        <!-- Metrics Row -->
        <div class="flex gap-8 mt-10">
          <div class="text-center">
            <div class="text-2xl font-black text-slate-800">95.8%</div>
            <div class="text-[9px] text-slate-400 uppercase tracking-wider font-bold">Dice Score</div>
          </div>
          <div class="w-px bg-slate-200"></div>
          <div class="text-center">
            <div class="text-2xl font-black text-slate-800">3.24s</div>
            <div class="text-[9px] text-slate-400 uppercase tracking-wider font-bold">Inference</div>
          </div>
          <div class="w-px bg-slate-200"></div>
          <div class="text-center">
            <div class="text-2xl font-black text-slate-800">100%</div>
            <div class="text-[9px] text-slate-400 uppercase tracking-wider font-bold">HIPAA Secure</div>
          </div>
        </div>
      </div>

      <!-- Footer check points -->
      <div class="space-y-3">
        <div 
          v-for="f in [
            'AI-powered liver & lesion segmentations',
            'PACS router integration for volumetric scans',
            'Secure database integration via Django & PostgreSQL'
          ]"
          :key="f"
          class="flex items-center gap-2.5 text-[11px] text-slate-500 font-semibold"
        >
          <CheckCircle2 class="w-4 h-4 text-teal-500 flex-shrink-0" />
          {{ f }}
        </div>
      </div>
    </div>

    <!-- RIGHT — Auth Form -->
    <div class="flex-1 flex items-center justify-center p-6 relative z-10">
      <div class="frosted-glass-panel w-full max-w-md p-8 sm:p-10 shadow-xl border border-slate-200/60 bg-white/70">

        <!-- Mobile Logo -->
        <div class="lg:hidden flex items-center gap-2.5 mb-8">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-teal-500 to-sky-600 flex items-center justify-center">
            <Activity class="w-4 h-4 text-white" />
          </div>
          <span class="font-black text-slate-800 text-sm">
            LiverSeg<span class="bg-gradient-to-r from-teal-600 to-sky-500 bg-clip-text text-transparent">AI</span>
          </span>
        </div>

        <div class="mb-7">
          <h2 class="text-xl font-black text-slate-900 tracking-tight">Clinical Sign-In</h2>
          <p class="text-xs text-slate-500 font-semibold mt-1">Access your radiology workspace</p>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label class="block text-[9px] font-bold uppercase tracking-wider text-slate-500 mb-1.5">Username</label>
            <input
              v-model="username"
              type="text"
              placeholder="dr_smith"
              class="clinical-input w-full px-3.5 py-2.5 text-xs font-semibold"
            />
          </div>

          <div>
            <label class="block text-[9px] font-bold uppercase tracking-wider text-slate-500 mb-1.5">Password</label>
            <div class="relative">
              <input
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="••••••••"
                class="clinical-input w-full px-3.5 py-2.5 text-xs font-semibold pr-10"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
              >
                <EyeOff v-if="showPassword" class="w-4 h-4" />
                <Eye v-else class="w-4 h-4" />
              </button>
            </div>
          </div>

          <div class="flex items-center justify-between">
            <label class="flex items-center gap-2 text-xs font-semibold text-slate-600 cursor-pointer select-none">
              <input v-model="rememberMe" type="checkbox" class="rounded border-slate-300 text-teal-600 focus:ring-teal-500" />
              Remember me
            </label>
            <router-link :to="{ path: '/forgot-password', query: { username: username } }" class="text-xs font-bold text-teal-650 hover:text-teal-700">
              Forgot password?
            </router-link>
          </div>

          <!-- Error Alert -->
          <div v-if="error" class="flex items-center gap-2 p-3 bg-rose-50 border border-rose-250 border-rose-100 rounded-xl text-xs text-rose-700 font-semibold">
            <AlertCircle class="w-4 h-4 flex-shrink-0" />
            {{ error }}
          </div>

          <button
            type="submit"
            :disabled="isLoading"
            class="clinical-btn-primary w-full flex items-center justify-center gap-2 py-3 rounded-xl text-xs font-bold uppercase tracking-wider active-shrink"
          >
            <Loader2 v-if="isLoading" class="w-4 h-4 animate-spin" />
            <span v-else class="flex items-center gap-2">Sign In <ArrowRight class="w-4 h-4" /></span>
          </button>
        </form>

        <p class="text-center text-xs text-slate-500 font-semibold mt-6">
          No account?
          <router-link to="/register" class="text-teal-650 font-bold hover:text-teal-700 ml-1">Create workspace</router-link>
        </p>
      </div>
    </div>
  </div>
</template>
