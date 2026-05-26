<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useAppState } from '../../composables/useAppState'
import { useAuthStore } from '../../stores/auth'
import { Save, Server, Wifi, Info, Bell, User, Check, RefreshCw, Eye, EyeOff } from 'lucide-vue-next'

const { pacsConfig, fetchPacsConfig, updatePacs } = useAppState()
const auth = useAuthStore()

const pacsForm = reactive({
  aeTitle: '',
  port: 104,
  ipAddress: '',
  compression: 'No Compression',
  autoRoute: false,
  validateOnReceive: false
})

onMounted(async () => {
  await fetchPacsConfig()
  Object.assign(pacsForm, pacsConfig.value)
})
const saved = ref(false)
const savePacs = () => {
  updatePacs({ ...pacsForm })
  saved.value = true
  setTimeout(() => saved.value = false, 2500)
}

const profileForm = reactive({
  name: auth.userName,
  username: auth.userUsername,
})

const notifSettings = reactive({
  segmentationComplete: true,
  reportSigned: true,
  platformAlerts: true,
  pacsSync: false,
  weeklyDigest: true,
})

const platformInfo = [
  { label: 'Platform Version', value: 'LiversegAI v2.5.0' },
  { label: 'AI Engine', value: 'MONAI v1.4.2' },
  { label: 'Model Weights', value: 'attn_unet_liver_v1.4.pt' },
  { label: 'DICOM Library', value: 'pydicom 2.4.3' },
  { label: 'GPU Runtime', value: 'CUDA 12.1 · cuDNN 8.9' },
]
</script>

