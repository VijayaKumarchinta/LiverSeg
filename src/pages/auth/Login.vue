<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { Activity, Eye, EyeOff, ArrowRight, Shield, Stethoscope, Brain, User, Loader2, Wrench, AlertCircle } from 'lucide-vue-next'

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
  await new Promise(r => setTimeout(r, 900))
  const success = await auth.login(username.value, password.value)
  isLoading.value = false
  if (success) router.push('/app')
  else error.value = 'Invalid credentials. Please try again.'
}


</script>

<template>
  <div class="min-h-screen flex auth-bg">

    <!-- LEFT — Clinical Visual Panel -->
    <div class="hidden lg:flex flex-col justify-between w-1/2 p-12 relative z-10">

      <!-- Logo -->
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-teal-500 to-sky-600 flex items-center justify-center shadow-lg">
          <Activity class="w-5 h-5 text-white" />
        </div>
        <div>
          <div class="font-black text-white text-lg tracking-tight">
            LiverSeg<span class="bg-gradient-to-r from-teal-400 to-sky-400 bg-clip-text text-transparent">AI</span>
          </div>
          <div class="text-[10px] text-slate-500 font-semibold uppercase tracking-widest">Clinical Imaging Platform</div>
        </div>
      </div>

      <!-- Center graphic -->
      <div class="flex flex-col items-center">
        <!-- CT Scanner Ring -->
        <div class="relative w-72 h-72">
          <div class="absolute inset-0 rounded-full border border-teal-500/20 animate-pulse"></div>
          <div class="absolute inset-4 rounded-full border border-teal-500/15"></div>
          <div class="absolute inset-8 rounded-full border border-sky-500/10"></div>

          <!-- Scanning beam -->
          <div class="absolute inset-0 rounded-full overflow-hidden">
            <div class="scan-beam opacity-60"></div>
          </div>

          <!-- Center piece -->
          <div class="absolute inset-0 flex items-center justify-center">
            <div class="w-40 h-40 rounded-full bg-black/40 border border-teal-500/20 flex items-center justify-center backdrop-blur-sm">
              <svg viewBox="0 0 100 100" class="w-28 h-28">
                <!-- Body outline -->
                <ellipse cx="50" cy="50" rx="35" ry="38" fill="#0a0f1a" stroke="#1e293b" stroke-width="1" />
                <!-- Liver -->
                <path d="M 46,35 C 32,32 20,38 20,50 C 20,60 26,68 35,70 C 43,67 46,58 46,48 C 46,38 50,34 46,35 Z"
                  fill="#1d2535" stroke="#14b8a6" stroke-width="1.2" />
                <!-- AI contour -->
                <path d="M 46,35 C 32,32 20,38 20,50 C 20,60 26,68 35,70 C 43,67 46,58 46,48 C 46,38 50,34 46,35 Z"
                  fill="rgba(20,184,166,0.35)" stroke="#14b8a6" stroke-width="0.8" />
                <!-- Lesion marker -->
                <circle cx="28" cy="52" r="4" fill="rgba(239,68,68,0.5)" stroke="#ef4444" stroke-width="0.6" />
                <!-- Spine -->
                <ellipse cx="50" cy="72" rx="5" ry="3" fill="#1e293b" stroke="#e2e8f0" stroke-width="0.7" />
              </svg>
            </div>
          </div>

          <!-- Metric labels around ring -->
          <div class="absolute top-2 left-1/2 -translate-x-1/2 text-[9px] font-mono text-teal-400 font-bold">AXIAL</div>
          <div class="absolute bottom-2 left-1/2 -translate-x-1/2 text-[9px] font-mono text-slate-500 font-bold">512×512</div>
          <div class="absolute left-2 top-1/2 -translate-y-1/2 text-[9px] font-mono text-slate-500 font-bold">R</div>
          <div class="absolute right-2 top-1/2 -translate-y-1/2 text-[9px] font-mono text-slate-500 font-bold">L</div>
        </div>

        <!-- Stats row -->
        <div class="flex gap-6 mt-8">
          <div class="text-center">
            <div class="text-2xl font-black text-white">95.8%</div>
            <div class="text-[9px] text-slate-500 uppercase tracking-widest font-bold">Dice Score</div>
          </div>
          <div class="w-px bg-slate-800"></div>
          <div class="text-center">
            <div class="text-2xl font-black text-white">3.2s</div>
            <div class="text-[9px] text-slate-500 uppercase tracking-widest font-bold">Inference</div>
          </div>
          <div class="w-px bg-slate-800"></div>
          <div class="text-center">
            <div class="text-2xl font-black text-white">HIPAA</div>
            <div class="text-[9px] text-slate-500 uppercase tracking-widest font-bold">Compliant</div>
          </div>
        </div>
      </div>

      <!-- Feature bullets -->
      <div class="space-y-3">
        <div v-for="f in ['AI-powered liver segmentation · 3D Attention U-Net', 'DICOM / NIfTI volumetric processing pipeline', 'Radiologist review & structured report generation']"
          :key="f"
          class="flex items-center gap-2.5 text-[11px] text-slate-400 font-medium"
        >
          <div class="w-1.5 h-1.5 rounded-full bg-teal-500 flex-shrink-0"></div>
          {{ f }}
        </div>
      </div>
    </div>

    <!-- RIGHT — Auth Form -->
    <div class="flex-1 flex items-center justify-center p-6 relative z-10">
      <div class="auth-card w-full max-w-md p-8">

        <!-- Mobile logo -->
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
          <p class="text-xs text-slate-500 font-medium mt-1">Access your radiology workspace</p>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label class="section-title block mb-1.5">Username</label>
            <input
              v-model="username"
              type="text"
              placeholder="dr_smith"
              class="clinical-input w-full px-3.5 py-2.5 text-sm"
            />
          </div>

          <div>
            <label class="section-title block mb-1.5">Password</label>
            <div class="relative">
              <input
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="••••••••"
                class="clinical-input w-full px-3.5 py-2.5 text-sm pr-10"
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
            <label class="flex items-center gap-2 text-xs font-medium text-slate-600 cursor-pointer">
              <input v-model="rememberMe" type="checkbox" class="rounded border-slate-300 text-teal-600" />
              Remember me
            </label>
            <router-link :to="{ path: '/forgot-password', query: { username: username } }" class="text-xs font-semibold text-teal-600 hover:text-teal-700">
              Forgot password?
            </router-link>
          </div>

          <!-- Error -->
          <div v-if="error" class="flex items-center gap-2 p-3 bg-rose-50 border border-rose-200 rounded-lg text-xs text-rose-700 font-medium">
            <AlertCircle class="w-3.5 h-3.5 flex-shrink-0" />
            {{ error }}
          </div>

          <button
            type="submit"
            :disabled="isLoading"
            class="clinical-btn-primary w-full flex items-center justify-center gap-2 py-2.5 rounded-xl text-sm font-bold tracking-wide"
          >
            <Loader2 v-if="isLoading" class="w-4 h-4 animate-spin" />
            <span v-else class="flex items-center gap-2">Sign In <ArrowRight class="w-4 h-4" /></span>
          </button>
        </form>



        <p class="text-center text-xs text-slate-500 font-medium mt-6">
          No account?
          <router-link to="/register" class="text-teal-600 font-bold hover:text-teal-700 ml-1">Create workspace</router-link>
        </p>
      </div>
    </div>
  </div>
</template>
