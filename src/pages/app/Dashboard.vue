<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAppState } from '../../composables/useAppState'
import { useAuthStore } from '../../stores/auth'
import { 
  Users, 
  Activity, 
  FileText, 
  TrendingUp, 
  ArrowRight, 
  Clock, 
  CheckCircle, 
  Loader2,
  Scan,
  Sliders,
  Play,
  RotateCcw,
  Check,
  Shield,
  ShieldAlert,
  Server,
  Database,
  LineChart,
  BookOpen,
  Heart,
  UploadCloud,
  Layers,
  HeartPulse,
  BrainCircuit,
  Settings,
  AlertCircle
} from 'lucide-vue-next'

const router = useRouter()
const auth = useAuthStore()
const { 
  patients, 
  activities, 
  activePatient,
  selectPatient, 
  runSegmentation,
  isInferenceRunning,
  inferenceProgress,
  inferenceStage,
  uploadQueue,
  simulateUpload
} = useAppState()

// ==========================================
// 1. RADIOLOGIST VARIABLES
// ==========================================
const currentSlice = ref(10)
const maskOpacity = ref(60)

const sliceData = computed(() => {
  if (!activePatient.value || !activePatient.value.slices) return null
  return activePatient.value.slices[currentSlice.value]
})

const handleTriggerSegment = () => {
  runSegmentation(activePatient.value.id)
}

const handleViewPatientDetails = () => {
  router.push('/app/analysis')
}

// Stats computations
const totalScans = computed(() => patients.value.length)
const completedScans = computed(() => patients.value.filter(p => p.status === 'Completed').length)
const activeQueue = computed(() => patients.value.filter(p => p.status === 'Analyzing' || p.status === 'Ready').length)

const avgDice = () => {
  const completed = patients.value.filter(p => p.metrics && p.metrics.dice !== '—')
  if (completed.length === 0) return '—'
  const sum = completed.reduce((acc, p) => acc + parseFloat(p.metrics.dice), 0)
  return (sum / completed.length).toFixed(1) + '%'
}

// ==========================================
// 2. HOSPITAL ADMIN VARIABLES
// ==========================================
const adminUsers = ref([])

const adminLogs = ref([])

// ==========================================
// 3. AI RESEARCH VARIABLES
// ==========================================
const activeModels = ref([])

const datasetDistribution = ref([])

// ==========================================
// 4. CLINICIAN VARIABLES
// ==========================================
const clinicianTimeline = ref([])

const clinicianNotes = ref("")

// ==========================================
// 5. TECHNICIAN VARIABLES
// ==========================================
const preprocQueue = ref([])

const assignName = ref('PT-8841-K')
const assignModality = ref('CT')
const assignAge = ref(45)

const handleAssign = () => {
  simulateUpload('CT_SCAN_' + assignName.value + '.nii.gz', '42.0 MB', 'nifti')
  alert(`Assigned and queued ${assignName.value} modality to active workspace cache.`)
}
</script>