<template>
  <div class="space-y-5 animate-fade-in-up max-w-5xl">

    <!-- Header -->
    <div class="frosted-glass-panel p-4">
      <div class="section-title">Configuration</div>
      <h2 class="text-sm font-black text-slate-800 mt-0.5">Workstation Settings</h2>
      <p class="text-[10px] text-slate-500 font-medium mt-0.5">PACS configuration, user preferences, notifications, and platform info</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">

      <!-- PACS Configuration -->
      <div class="frosted-glass-panel p-5 space-y-4">
        <div class="flex items-center gap-2 pb-3 border-b border-slate-200/50">
          <Server class="w-4 h-4 text-teal-600" />
          <div>
            <div class="section-title">DICOM / PACS Node</div>
            <div class="text-xs font-bold text-slate-800">Network Configuration</div>
          </div>
        </div>

        <div class="space-y-3">
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="section-title block mb-1.5">AE Title</label>
              <input v-model="pacsForm.aeTitle" type="text" class="clinical-input w-full px-3 py-2 text-xs font-mono" />
            </div>
            <div>
              <label class="section-title block mb-1.5">Port</label>
              <input v-model.number="pacsForm.port" type="number" class="clinical-input w-full px-3 py-2 text-xs font-mono" />
            </div>
          </div>
          <div>
            <label class="section-title block mb-1.5">IP Address</label>
            <input v-model="pacsForm.ipAddress" type="text" class="clinical-input w-full px-3 py-2 text-xs font-mono" />
          </div>
          <div>
            <label class="section-title block mb-1.5">Compression</label>
            <select v-model="pacsForm.compression" class="clinical-input w-full px-3 py-2 text-xs">
              <option>Lossless JPEG-LS</option>
              <option>JPEG 2000 Lossless</option>
              <option>No Compression</option>
            </select>
          </div>
          <div class="space-y-2 pt-1">
            <label v-for="(key, label) in { 'Auto-route ingested scans': 'autoRoute', 'Validate on DICOM receive': 'validateOnReceive' }" :key="key"
              class="flex items-center justify-between py-2 border-b border-slate-100/60 last:border-0 cursor-pointer"
            >
              <span class="text-[10px] font-semibold text-slate-700">{{ label }}</span>
              <button
                @click="pacsForm[key] = !pacsForm[key]"
                :class="['w-9 h-5 rounded-full border transition-all relative', pacsForm[key] ? 'bg-teal-500 border-teal-500' : 'bg-slate-200 border-slate-300']"
              >
                <span :class="['absolute top-0.5 w-4 h-4 bg-white rounded-full shadow transition-all', pacsForm[key] ? 'left-4' : 'left-0.5']"></span>
              </button>
            </label>
          </div>
        </div>

        <button @click="savePacs" class="clinical-btn-primary w-full flex items-center justify-center gap-2 py-2.5 rounded-xl text-xs font-bold active-shrink">
          <Check v-if="saved" class="w-4 h-4" />
          <Save v-else class="w-4 h-4" />
          {{ saved ? 'Saved Successfully!' : 'Save PACS Config' }}
        </button>
      </div>

      <!-- User Profile -->
      <div class="frosted-glass-panel p-5 space-y-4">
        <div class="flex items-center gap-2 pb-3 border-b border-slate-200/50">
          <User class="w-4 h-4 text-sky-600" />
          <div>
            <div class="section-title">User Profile</div>
            <div class="text-xs font-bold text-slate-800">Account Information</div>
          </div>
        </div>

        <div class="flex items-center gap-3 p-3 bg-slate-50/60 rounded-xl border border-slate-200/40">
          <div class="w-12 h-12 rounded-full bg-gradient-to-br from-teal-500 to-sky-600 flex items-center justify-center text-white font-black text-sm flex-shrink-0">
            {{ auth.userInitials }}
          </div>
          <div>
            <div class="text-sm font-black text-slate-800">{{ auth.userName }}</div>
            <div class="text-[9px] font-semibold text-teal-600 capitalize">{{ auth.userRole }}</div>
            <div class="text-[9px] text-slate-400 font-medium">@{{ auth.userUsername }}</div>
          </div>
        </div>

        <div class="space-y-3">
          <div v-for="(val, label) in { 'Full Name': profileForm.name, 'Username': profileForm.username }" :key="label">
            <label class="section-title block mb-1.5">{{ label }}</label>
            <input :value="val" type="text" class="clinical-input w-full px-3 py-2 text-xs" readonly />
          </div>
        </div>
      </div>

      <!-- Notifications -->
      <div class="frosted-glass-panel p-5 space-y-4">
        <div class="flex items-center gap-2 pb-3 border-b border-slate-200/50">
          <Bell class="w-4 h-4 text-amber-500" />
          <div>
            <div class="section-title">Notifications</div>
            <div class="text-xs font-bold text-slate-800">Alert Preferences</div>
          </div>
        </div>

        <div class="space-y-1">
          <label v-for="(key, label) in {
            'Segmentation complete': 'segmentationComplete',
            'Report signed': 'reportSigned',
            'Platform alerts': 'platformAlerts',
            'PACS sync events': 'pacsSync',
            'Weekly digest email': 'weeklyDigest'
          }" :key="key" class="flex items-center justify-between py-2.5 border-b border-slate-100/60 last:border-0 cursor-pointer">
            <span class="text-[10px] font-semibold text-slate-700">{{ label }}</span>
            <button
              @click="notifSettings[key] = !notifSettings[key]"
              :class="['w-9 h-5 rounded-full border transition-all relative', notifSettings[key] ? 'bg-teal-500 border-teal-500' : 'bg-slate-200 border-slate-300']"
            >
              <span :class="['absolute top-0.5 w-4 h-4 bg-white rounded-full shadow transition-all', notifSettings[key] ? 'left-4' : 'left-0.5']"></span>
            </button>
          </label>
        </div>
      </div>

      <!-- Platform Info -->
      <div class="frosted-glass-panel p-5 space-y-4">
        <div class="flex items-center gap-2 pb-3 border-b border-slate-200/50">
          <Info class="w-4 h-4 text-purple-600" />
          <div>
            <div class="section-title">Platform</div>
            <div class="text-xs font-bold text-slate-800">Platform Information</div>
          </div>
        </div>

        <div>
          <div class="section-title mb-2">Platform Details</div>
          <div class="space-y-1.5">
            <div v-for="s in platformInfo" :key="s.label" class="flex justify-between py-1.5 border-b border-slate-100/50 last:border-0 text-[10px]">
              <span class="text-slate-500 font-medium">{{ s.label }}</span>
              <span class="font-bold text-slate-800">{{ s.value }}</span>
            </div>
          </div>
        </div>

        <div class="flex items-center gap-1.5 px-3 py-2 rounded-lg bg-teal-50 border border-teal-100">
          <div class="w-2 h-2 rounded-full bg-teal-500"></div>
          <span class="text-[9px] font-bold text-teal-700">All services operational · HIPAA compliant</span>
        </div>
      </div>

    </div>
  </div>
</template>