<template>
  <div class="space-y-6">

    <!-- ════════════════════════════════════════
         1. RADIOLOGIST WORKSPACE
         ════════════════════════════════════════ -->
    <div v-if="auth.userRole === 'radiologist'" class="space-y-6 animate-fade-in">
      
      <!-- Top indicators -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="frosted-glass-panel p-4 flex items-center justify-between">
          <div class="space-y-1">
            <div class="text-[9px] font-bold uppercase tracking-wider text-slate-400">Scan Database</div>
            <div class="text-xl font-extrabold text-slate-900">{{ totalScans }} Cases</div>
            <div class="text-[10px] text-slate-500 font-bold">{{ completedScans }} Completed &middot; {{ activeQueue }} Pending</div>
          </div>
          <div class="w-9 h-9 rounded-lg bg-teal-50 text-teal-650 flex items-center justify-center shadow-sm">
            <Users class="w-4.5 h-4.5" />
          </div>
        </div>

        <div class="frosted-glass-panel p-4 flex items-center justify-between">
          <div class="space-y-1">
            <div class="text-[9px] font-bold uppercase tracking-wider text-slate-400">Mean Dice Score</div>
            <div class="text-xl font-extrabold text-slate-900">{{ avgDice() }}</div>
            <div class="text-[10px] text-teal-600 font-bold flex items-center gap-1">
              <TrendingUp class="w-3 h-3" />
              <span>Exceeds QA threshold</span>
            </div>
          </div>
          <div class="w-9 h-9 rounded-lg bg-teal-50 text-teal-650 flex items-center justify-center shadow-sm">
            <Activity class="w-4.5 h-4.5" />
          </div>
        </div>

        <div class="frosted-glass-panel p-4 flex items-center justify-between">
          <div class="space-y-1">
            <div class="text-[9px] font-bold uppercase tracking-wider text-slate-400">Active Pipeline</div>
            <div class="text-xl font-extrabold text-slate-900">{{ activeQueue }} Running</div>
            <div class="text-[10px] text-slate-500 font-bold">Ingested from local PACS node</div>
          </div>
          <div class="w-9 h-9 rounded-lg bg-teal-50 text-teal-655 flex items-center justify-center shadow-sm">
            <Clock class="w-4.5 h-4.5" />
          </div>
        </div>

        <div class="frosted-glass-panel p-4 flex items-center justify-between">
          <div class="space-y-1">
            <div class="text-[9px] font-bold uppercase tracking-wider text-slate-400">Approved Reports</div>
            <div class="text-xl font-extrabold text-slate-900">{{ completedScans }} DICOM SR</div>
            <div class="text-[10px] text-slate-500 font-bold">100% digital trace compliance</div>
          </div>
          <div class="w-9 h-9 rounded-lg bg-teal-50 text-teal-655 flex items-center justify-center shadow-sm">
            <FileText class="w-4.5 h-4.5" />
          </div>
        </div>
      </div>

      <!-- Main grid splits -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        <!-- Left panel Case list -->
        <div class="lg:col-span-8 space-y-6">
          <div class="frosted-glass-panel flex flex-col justify-between overflow-hidden !p-0">
            <div>
              <div class="px-5 py-3.5 border-b border-slate-200/50 flex items-center justify-between bg-white/40">
                <h3 class="font-extrabold text-slate-800 text-xs tracking-tight uppercase">PACS Active Case List</h3>
                <span class="text-[9px] bg-white/80 border border-slate-200/60 px-2 py-0.5 rounded-full font-bold text-slate-500">Auto Sync: 104/DICOM</span>
              </div>

              <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse text-xs">
                  <thead>
                    <tr class="bg-slate-50/50 border-b border-slate-200/50 text-slate-500 font-bold">
                      <th class="px-5 py-2.5 font-bold text-[9px] uppercase tracking-wider">Patient Case</th>
                      <th class="px-5 py-2.5 font-bold text-[9px] uppercase tracking-wider">Modality</th>
                      <th class="px-5 py-2.5 font-bold text-[9px] uppercase tracking-wider">Scan Date</th>
                      <th class="px-5 py-2.5 font-bold text-[9px] uppercase tracking-wider">Status</th>
                      <th class="px-5 py-2.5 font-bold text-[9px] uppercase tracking-wider">Dice Score</th>
                      <th class="px-5 py-2.5"></th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-slate-100/50">
                    <tr 
                      v-for="p in patients" 
                      :key="p.id" 
                      @click="selectPatient(p.id)"
                      :class="[
                        'cursor-pointer transition-colors',
                        activePatient.id === p.id 
                          ? 'bg-teal-50/30 hover:bg-teal-50/40 border-l-4 border-teal-600 pl-4' 
                          : 'hover:bg-white/40 border-l-4 border-transparent'
                      ]"
                    >
                      <td class="px-5 py-3">
                        <div class="font-bold text-slate-850">{{ p.name }}</div>
                        <div class="text-[10px] text-slate-400 font-mono font-bold">{{ p.id }} &middot; {{ p.gender.substring(0,1) }}/{{ p.age }}y</div>
                      </td>
                      <td class="px-5 py-3 text-slate-600 font-bold">{{ p.modality }}</td>
                      <td class="px-5 py-3 text-slate-500 font-semibold">{{ p.scanDate }}</td>
                      <td class="px-5 py-3">
                        <span v-if="p.status === 'Completed'" class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[9px] font-bold bg-teal-50 border border-teal-100 text-teal-700">
                          <CheckCircle class="w-2.5 h-2.5" /> Completed
                        </span>
                        <span v-else-if="p.status === 'Analyzing'" class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[9px] font-bold bg-sky-50 border border-sky-100 text-sky-700 animate-pulse">
                          <Loader2 class="w-2.5 h-2.5 animate-spin" /> Ingesting...
                        </span>
                        <span v-else class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[9px] font-bold bg-amber-50 border border-amber-100 text-amber-700">
                          Ready for AI
                        </span>
                      </td>
                      <td class="px-5 py-3 font-mono font-bold text-slate-800">{{ p.metrics.dice }}</td>
                      <td class="px-5 py-3 text-right">
                        <button @click.stop="selectPatient(p.id); handleViewPatientDetails()" class="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-[9px] font-bold uppercase tracking-wider clinical-btn-secondary active-shrink">
                          Workspace <ArrowRight class="w-3 h-3" />
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <div class="frosted-glass-panel p-5 space-y-4">
            <h3 class="font-extrabold text-slate-800 text-xs tracking-tight uppercase border-b border-slate-200/50 pb-2.5">PACS Telemetry logs</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div v-for="act in activities" :key="act.id" class="flex gap-3 text-xs leading-normal p-2.5 bg-white/40 border border-slate-200/50 rounded-xl">
                <div class="w-1.5 h-1.5 rounded-full mt-1.5 flex-shrink-0" :class="act.type === 'success' ? 'bg-teal-500' : 'bg-sky-500'"></div>
                <div class="space-y-0.5">
                  <div class="font-bold text-slate-800">{{ act.action }}</div>
                  <div class="text-[10px] text-slate-500 leading-normal font-semibold">{{ act.details }}</div>
                  <div class="text-[9px] text-slate-400 font-bold">{{ act.time }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Visualizer Spotlight -->
        <div class="lg:col-span-4 space-y-6">
          <div v-if="activePatient" class="frosted-glass-panel p-4 flex flex-col justify-between space-y-4">
            <div class="border-b border-slate-200/50 pb-2 flex items-center justify-between">
              <div class="space-y-0.5">
                <span class="text-[9px] font-bold text-teal-650 text-teal-600 uppercase tracking-widest block">pacs view monitor</span>
                <h3 class="font-extrabold text-slate-900 text-sm tracking-tight leading-tight">Case: {{ activePatient.name }}</h3>
              </div>
              <span class="text-[9px] font-mono bg-white/70 border border-slate-200/60 text-slate-500 px-2 py-0.5 rounded font-bold">{{ activePatient.id }}</span>
            </div>

            <!-- CT SVG render viewport -->
            <div class="bg-black/95 rounded-xl border border-slate-800 p-3 relative flex items-center justify-center aspect-square select-none">
              <div class="absolute inset-0 bg-[radial-gradient(rgba(255,255,255,0.015)_1px,transparent_1px)] bg-[size:12px_12px] pointer-events-none"></div>
              
              <div class="absolute w-[92%] h-[92%] rounded-full border border-dashed border-slate-850/40 pointer-events-none flex items-center justify-center">
                <div class="w-[85%] h-[85%] rounded-full border border-slate-850/20"></div>
              </div>

              <!-- Orientation tags -->
              <div class="absolute top-2 text-[9px] font-bold font-mono text-slate-600">A</div>
              <div class="absolute bottom-2 text-[9px] font-bold font-mono text-slate-600">P</div>
              <div class="absolute left-2 text-[9px] font-bold font-mono text-slate-600">R</div>
              <div class="absolute right-2 text-[9px] font-bold font-mono text-slate-600">L</div>

              <svg viewBox="0 0 100 100" class="w-48 h-48 md:w-56 md:h-56">
                <!-- Spinal bone -->
                <g :transform="`translate(0, ${sliceData ? sliceData.liverY/10 : 0})`">
                  <path d="M 44,73.5 Q 50,69.5 56,73.5 Q 60,76.5 50,79.5 Q 40,76.5 44,73.5 Z" fill="#25252a" stroke="#efefef" stroke-width="0.8" />
                  <path d="M 50,78.5 L 50,82" stroke="#ffffff" stroke-width="1.2" />
                  <circle cx="50" cy="75" r="1.8" fill="#000000" stroke="#71717a" stroke-width="0.4" />
                </g>

                <!-- Rib arches -->
                <g stroke="#a1a1aa" stroke-width="0.9" fill="none" opacity="0.6">
                  <path d="M 26,24 Q 21,29 19,36" />
                  <path d="M 18,43 Q 17,49 18,55" />
                  <path d="M 74,24 Q 79,29 81,36" />
                  <path d="M 82,43 Q 83,49 82,55" />
                </g>

                <!-- duod / stomach -->
                <path v-if="currentSlice >= 2 && currentSlice <= 13" d="M 52,27 C 62,25 73,29 73,38 C 73,46 64,48 54,44 Z" fill="#121214" stroke="#3f3f46" stroke-width="0.5" />

                <!-- spleen -->
                <path v-if="currentSlice >= 4 && currentSlice <= 15" d="M 68,46 C 76,43 79,52 76,60 C 73,66 65,64 64,54 Z" fill="#18181c" stroke="#4b5563" stroke-width="0.5" />

                <!-- LIVER -->
                <path v-if="sliceData" :d="`M ${46 + sliceData.liverX},${30 + sliceData.liverY/2} C ${32 + sliceData.liverX},${26 + sliceData.liverY} 19,36 19,48 C 19,58 24,${66 - sliceData.liverY/2} ${32 + sliceData.liverX},${68 - sliceData.liverY/2} C ${42 + sliceData.liverX},${66 - sliceData.liverY} ${46 + sliceData.liverX},${56 - sliceData.liverY} ${46 + sliceData.liverX},${46 - sliceData.liverY} C ${46 + sliceData.liverX},${36 - sliceData.liverY} 50,32 ${46 + sliceData.liverX},${30 + sliceData.liverY/2} Z`" fill="#242429" stroke="#4b5563" stroke-width="0.6" />

                <!-- TEAL AI CONTOUR -->
                <path v-if="sliceData && activePatient.status === 'Completed'" :d="`M ${46 + sliceData.liverX},${30 + sliceData.liverY/2} C ${32 + sliceData.liverX},${26 + sliceData.liverY} 19,36 19,48 C 19,58 24,${66 - sliceData.liverY/2} ${32 + sliceData.liverX},${68 - sliceData.liverY/2} C ${42 + sliceData.liverX},${66 - sliceData.liverY} ${46 + sliceData.liverX},${56 - sliceData.liverY} ${46 + sliceData.liverX},${46 - sliceData.liverY} C ${46 + sliceData.liverX},${36 - sliceData.liverY} 50,32 ${46 + sliceData.liverX},${30 + sliceData.liverY/2} Z`" :fill="`rgba(20, 184, 166, ${maskOpacity / 100})`" stroke="#14b8a6" stroke-width="0.85" />

                <!-- Red Tumor Lesions -->
                <circle v-if="sliceData && sliceData.lesionSize > 0 && activePatient.status === 'Completed'" :cx="28 + sliceData.lesionX / 5" :cy="48 + sliceData.lesionY / 5" :r="sliceData.lesionSize * 15" fill="rgba(239, 68, 68, 0.45)" stroke="#ef4444" stroke-width="0.5" />
              </svg>

              <!-- Ingestion Telemetry overlay -->
              <div v-if="isInferenceRunning" class="absolute inset-0 bg-black/85 flex flex-col items-center justify-center p-4 text-center rounded-xl">
                <Loader2 class="w-6 h-6 animate-spin text-teal-500 mb-2" />
                <div class="text-[10px] font-mono text-teal-400 font-bold mb-1">{{ inferenceStage }}</div>
                <div class="w-2/3 bg-slate-800 h-1 rounded-full overflow-hidden">
                  <div class="bg-teal-500 h-full transition-all duration-200" :style="{ width: inferenceProgress + '%' }"></div>
                </div>
              </div>
            </div>

            <!-- Visualizer Actions & slider -->
            <div class="space-y-3">
              <div class="flex items-center justify-between text-[10px] font-bold text-slate-500">
                <span>SCAN SLICE SELECTION</span>
                <span>Slice {{ currentSlice + 1 }}/20</span>
              </div>
              <input v-model.number="currentSlice" type="range" min="0" max="19" class="w-full accent-teal-600 bg-slate-200 h-1.5 rounded-lg appearance-none cursor-pointer" />

              <div class="grid grid-cols-3 gap-2 text-center text-xs font-semibold pt-1">
                <div class="bg-slate-50/80 border border-slate-200/50 p-2 rounded-lg">
                  <div class="text-[9px] text-slate-400 uppercase font-bold">Dice Score</div>
                  <div class="text-sm font-extrabold text-teal-600 mt-0.5">{{ activePatient.metrics.dice }}</div>
                </div>
                <div class="bg-slate-50/80 border border-slate-200/50 p-2 rounded-lg">
                  <div class="text-[9px] text-slate-400 uppercase font-bold">Liver Vol</div>
                  <div class="text-sm font-extrabold text-slate-800 mt-0.5">{{ activePatient.metrics.volume !== '—' ? activePatient.metrics.volume.replace(' cc', '') : '—' }} <span v-if="activePatient.metrics.volume !== '—'" class="text-[9px] text-slate-400 font-bold">cc</span></div>
                </div>
                <div class="bg-slate-50/80 border border-slate-200/50 p-2 rounded-lg">
                  <div class="text-[9px] text-slate-400 uppercase font-bold">Lesion Vol</div>
                  <div class="text-sm font-extrabold mt-0.5" :class="activePatient.hasLesions ? 'text-rose-600' : 'text-slate-850'">{{ activePatient.lesionVolume !== '—' ? activePatient.lesionVolume.replace(' cc', '') : '—' }} <span v-if="activePatient.lesionVolume !== '—' && activePatient.lesionVolume !== '0 cc'" class="text-[9px] text-slate-400 font-bold">cc</span></div>
                </div>
              </div>

              <div class="pt-2">
                <button v-if="activePatient.status === 'Ready' && !isInferenceRunning" @click="handleTriggerSegment" class="w-full flex items-center justify-center gap-1.5 py-2.5 rounded-lg text-xs font-semibold uppercase tracking-wider clinical-btn-primary active-shrink">
                  <Play class="w-3.5 h-3.5 fill-white" /> Run AI Segmenter
                </button>
                <div v-else-if="isInferenceRunning" class="w-full flex items-center justify-center gap-2 py-2.5 rounded-lg text-xs font-mono font-bold text-sky-700 bg-sky-50 border border-sky-100">
                  <Loader2 class="w-3.5 h-3.5 animate-spin" /> Ingesting {{ inferenceProgress }}%
                </div>
                <button v-else @click="handleViewPatientDetails" class="w-full flex items-center justify-center gap-1.5 py-2.5 rounded-lg text-xs font-bold uppercase tracking-wider clinical-btn-primary active-shrink">
                  Open Full Workstation <ArrowRight class="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          </div>
        </div>

      </div>

    </div>

    <!-- ════════════════════════════════════════
         2. HOSPITAL ADMIN WORKSPACE
         ════════════════════════════════════════ -->
    <div v-else-if="auth.userRole === 'admin'" class="space-y-6 animate-fade-in">
      
      <!-- Top KPIs -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="frosted-glass-panel p-4 flex items-center justify-between">
          <div class="space-y-1">
            <div class="text-[9px] font-bold uppercase tracking-wider text-slate-400">Total Users Active</div>
            <div class="text-xl font-extrabold text-slate-900">14 Doctors</div>
            <div class="text-[10px] text-slate-500 font-bold">4 Departments Connected</div>
          </div>
          <div class="w-9 h-9 rounded-lg bg-purple-50 text-purple-700 flex items-center justify-center shadow-sm">
            <Users class="w-4.5 h-4.5" />
          </div>
        </div>

        <div class="frosted-glass-panel p-4 flex items-center justify-between">
          <div class="space-y-1">
            <div class="text-[9px] font-bold uppercase tracking-wider text-slate-400">System Network Load</div>
            <div class="text-xl font-extrabold text-slate-900">421.5 Mbps</div>
            <div class="text-[10px] text-emerald-600 font-bold flex items-center gap-0.5">
              <CheckCircle class="w-3 h-3" /> PACS routing stable
            </div>
          </div>
          <div class="w-9 h-9 rounded-lg bg-purple-50 text-purple-700 flex items-center justify-center shadow-sm">
            <Server class="w-4.5 h-4.5" />
          </div>
        </div>

        <div class="frosted-glass-panel p-4 flex items-center justify-between">
          <div class="space-y-1">
            <div class="text-[9px] font-bold uppercase tracking-wider text-slate-400">AI GPU Utilisation</div>
            <div class="text-xl font-extrabold text-slate-900">48.2% Average</div>
            <div class="text-[10px] text-slate-500 font-bold">Running model inference</div>
          </div>
          <div class="w-9 h-9 rounded-lg bg-purple-50 text-purple-700 flex items-center justify-center shadow-sm">
            <Activity class="w-4.5 h-4.5" />
          </div>
        </div>

        <div class="frosted-glass-panel p-4 flex items-center justify-between">
          <div class="space-y-1">
            <div class="text-[9px] font-bold uppercase tracking-wider text-slate-400">Security Audit status</div>
            <div class="text-xl font-extrabold text-slate-900">100% Secure</div>
            <div class="text-[10px] text-slate-500 font-bold">HIPAA Compliant trace log</div>
          </div>
          <div class="w-9 h-9 rounded-lg bg-purple-50 text-purple-700 flex items-center justify-center shadow-sm">
            <Shield class="w-4.5 h-4.5" />
          </div>
        </div>
      </div>

      <!-- Admin Details Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        <!-- Left: Users & Logs -->
        <div class="lg:col-span-8 space-y-6">
          
          <!-- Users table -->
          <div class="frosted-glass-panel overflow-hidden !p-0">
            <div class="px-5 py-3 border-b border-slate-200/50 bg-white/40">
              <h3 class="font-extrabold text-slate-800 text-xs tracking-tight uppercase">Hospital User Access Management</h3>
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-left border-collapse text-xs">
                <thead>
                  <tr class="bg-slate-50/50 border-b border-slate-200/50 text-slate-500 font-bold">
                    <th class="px-5 py-2.5 font-bold text-[9px] uppercase tracking-wider">User Account</th>
                    <th class="px-5 py-2.5 font-bold text-[9px] uppercase tracking-wider">Role Assigned</th>
                    <th class="px-5 py-2.5 font-bold text-[9px] uppercase tracking-wider">Active Department</th>
                    <th class="px-5 py-2.5 font-bold text-[9px] uppercase tracking-wider">Status</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100/50 text-slate-700 font-semibold">
                  <tr v-for="user in adminUsers" :key="user.id">
                    <td class="px-5 py-3 font-bold text-slate-850">{{ user.name }}</td>
                    <td class="px-5 py-3 font-mono text-[10px] text-slate-500 font-bold">{{ user.role }}</td>
                    <td class="px-5 py-3 text-slate-655">{{ user.dept }}</td>
                    <td class="px-5 py-3">
                      <span :class="user.status === 'Active' ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-100 text-slate-400'" class="px-2 py-0.5 rounded text-[9px] font-bold">
                        {{ user.status }}
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Audit log console -->
          <div class="frosted-glass-panel p-5 space-y-4">
            <h3 class="font-extrabold text-slate-800 text-xs tracking-tight uppercase border-b border-slate-200/50 pb-2.5">Real-time Compliance Audit Trail</h3>
            <div class="space-y-2.5">
              <div v-for="log in adminLogs" :key="log.time" class="flex items-center justify-between text-xs p-2.5 bg-white/40 border border-slate-200/50 rounded-xl">
                <div class="flex items-center gap-3">
                  <span class="font-mono text-[10px] text-slate-400 font-bold">{{ log.time }}</span>
                  <span class="font-extrabold text-slate-800">{{ log.user }}</span>
                  <span class="text-slate-500 font-semibold">&mdash; {{ log.action }}</span>
                </div>
                <span class="text-[9.5px] font-bold text-emerald-600 font-mono">{{ log.status }}</span>
              </div>
            </div>
          </div>

        </div>

        <!-- Right: Server health checks -->
        <div class="lg:col-span-4 space-y-6">
          <div class="frosted-glass-panel p-5 space-y-4">
            <h3 class="font-extrabold text-slate-800 text-xs tracking-tight uppercase border-b border-slate-200/50 pb-2.5">PACS &amp; System Health</h3>
            
            <div class="space-y-3.5">
              <div class="flex justify-between items-center text-xs">
                <span class="font-bold text-slate-655">DICOM PACS Router</span>
                <span class="px-2.5 py-0.5 rounded bg-emerald-50 text-emerald-800 font-bold text-[9px] border border-emerald-100">ONLINE</span>
              </div>
              <div class="flex justify-between items-center text-xs">
                <span class="font-bold text-slate-655">AI Inference Server</span>
                <span class="px-2.5 py-0.5 rounded bg-emerald-50 text-emerald-800 font-bold text-[9px] border border-emerald-100">ONLINE</span>
              </div>
              <div class="flex justify-between items-center text-xs">
                <span class="font-bold text-slate-655">PostgreSQL Database</span>
                <span class="px-2.5 py-0.5 rounded bg-emerald-50 text-emerald-800 font-bold text-[9px] border border-emerald-100">STABLE</span>
              </div>
              <div class="flex justify-between items-center text-xs">
                <span class="font-bold text-slate-655">Storage Allocation</span>
                <span class="font-mono font-bold text-slate-700">1.2 TB / 4.0 TB free</span>
              </div>
            </div>

            <!-- Health visual tracker representation -->
            <div class="pt-4 border-t border-slate-200/50 text-center">
              <div class="text-[10px] text-slate-400 font-bold uppercase tracking-wider mb-2">Host Node System Latency</div>
              <div class="flex gap-1 justify-center items-end h-8">
                <div class="w-2.5 bg-teal-500 rounded-t h-3"></div>
                <div class="w-2.5 bg-teal-500 rounded-t h-4"></div>
                <div class="w-2.5 bg-teal-500 rounded-t h-3.5"></div>
                <div class="w-2.5 bg-teal-500 rounded-t h-5"></div>
                <div class="w-2.5 bg-sky-500 rounded-t h-6 animate-pulse"></div>
              </div>
              <div class="text-[9px] font-mono text-slate-455 text-slate-400 mt-2 font-bold">12ms average node latency</div>
            </div>

          </div>
        </div>

      </div>

    </div>

    <!-- ════════════════════════════════════════
         3. AI RESEARCH ENGINEER WORKSPACE
         ════════════════════════════════════════ -->
    <div v-if="auth.userRole === 'researcher'" class="space-y-6 animate-fade-in">
      
      <!-- Top KPIs -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="frosted-glass-panel p-4 flex items-center justify-between">
          <div class="space-y-1">
            <div class="text-[9px] font-bold uppercase tracking-wider text-slate-400">Deployed Model</div>
            <div class="text-xl font-extrabold text-slate-900">UNet3D v1.4.0</div>
            <div class="text-[10px] text-slate-500 font-bold">Voxel ResNet Backbone</div>
          </div>
          <div class="w-9 h-9 rounded-lg bg-blue-50 text-blue-700 flex items-center justify-center shadow-sm">
            <Activity class="w-4.5 h-4.5" />
          </div>
        </div>

        <div class="frosted-glass-panel p-4 flex items-center justify-between">
          <div class="space-y-1">
            <div class="text-[9px] font-bold uppercase tracking-wider text-slate-400">Overall Dice Average</div>
            <div class="text-xl font-extrabold text-slate-900">95.4% Accuracy</div>
            <div class="text-[10px] text-teal-600 font-bold flex items-center gap-0.5">
              <TrendingUp class="w-3 h-3" /> Exceeds baseline v1.3
            </div>
          </div>
          <div class="w-9 h-9 rounded-lg bg-blue-50 text-blue-700 flex items-center justify-center shadow-sm">
            <TrendingUp class="w-4.5 h-4.5" />
          </div>
        </div>

        <div class="frosted-glass-panel p-4 flex items-center justify-between">
          <div class="space-y-1">
            <div class="text-[9px] font-bold uppercase tracking-wider text-slate-400">Training Epochs</div>
            <div class="text-xl font-extrabold text-slate-900">50 epochs</div>
            <div class="text-[10px] text-slate-500 font-bold">12 hours train time</div>
          </div>
          <div class="w-9 h-9 rounded-lg bg-blue-50 text-blue-700 flex items-center justify-center shadow-sm">
            <Layers class="w-4.5 h-4.5" />
          </div>
        </div>

        <div class="frosted-glass-panel p-4 flex items-center justify-between">
          <div class="space-y-1">
            <div class="text-[9px] font-bold uppercase tracking-wider text-slate-400">Dataset Volume</div>
            <div class="text-xl font-extrabold text-slate-900">350 patients</div>
            <div class="text-[10px] text-slate-500 font-bold">L3-L4 axial segmentation</div>
          </div>
          <div class="w-9 h-9 rounded-lg bg-blue-50 text-blue-700 flex items-center justify-center shadow-sm">
            <Database class="w-4.5 h-4.5" />
          </div>
        </div>
      </div>

      <!-- Research Details Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        <!-- Left: Chart & Model queue -->
        <div class="lg:col-span-8 space-y-6">
          
          <!-- Training Trend visual SVG chart -->
          <div class="frosted-glass-panel p-5 space-y-4">
            <h3 class="font-extrabold text-slate-800 text-xs tracking-tight uppercase border-b border-slate-200/50 pb-2.5">Volumetric Model Validation Convergence (Dice / Loss)</h3>
            
            <div class="relative bg-slate-950 rounded-xl p-4 h-64 border border-slate-900 flex flex-col justify-between select-none">
              <div class="absolute inset-0 bg-[radial-gradient(rgba(255,255,255,0.01)_1px,transparent_1px)] bg-[size:16px_16px] pointer-events-none"></div>
              
              <!-- Simple SVG Line graph representing dice scores trends -->
              <svg viewBox="0 0 100 50" class="w-full h-full">
                <!-- Grid lines -->
                <line x1="0" y1="10" x2="100" y2="10" stroke="#1e293b" stroke-width="0.3" stroke-dasharray="1,1" />
                <line x1="0" y1="20" x2="100" y2="20" stroke="#1e293b" stroke-width="0.3" stroke-dasharray="1,1" />
                <line x1="0" y1="30" x2="100" y2="30" stroke="#1e293b" stroke-width="0.3" stroke-dasharray="1,1" />
                <line x1="0" y1="40" x2="100" y2="40" stroke="#1e293b" stroke-width="0.3" stroke-dasharray="1,1" />
                
                <!-- Dice curve line (Teal) -->
                <path d="M 0,42 Q 25,35 50,22 T 100,10" fill="none" stroke="#14b8a6" stroke-width="1.2" stroke-linecap="round" />
                
                <!-- Loss curve line (Sky) -->
                <path d="M 0,15 Q 25,25 50,38 T 100,45" fill="none" stroke="#0284c7" stroke-width="0.8" stroke-dasharray="1.5,1.5" />
              </svg>

              <!-- Legends -->
              <div class="flex justify-between items-center text-[9px] font-mono text-slate-550 text-slate-400">
                <span class="flex items-center gap-1"><span class="w-2.5 h-0.5 bg-teal-500 inline-block"></span> Validation Dice Score</span>
                <span class="flex items-center gap-1"><span class="w-2.5 h-0.5 bg-sky-500 border-dashed border-t inline-block"></span> Focal Loss Curve</span>
                <span>Epoch 50/50</span>
              </div>
            </div>
          </div>

          <!-- Dataset splits -->
          <div class="frosted-glass-panel overflow-hidden !p-0">
            <div class="px-5 py-3 border-b border-slate-200/50 bg-white/40">
              <h3 class="font-extrabold text-slate-800 text-xs tracking-tight uppercase">Radiological Dataset Directories</h3>
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-left border-collapse text-xs">
                <thead>
                  <tr class="bg-slate-50/50 border-b border-slate-200/50 text-slate-500 font-bold">
                    <th class="px-5 py-2.5 font-bold text-[9px] uppercase tracking-wider">Dataset Cohort</th>
                    <th class="px-5 py-2.5 font-bold text-[9px] uppercase tracking-wider">CT Volumes</th>
                    <th class="px-5 py-2.5 font-bold text-[9px] uppercase tracking-wider">Ground Truth Mask Status</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100/50 text-slate-700 font-semibold">
                  <tr v-for="cohort in datasetDistribution" :key="cohort.split">
                    <td class="px-5 py-3 font-bold text-slate-850">{{ cohort.split }}</td>
                    <td class="px-5 py-3 font-mono font-bold">{{ cohort.cases }} subjects</td>
                    <td class="px-5 py-3 text-teal-650 font-bold text-[10px]">{{ cohort.labels }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

        </div>

        <!-- Right Model topologies -->
        <div class="lg:col-span-4 space-y-6">
          <div class="frosted-glass-panel p-5 space-y-4">
            <h3 class="font-extrabold text-slate-800 text-xs tracking-tight uppercase border-b border-slate-200/50 pb-2.5">Available Inference Models</h3>
            
            <div class="space-y-3">
              <div v-for="m in activeModels" :key="m.name" class="p-3 bg-white/40 border border-slate-200/50 rounded-xl space-y-1">
                <div class="flex justify-between items-center">
                  <span class="font-bold text-slate-800 text-xs">{{ m.name }}</span>
                  <span class="px-1.5 py-0.5 rounded text-[8px] font-bold" :class="m.status === 'Active' ? 'bg-teal-50 text-teal-700' : 'bg-amber-50 text-amber-700'">{{ m.status }}</span>
                </div>
                <div class="flex justify-between text-[10px] text-slate-500 font-semibold">
                  <span>Version: {{ m.version }}</span>
                  <span>Dice: {{ m.dice }} &middot; IoU: {{ m.iou }}</span>
                </div>
              </div>
            </div>

            <!-- Model Parameters settings link -->
            <div class="pt-2">
              <button @click="router.push('/app/research')" class="w-full flex items-center justify-center gap-1.5 py-2 rounded-lg text-xs font-bold uppercase tracking-wider clinical-btn-primary active-shrink">
                Configure Nodes <Settings class="w-3.5 h-3.5" />
              </button>
            </div>

          </div>
        </div>

      </div>

    </div>

    <!-- ════════════════════════════════════════
         4. CLINICIAN / PHYSICIAN WORKSPACE
         ════════════════════════════════════════ -->
    <div v-if="auth.userRole === 'clinician'" class="space-y-6 animate-fade-in">
      
      <!-- Top KPIs -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="frosted-glass-panel p-4 flex items-center justify-between">
          <div class="space-y-1">
            <div class="text-[9px] font-bold uppercase tracking-wider text-slate-400">Assigned Patients</div>
            <div class="text-xl font-extrabold text-slate-900">8 Active Cases</div>
            <div class="text-[10px] text-slate-500 font-bold">Oncology Suite 2B</div>
          </div>
          <div class="w-9 h-9 rounded-lg bg-emerald-50 text-emerald-700 flex items-center justify-center shadow-sm">
            <Heart class="w-4.5 h-4.5" />
          </div>
        </div>

        <div class="frosted-glass-panel p-4 flex items-center justify-between">
          <div class="space-y-1">
            <div class="text-[9px] font-bold uppercase tracking-wider text-slate-400">Reports Signed</div>
            <div class="text-xl font-extrabold text-slate-900">6 Approved</div>
            <div class="text-[10px] text-slate-500 font-bold">Ready for consult validation</div>
          </div>
          <div class="w-9 h-9 rounded-lg bg-emerald-50 text-emerald-700 flex items-center justify-center shadow-sm">
            <FileText class="w-4.5 h-4.5" />
          </div>
        </div>

        <div class="frosted-glass-panel p-4 flex items-center justify-between">
          <div class="space-y-1">
            <div class="text-[9px] font-bold uppercase tracking-wider text-slate-400">Mean Lesion Change</div>
            <div class="text-xl font-extrabold text-rose-600">-31.2% regression</div>
            <div class="text-[10px] text-emerald-600 font-bold flex items-center gap-0.5">
              <TrendingUp class="w-3 h-3" /> Favorable progression
            </div>
          </div>
          <div class="w-9 h-9 rounded-lg bg-emerald-50 text-emerald-700 flex items-center justify-center shadow-sm">
            <Activity class="w-4.5 h-4.5" />
          </div>
        </div>

        <div class="frosted-glass-panel p-4 flex items-center justify-between">
          <div class="space-y-1">
            <div class="text-[9px] font-bold uppercase tracking-wider text-slate-400">Clinical Alerts</div>
            <div class="text-xl font-extrabold text-slate-900">0 critical</div>
            <div class="text-[10px] text-slate-500 font-bold">All margins stable</div>
          </div>
          <div class="w-9 h-9 rounded-lg bg-emerald-50 text-emerald-700 flex items-center justify-center shadow-sm">
            <CheckCircle class="w-4.5 h-4.5" />
          </div>
        </div>
      </div>

      <!-- Clinician splits -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        <!-- Left panel Progression Timeline -->
        <div class="lg:col-span-8 space-y-6">
          <div class="frosted-glass-panel p-5 space-y-5">
            <h3 class="font-extrabold text-slate-800 text-xs tracking-tight uppercase border-b border-slate-200/50 pb-2.5">Patient progression timeline: Marcus Aurelius</h3>
            
            <div class="relative pl-6 border-l border-slate-200/60 space-y-6 text-xs font-semibold">
              <div v-for="t in clinicianTimeline" :key="t.date" class="relative">
                <!-- timeline dot indicator -->
                <div class="absolute -left-[30px] w-2.5 h-2.5 rounded-full bg-emerald-500 border border-white mt-1"></div>
                
                <div class="space-y-1 bg-white/40 border border-slate-200/50 rounded-xl p-3">
                  <div class="flex justify-between items-center text-[10px] font-bold text-slate-400">
                    <span>SCAN DATE: {{ t.date }}</span>
                    <span class="text-rose-600">Tumor Vol: {{ t.lesion }}</span>
                  </div>
                  <div class="text-slate-850 font-bold text-sm">Liver Parenchyma Volume: {{ t.volume }}</div>
                  <div class="text-slate-500 font-medium text-[11px] leading-relaxed">{{ t.notes }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right panel oncology summaries -->
        <div class="lg:col-span-4 space-y-6">
          <div class="frosted-glass-panel p-5 space-y-4">
            <h3 class="font-extrabold text-slate-800 text-xs tracking-tight uppercase border-b border-slate-200/50 pb-2.5">Oncology Insights</h3>
            
            <div class="space-y-3.5">
              <div class="text-[9px] font-bold text-slate-400 uppercase tracking-widest">Active Diagnosis Summary</div>
              <p class="text-xs text-slate-600 leading-relaxed font-semibold">
                {{ clinicianNotes }}
              </p>
              
              <div class="pt-3 border-t border-slate-200/50 space-y-2 text-[10.5px] font-bold text-slate-700">
                <div class="flex items-center gap-1.5 text-emerald-600"><CheckCircle class="w-4 h-4" /> Chemo response: Positive</div>
                <div class="flex items-center gap-1.5 text-slate-655"><Clock class="w-4 h-4" /> Next scan due: June 15, 2026</div>
              </div>
            </div>

            <div class="pt-3 border-t border-slate-200/50">
              <button @click="router.push('/app/reports')" class="w-full flex items-center justify-center gap-1.5 py-2.5 rounded-lg text-xs font-bold uppercase tracking-wider clinical-btn-primary active-shrink">
                Open Reports Library <FileText class="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        </div>

      </div>

    </div>

    <!-- ════════════════════════════════════════
         5. IMAGING TECHNICIAN WORKSPACE
         ════════════════════════════════════════ -->
    <div v-if="auth.userRole === 'technician'" class="space-y-6 animate-fade-in">
      
      <!-- Top KPIs -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="frosted-glass-panel p-4 flex items-center justify-between">
          <div class="space-y-1">
            <div class="text-[9px] font-bold uppercase tracking-wider text-slate-400">Scans Ingested Today</div>
            <div class="text-xl font-extrabold text-slate-900">4 Volumes</div>
            <div class="text-[10px] text-slate-500 font-bold">128 MB total caching footprint</div>
          </div>
          <div class="w-9 h-9 rounded-lg bg-amber-50 text-amber-700 flex items-center justify-center shadow-sm">
            <UploadCloud class="w-4.5 h-4.5" />
          </div>
        </div>

        <div class="frosted-glass-panel p-4 flex items-center justify-between">
          <div class="space-y-1">
            <div class="text-[9px] font-bold uppercase tracking-wider text-slate-400">Pending Assignments</div>
            <div class="text-xl font-extrabold text-slate-900">0 Scans</div>
            <div class="text-[10px] text-emerald-600 font-bold flex items-center gap-0.5">
              <CheckCircle class="w-3 h-3" /> Queue fully assigned
            </div>
          </div>
          <div class="w-9 h-9 rounded-lg bg-amber-50 text-amber-700 flex items-center justify-center shadow-sm">
            <Clock class="w-4.5 h-4.5" />
          </div>
        </div>

        <div class="frosted-glass-panel p-4 flex items-center justify-between">
          <div class="space-y-1">
            <div class="text-[9px] font-bold uppercase tracking-wider text-slate-400">Preprocessing Load</div>
            <div class="text-xl font-extrabold text-slate-900">1 Queue Active</div>
            <div class="text-[10px] text-slate-500 font-bold">Automatic intensity normalization</div>
          </div>
          <div class="w-9 h-9 rounded-lg bg-amber-50 text-amber-700 flex items-center justify-center shadow-sm">
            <Activity class="w-4.5 h-4.5" />
          </div>
        </div>

        <div class="frosted-glass-panel p-4 flex items-center justify-between">
          <div class="space-y-1">
            <div class="text-[9px] font-bold uppercase tracking-wider text-slate-400">Modality Validation</div>
            <div class="text-xl font-extrabold text-slate-900">100% DICOM compliant</div>
            <div class="text-[10px] text-slate-500 font-bold">CT abdomen reconstruction</div>
          </div>
          <div class="w-9 h-9 rounded-lg bg-amber-50 text-amber-700 flex items-center justify-center shadow-sm">
            <Shield class="w-4.5 h-4.5" />
          </div>
        </div>
      </div>

      <!-- Technician details split -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        <!-- Left: Upload area & queue -->
        <div class="lg:col-span-8 space-y-6">
          
          <!-- Technician Direct Assign & Ingest form -->
          <div class="frosted-glass-panel p-5 space-y-4">
            <h3 class="font-extrabold text-slate-800 text-xs tracking-tight uppercase border-b border-slate-200/50 pb-2.5">DICOM Patient Demographics Assigner</h3>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs font-semibold">
              <div>
                <label class="block text-[8px] font-bold text-slate-400 uppercase mb-1">Patient Name/ID</label>
                <input v-model="assignName" type="text" class="w-full bg-white/80 border border-slate-200 rounded-lg px-2.5 py-1.5 text-slate-800 focus:outline-none focus:border-amber-500" />
              </div>
              <div>
                <label class="block text-[8px] font-bold text-slate-400 uppercase mb-1">Imaging Modality</label>
                <select v-model="assignModality" class="w-full bg-white/80 border border-slate-200 rounded-lg px-2.5 py-1.5 text-slate-800 focus:outline-none focus:border-amber-500">
                  <option value="CT">CT (Computed Tomography)</option>
                  <option value="MR">MR (Magnetic Resonance)</option>
                </select>
              </div>
              <div>
                <label class="block text-[8px] font-bold text-slate-400 uppercase mb-1">Patient Age</label>
                <input v-model.number="assignAge" type="number" class="w-full bg-white/80 border border-slate-200 rounded-lg px-2.5 py-1.5 text-slate-800 focus:outline-none focus:border-amber-500" />
              </div>
            </div>

            <button @click="handleAssign" class="flex items-center justify-center gap-1.5 px-4 py-2.5 rounded-lg text-xs font-bold uppercase tracking-wider clinical-btn-primary active-shrink">
              Assign &amp; Dispatch to Workqueue <ArrowRight class="w-3.5 h-3.5" />
            </button>
          </div>

          <!-- Preprocessing tasks -->
          <div class="frosted-glass-panel overflow-hidden !p-0">
            <div class="px-5 py-3 border-b border-slate-200/50 bg-white/40 flex justify-between items-center">
              <h3 class="font-extrabold text-slate-800 text-xs tracking-tight uppercase">Preprocessing Pipelines</h3>
              <span class="text-[9px] font-mono bg-white/70 border border-slate-200/60 px-2 py-0.5 rounded text-slate-500">CUDA Enabled</span>
            </div>
            <div class="p-4 space-y-4">
              <div v-for="item in preprocQueue" :key="item.file" class="flex items-center justify-between border-b border-slate-100 pb-3 last:border-0 last:pb-0">
                <div class="flex-1 mr-6 space-y-1">
                  <div class="flex justify-between text-xs font-bold text-slate-800">
                    <span>{{ item.file }} ({{ item.format }})</span>
                    <span class="text-[10px] text-slate-400">{{ item.preproc }}</span>
                  </div>
                  <!-- Progress slider representation -->
                  <div class="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
                    <div class="bg-amber-500 h-full rounded-full transition-all duration-300" :style="{ width: item.progress + '%' }"></div>
                  </div>
                </div>
                
                <span class="px-2.5 py-0.5 rounded-full text-[9px] font-bold" :class="item.progress === 100 ? 'bg-teal-50 text-teal-700' : 'bg-amber-50 text-amber-700 animate-pulse'">
                  {{ item.progress }}%
                </span>
              </div>
            </div>
          </div>

        </div>

        <!-- Right: Upload area -->
        <div class="lg:col-span-4 space-y-6">
          <div class="frosted-glass-panel p-5 space-y-4">
            <h3 class="font-extrabold text-slate-800 text-xs tracking-tight uppercase border-b border-slate-200/50 pb-2.5">Local Upload Directory</h3>
            
            <div class="border border-dashed border-slate-200 rounded-xl p-6 text-center bg-white/30 space-y-2">
              <UploadCloud class="w-8 h-8 text-amber-600 mx-auto" />
              <div class="text-xs font-bold text-slate-700">Drag files to ingest</div>
              <div class="text-[9px] text-slate-400 font-bold">Accepts *.dcm, *.nii.gz, *.pdf</div>
            </div>

            <div class="pt-2">
              <button @click="router.push('/app/upload')" class="w-full flex items-center justify-center gap-1.5 py-2.5 rounded-lg text-xs font-bold uppercase tracking-wider clinical-btn-primary active-shrink">
                Launch Batch Ingest <UploadCloud class="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        </div>

      </div>

    </div>

  </div>
</template>
