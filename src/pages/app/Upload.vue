<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAppState } from '../../composables/useAppState'
import {
  UploadCloud, FileText, CheckCircle2, Loader2, AlertCircle,
  X, ShieldCheck, ChevronRight, File, Database, Zap, Play, RotateCcw,
  ChevronLeft, BrainCircuit, Activity, Sliders, Layers
} from 'lucide-vue-next'

const router = useRouter()
const {
  uploadQueue,
  simulateUpload,
  patients,
  activePatient,
  selectPatient,
  runSegmentation,
  isInferenceRunning,
  inferenceProgress,
  inferenceStage
} = useAppState()

const isDragging = ref(false)
const patientName = ref('')
const patientDob = ref('')
const patientGender = ref('Male')
const modality = ref('CT Abdomen (Portal Venous)')

// Viewer Controls
const currentSlice = ref(10)
const wwValue = ref(400) // Window Width
const wlValue = ref(40)  // Window Level
const maskOpacity = ref(60) // Percentage opacity of teal mask
const showGroundTruth = ref(false)
const showLesions = ref(true)

const handleDragOver = (e) => { e.preventDefault(); isDragging.value = true }
const handleDragLeave = () => { isDragging.value = false }
const handleDrop = (e) => { e.preventDefault(); isDragging.value = false; processFiles(e.dataTransfer.files) }
const handleFileSelect = (e) => processFiles(e.target.files)

const processFiles = (files) => {
  for (const file of files) {
    const filename = file.name.toLowerCase()
    let type = 'unknown'
    if (filename.endsWith('.dcm')) type = 'dicom'
    else if (filename.endsWith('.nii') || filename.endsWith('.nii.gz')) type = 'nifti'
    else if (filename.endsWith('.pdf')) type = 'pdf'
    
    if (type === 'unknown') {
      const ext = filename.split('.').pop()
      alert(`Format .${ext} not supported.`)
      continue
    }
    simulateUpload(file.name, (file.size / 1048576).toFixed(1) + ' MB', type)
  }
}

// Current slice data based on scroll selection
const sliceData = computed(() => {
  if (!activePatient.value || !activePatient.value.slices) return null
  return activePatient.value.slices[currentSlice.value]
})

// CSS grayscale filter computed based on WW / WL adjustments
const ctFilterStyle = computed(() => {
  const contrast = (400 / wwValue.value).toFixed(2)
  const brightness = ((wlValue.value + 100) / 140).toFixed(2)
  return {
    filter: `contrast(${contrast}) brightness(${brightness})`
  }
})

const handleTriggerSegment = () => {
  if (activePatient.value) {
    runSegmentation(activePatient.value.id)
  }
}

const handleResetWorkstation = () => {
  wwValue.value = 400
  wlValue.value = 40
  maskOpacity.value = 60
  showGroundTruth.value = false
  showLesions.value = true
}

// Inactive/Active logs
const activeConsoleLogs = ref([])
watch(inferenceStage, (newStage) => {
  if (isInferenceRunning.value) {
    if (inferenceProgress.value <= 5) {
      activeConsoleLogs.value = []
    }
    const time = new Date().toLocaleTimeString([], { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' })
    activeConsoleLogs.value.push(`[${time}] ${newStage}`)
  }
})

// Reset slice index on patient change
watch(activePatient, () => {
  currentSlice.value = 10
})

const completedUploads = computed(() => uploadQueue.value.filter(u => u.status === 'completed'))
const activeUploads = computed(() => uploadQueue.value.filter(u => u.status === 'uploading'))

const typeLabel = (type) => ({ dicom: 'DICOM', nifti: 'NIfTI', pdf: 'PDF' }[type] || type)
</script>

<template>
  <div class="space-y-5 animate-fade-in-up">

    <!-- Header -->
    <div class="frosted-glass-panel p-4 flex flex-wrap items-center justify-between gap-4">
      <div>
        <div class="section-title">Imaging Ingest & Real-Time AI Segmentation</div>
        <h2 class="text-sm font-black text-slate-800 mt-0.5">Clinical Workstation Upload Hub</h2>
        <p class="text-[10px] text-slate-500 font-medium mt-0.5">Ingest patient volume scans and evaluate real-time mask segmentation directly</p>
      </div>
      <button @click="router.push('/app/analysis')" class="clinical-btn-secondary flex items-center gap-2 px-3 py-2 rounded-xl text-xs font-bold active-shrink">
        Open Analysis Workspace <ChevronRight class="w-3.5 h-3.5" />
      </button>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-5">

      <!-- LEFT: Upload, Case Selector & Patient Metadata (4 columns) -->
      <div class="lg:col-span-4 space-y-4">

        <!-- Drop Zone -->
        <div class="frosted-glass-panel p-5 space-y-4">
          <div class="section-title flex items-center gap-1.5"><UploadCloud class="w-3.5 h-3.5" /> Upload Files</div>

          <div
            @dragover="handleDragOver" @dragleave="handleDragLeave" @drop="handleDrop"
            :class="[
              'border-2 border-dashed rounded-xl p-8 flex flex-col items-center justify-center gap-3 text-center transition-all cursor-pointer',
              isDragging ? 'border-teal-400 bg-teal-50/40 scale-[1.01]' : 'border-slate-200 bg-white/30 hover:border-teal-300 hover:bg-teal-50/20'
            ]"
          >
            <input id="file-upload" type="file" class="hidden" multiple accept=".dcm,.nii,.nii.gz,.pdf" @change="handleFileSelect" />
            <label for="file-upload" class="cursor-pointer">
              <div class="w-12 h-12 rounded-full bg-teal-50 border border-teal-100 flex items-center justify-center mx-auto mb-2">
                <UploadCloud class="w-5 h-5 text-teal-600" />
              </div>
              <div class="text-xs font-bold text-slate-700">Drag & drop imaging files</div>
              <div class="text-[10px] text-slate-400 font-medium mt-1">or <span class="text-teal-600 font-bold">click to browse</span></div>
              <div class="text-[9px] text-slate-400 font-bold mt-2 bg-slate-50 border border-slate-200/60 px-3 py-1 rounded-full">
                DICOM (.dcm) · NIfTI (.nii/.nii.gz) · PDF
              </div>
            </label>
          </div>

          <!-- Quick test buttons -->
          <div class="flex gap-2">
            <button @click="simulateUpload('CT_Liver_Portal.nii.gz','48.2 MB','nifti')"
              class="clinical-btn-secondary flex-1 py-1.5 rounded-lg text-[9px] font-bold active-shrink">+ NIfTI</button>
            <button @click="simulateUpload('CT_ABDOMEN_CASE.dcm','84.1 MB','dicom')"
              class="clinical-btn-secondary flex-1 py-1.5 rounded-lg text-[9px] font-bold active-shrink">+ DICOM</button>
            <button @click="simulateUpload('Radiology_Report.pdf','2.4 MB','pdf')"
              class="clinical-btn-secondary flex-1 py-1.5 rounded-lg text-[9px] font-bold active-shrink">+ PDF</button>
          </div>

          <!-- Active uploads -->
          <div v-if="activeUploads.length > 0" class="space-y-2">
            <div class="section-title">Uploading</div>
            <div v-for="u in activeUploads" :key="u.id" class="p-2.5 bg-sky-50/60 border border-sky-100 rounded-xl">
              <div class="flex items-center justify-between mb-1.5">
                <span class="text-[10px] font-bold text-slate-700 truncate">{{ u.name }}</span>
                <span class="text-[9px] font-bold text-sky-600 flex-shrink-0 ml-2">{{ u.progress }}%</span>
              </div>
              <div class="progress-track h-1.5">
                <div class="progress-fill" :style="`width:${u.progress}%`"></div>
              </div>
            </div>
          </div>

          <!-- Completed uploads -->
          <div v-if="completedUploads.length > 0" class="space-y-1.5">
            <div class="section-title">Completed Queue</div>
            <div v-for="u in completedUploads.slice(-4)" :key="u.id"
              class="flex items-center gap-2 p-2 bg-white/50 border border-slate-100/70 rounded-lg"
            >
              <CheckCircle2 class="w-3.5 h-3.5 text-teal-500 flex-shrink-0" />
              <span class="text-[9px] font-semibold text-slate-700 truncate">{{ u.name }}</span>
              <span class="ml-auto text-[8px] font-bold text-slate-400 flex-shrink-0">{{ typeLabel(u.type) }}</span>
            </div>
          </div>
        </div>

        <!-- Workspace Active Case Selector -->
        <div class="frosted-glass-panel p-5 space-y-3">
          <div class="section-title flex items-center justify-between">
            <span>Active Workspace Patient</span>
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
          </div>
          <div>
            <label class="block text-[8px] font-bold text-slate-400 uppercase mb-1">Select Patient Case</label>
            <select
              :value="activePatient?.id"
              @change="selectPatient($event.target.value)"
              class="w-full bg-white/80 border border-slate-200 rounded-lg px-2.5 py-1.5 text-xs font-bold text-slate-800 focus:outline-none focus:border-teal-500"
            >
              <option v-for="p in patients" :key="p.id" :value="p.id">
                {{ p.name }} ({{ p.id }})
              </option>
            </select>
          </div>
        </div>

        <!-- Patient Demographics Info -->
        <div v-if="activePatient" class="frosted-glass-panel p-5 space-y-3">
          <div class="section-title flex items-center gap-1.5"><Database class="w-3.5 h-3.5" /> Patient Details</div>
          <div class="text-[10px] space-y-1.5 text-slate-600 font-semibold bg-white/40 border border-slate-200/50 p-2.5 rounded-xl">
            <div class="flex justify-between"><span class="text-slate-400">MRN ID:</span> <span class="font-mono text-slate-800 font-bold">{{ activePatient.id }}</span></div>
            <div class="flex justify-between"><span class="text-slate-400">DOB:</span> <span class="text-slate-800">{{ activePatient.dob }}</span></div>
            <div class="flex justify-between"><span class="text-slate-400">Age / Sex:</span> <span class="text-slate-800">{{ activePatient.age }}y / {{ activePatient.gender }}</span></div>
            <div class="flex justify-between"><span class="text-slate-400">Study Date:</span> <span class="text-slate-800">{{ activePatient.scanDate }}</span></div>
            <div class="flex justify-between"><span class="text-slate-400">Modality:</span> <span class="text-slate-800">{{ activePatient.modality }}</span></div>
          </div>
        </div>
      </div>

      <!-- RIGHT: Live Segmentation Viewer & Real-Time Mask Comparison (8 columns) -->
      <div class="lg:col-span-8 space-y-4">

        <!-- Live CT Viewer / Mask Renderer -->
        <div v-if="activePatient" class="frosted-glass-panel p-4 flex flex-col justify-between min-h-[480px]">
          
          <!-- Viewer Toolbar Header -->
          <div class="flex items-center justify-between pb-2 border-b border-slate-200/50">
            <div class="text-[9px] font-mono text-slate-400 space-y-0.5 font-semibold">
              <div>ACTIVE MRN: {{ activePatient.id }}</div>
              <div>RESOLUTION: 512 x 512 x 20 voxels &middot; Slice {{ currentSlice + 1 }} of 20</div>
            </div>
            
            <div class="flex items-center gap-2">
              <!-- Run AI segmentation trigger -->
              <button 
                v-if="activePatient.status === 'Ready' && !isInferenceRunning && activePatient.hasFile"
                @click="handleTriggerSegment"
                class="flex items-center gap-1 px-3 py-1.5 rounded-lg text-[9.5px] font-bold uppercase tracking-wider clinical-btn-primary active-shrink"
              >
                <Play class="w-3 h-3 fill-white" /> Run AI Segmentation
              </button>
              <button 
                @click="handleResetWorkstation"
                class="flex items-center gap-1 text-[9px] font-bold rounded px-2.5 py-1.5 clinical-btn-secondary active-shrink"
              >
                <RotateCcw class="w-3 h-3" /> Reset View
              </button>
            </div>
          </div>

          <!-- CT Scanner circular layout & SVG Canvas -->
          <div class="flex-1 flex items-center justify-center bg-black/95 rounded-xl border border-slate-800/80 my-4 relative overflow-hidden select-none min-h-[300px]">
            <div class="absolute inset-0 bg-[radial-gradient(rgba(255,255,255,0.015)_1px,transparent_1px)] bg-[size:16px_16px] pointer-events-none"></div>
            
            <div class="absolute w-[95%] h-[95%] rounded-full border border-dashed border-slate-800/40 pointer-events-none flex items-center justify-center">
              <div class="w-[90%] h-[90%] rounded-full border border-slate-800/20"></div>
            </div>

            <!-- PACS HUD Overlay -->
            <div class="absolute top-3.5 left-4 text-[9px] font-mono text-slate-400 space-y-0.5 leading-normal pointer-events-none">
              <div class="font-bold text-slate-300">{{ activePatient.name }}</div>
              <div>MRN: {{ activePatient.id }}</div>
              <div>Age/Sex: {{ activePatient.age }}y / {{ activePatient.gender }}</div>
            </div>

            <div class="absolute top-3.5 right-4 text-[9px] font-mono text-slate-400 text-right space-y-0.5 leading-normal pointer-events-none">
              <div class="font-bold text-teal-500">LiversegAI v1.4.0</div>
              <div>kVp: 120 &middot; mAs: 250</div>
              <div>Thk: 1.0 mm</div>
            </div>

            <div class="absolute bottom-3.5 left-4 text-[9px] font-mono text-slate-400 space-y-0.5 leading-normal pointer-events-none">
              <div>WW: {{ wwValue }} &middot; WL: {{ wlValue }}</div>
              <div>Zoom: 100% (Fit)</div>
              <div>Slice: {{ currentSlice + 1 }} / 20</div>
            </div>

            <div class="absolute bottom-3.5 right-4 text-[9px] font-mono text-slate-400 text-right space-y-0.5 leading-normal pointer-events-none">
              <div>Status: <span :class="activePatient.status === 'Completed' ? 'text-teal-400' : 'text-amber-500'">{{ activePatient.status }}</span></div>
              <div>PACS Router: Connected</div>
            </div>

            <!-- Anatomical markers -->
            <div class="absolute top-3 text-[10px] font-bold font-mono text-slate-500 pointer-events-none">A</div>
            <div class="absolute bottom-3 text-[10px] font-bold font-mono text-slate-500 pointer-events-none">P</div>
            <div class="absolute left-3 text-[10px] font-bold font-mono text-slate-500 pointer-events-none">R</div>
            <div class="absolute right-3 text-[10px] font-bold font-mono text-slate-500 pointer-events-none">L</div>

            <svg viewBox="0 0 100 100" class="w-64 h-64 md:w-80 md:h-80 transition-all duration-300" :style="ctFilterStyle">
              
              <line x1="50" y1="0" x2="50" y2="100" stroke="rgba(255, 255, 255, 0.05)" stroke-width="0.3" stroke-dasharray="2,2" />
              <line x1="0" y1="50" x2="100" y2="50" stroke="rgba(255, 255, 255, 0.05)" stroke-width="0.3" stroke-dasharray="2,2" />
              
              <!-- Left Calibration Ruler -->
              <line x1="4" y1="15" x2="4" y2="85" stroke="rgba(255,255,255,0.25)" stroke-width="0.4" />
              <line x1="4" y1="15" x2="6.5" y2="15" stroke="rgba(255,255,255,0.3)" stroke-width="0.4" />
              <line x1="4" y1="25" x2="6.5" y2="25" stroke="rgba(255,255,255,0.3)" stroke-width="0.4" />
              <line x1="4" y1="35" x2="6.5" y2="35" stroke="rgba(255,255,255,0.3)" stroke-width="0.4" />
              <line x1="4" y1="45" x2="6.5" y2="45" stroke="rgba(255,255,255,0.3)" stroke-width="0.4" />
              <line x1="4" y1="55" x2="6.5" y2="55" stroke="rgba(255,255,255,0.3)" stroke-width="0.4" />
              <line x1="4" y1="65" x2="6.5" y2="65" stroke="rgba(255,255,255,0.3)" stroke-width="0.4" />
              <line x1="4" y1="75" x2="6.5" y2="75" stroke="rgba(255,255,255,0.3)" stroke-width="0.4" />
              <line x1="4" y1="85" x2="6.5" y2="85" stroke="rgba(255,255,255,0.3)" stroke-width="0.4" />
              
              <!-- Bottom Calibration Ruler -->
              <line x1="15" y1="96" x2="85" y2="96" stroke="rgba(255,255,255,0.25)" stroke-width="0.4" />
              <line x1="15" y1="96" x2="15" y2="93.5" stroke="rgba(255,255,255,0.3)" stroke-width="0.4" />
              <line x1="25" y1="96" x2="25" y2="93.5" stroke="rgba(255,255,255,0.3)" stroke-width="0.4" />
              <line x1="35" y1="96" x2="35" y2="93.5" stroke="rgba(255,255,255,0.3)" stroke-width="0.4" />
              <line x1="45" y1="96" x2="45" y2="93.5" stroke="rgba(255,255,255,0.3)" stroke-width="0.4" />
              <line x1="55" y1="96" x2="55" y2="93.5" stroke="rgba(255,255,255,0.3)" stroke-width="0.4" />
              <line x1="65" y1="96" x2="65" y2="93.5" stroke="rgba(255,255,255,0.3)" stroke-width="0.4" />
              <line x1="75" y1="96" x2="75" y2="93.5" stroke="rgba(255,255,255,0.3)" stroke-width="0.4" />
              <line x1="85" y1="96" x2="85" y2="93.5" stroke="rgba(255,255,255,0.3)" stroke-width="0.4" />

              <!-- Body Fat Wall -->
              <path 
                v-if="sliceData"
                :d="`M 50,${22 - sliceData.liverY/8} 
                     C ${68 + sliceData.liverX/6},${20 - sliceData.liverY/8} ${84 + sliceData.liverX/8},28 ${84 + sliceData.liverX/8},48 
                     C ${84 + sliceData.liverX/8},64 70,${74 + sliceData.liverY/8} 58,${76 + sliceData.liverY/8} 
                     C 53,${77 + sliceData.liverY/8} 50,${72 + sliceData.liverY/10} 50,${72 + sliceData.liverY/10} 
                     C 50,${72 + sliceData.liverY/10} 47,${77 + sliceData.liverY/8} 42,${76 + sliceData.liverY/8} 
                     C 30,${74 + sliceData.liverY/8} ${16 - sliceData.liverX/8},64 ${16 - sliceData.liverX/8},48 
                     C ${16 - sliceData.liverX/8},28 ${32 - sliceData.liverX/6},${20 - sliceData.liverY/8} 50,${22 - sliceData.liverY/8} Z`"
                fill="#1b1b1f" 
                stroke="#2e2e33" 
                stroke-width="1.8" 
              />

              <!-- Abdominal Cavity -->
              <path 
                v-if="sliceData"
                :d="`M 50,24 
                     C 66,22 81,29 81,48 
                     C 81,62 68,71 57,73 
                     C 53,74 50,70 50,70 
                     C 50,70 47,74 43,73 
                     C 32,71 19,62 19,48 
                     C 19,29 34,22 50,24 Z`"
                fill="#08080a" 
                stroke="#27272a" 
                stroke-width="0.8" 
              />

              <!-- Crescent gantry -->
              <path d="M 12,74 C 25,92 75,92 88,74" fill="none" stroke="#2a2a2f" stroke-width="1.2" />

              <!-- Rib bones -->
              <g stroke="#ffffff" stroke-width="1.0" stroke-linecap="round" fill="none">
                <path d="M 26,24 Q 21,29 19,36" opacity="0.95" />
                <path d="M 18,43 Q 17,49 18,55" opacity="0.95" />
                <path d="M 20,62 Q 23,68 28,72" opacity="0.95" />
                <path d="M 74,24 Q 79,29 81,36" opacity="0.95" />
                <path d="M 82,43 Q 83,49 82,55" opacity="0.95" />
                <path d="M 80,62 Q 77,68 72,72" opacity="0.95" />
              </g>

              <!-- Spine -->
              <g :transform="`translate(0, ${sliceData ? sliceData.liverY/10 : 0})`">
                <path d="M 44,73.5 Q 50,69.5 56,73.5 Q 60,76.5 50,79.5 Q 40,76.5 44,73.5 Z" fill="#27272a" stroke="#ffffff" stroke-width="0.8" />
                <path d="M 50,78.5 L 50,82.5" stroke="#ffffff" stroke-width="1.2" stroke-linecap="round" />
                <circle cx="50" cy="75" r="1.8" fill="#000000" stroke="#a1a1aa" stroke-width="0.4" />
              </g>

              <!-- IVC & Aorta -->
              <circle cx="43" cy="64" r="2.0" fill="#3f3f46" stroke="#ffffff" stroke-width="0.5" />
              <circle cx="56" cy="63" r="2.4" fill="#52525b" stroke="#ffffff" stroke-width="0.6" />

              <!-- Kidneys -->
              <g v-if="currentSlice >= 7 && currentSlice <= 17">
                <path d="M 27,62 C 23,56 27,47 31,51 C 35,55 31,64 27,64 Z" fill="#1b1b1f" stroke="#4b5563" stroke-width="0.6" />
                <path d="M 73,62 C 77,56 73,47 69,51 C 65,55 69,64 73,64 Z" fill="#1b1b1f" stroke="#4b5563" stroke-width="0.6" />
              </g>

              <!-- Stomach -->
              <path 
                v-if="currentSlice >= 2 && currentSlice <= 13"
                d="M 52,27 C 62,25 73,29 73,38 C 73,46 64,48 54,44 Z"
                fill="#101012" 
                stroke="#3f3f46" 
                stroke-width="0.6" 
              />

              <!-- Spleen -->
              <path 
                v-if="currentSlice >= 4 && currentSlice <= 15"
                d="M 68,46 C 76,43 79,52 76,60 C 73,66 65,64 64,54 Z"
                fill="#1d1d22" 
                stroke="#52525b" 
                stroke-width="0.65" 
              />

              <!-- LIVER -->
              <path 
                v-if="sliceData"
                :d="`M ${46 + sliceData.liverX},${30 + sliceData.liverY/2} 
                     C ${32 + sliceData.liverX},${26 + sliceData.liverY} 19,36 19,48 
                     C 19,58 24,${66 - sliceData.liverY/2} ${32 + sliceData.liverX},${68 - sliceData.liverY/2} 
                     C ${42 + sliceData.liverX},${66 - sliceData.liverY} ${46 + sliceData.liverX},${56 - sliceData.liverY} ${46 + sliceData.liverX},${46 - sliceData.liverY} 
                     C ${46 + sliceData.liverX},${36 - sliceData.liverY} 50,32 ${46 + sliceData.liverX},${30 + sliceData.liverY/2} Z`" 
                fill="#25252a" 
                stroke="#52525b" 
                stroke-width="0.7" 
              />

              <!-- AI TEAL SEGMENTATION MASK -->
              <path 
                v-if="sliceData && activePatient.status === 'Completed'"
                :d="`M ${46 + sliceData.liverX},${30 + sliceData.liverY/2} 
                     C ${32 + sliceData.liverX},${26 + sliceData.liverY} 19,36 19,48 
                     C 19,58 24,${66 - sliceData.liverY/2} ${32 + sliceData.liverX},${68 - sliceData.liverY/2} 
                     C ${42 + sliceData.liverX},${66 - sliceData.liverY} ${46 + sliceData.liverX},${56 - sliceData.liverY} ${46 + sliceData.liverX},${46 - sliceData.liverY} 
                     C ${46 + sliceData.liverX},${36 - sliceData.liverY} 50,32 ${46 + sliceData.liverX},${30 + sliceData.liverY/2} Z`" 
                :fill="`rgba(20, 184, 166, ${maskOpacity / 100})`" 
                stroke="#14b8a6" 
                :stroke-width="maskOpacity > 0 ? 1.0 : 0" 
              />

              <!-- GROUND TRUTH CONTOUR (Real Time Comparison) -->
              <path 
                v-if="sliceData && showGroundTruth && activePatient.status === 'Completed'"
                :d="`M ${46.5 + sliceData.liverX},${30.5 + sliceData.liverY/2} 
                     C ${32.5 + sliceData.liverX},${26.5 + sliceData.liverY} 18.5,35.5 18.5,48 
                     C 18.5,58.5 23.5,${66.5 - sliceData.liverY/2} ${32.5 + sliceData.liverX},${68.5 - sliceData.liverY/2} 
                     C ${42.5 + sliceData.liverX},${66.5 - sliceData.liverY} ${46.5 + sliceData.liverX},${56.5 - sliceData.liverY} ${46.5 + sliceData.liverX},${46.5 - sliceData.liverY} 
                     C ${46.5 + sliceData.liverX},${36.5 - sliceData.liverY} 50.5,31.5 ${46.5 + sliceData.liverX},${30.5 + sliceData.liverY/2} Z`" 
                fill="none" 
                stroke="#10b981" 
                stroke-width="0.8" 
                stroke-dasharray="1.5,1.5" 
              />

              <!-- TUMOR LESION -->
              <circle 
                v-if="sliceData && sliceData.lesionSize > 0 && showLesions && activePatient.status === 'Completed'"
                :cx="28 + sliceData.lesionX / 5" 
                :cy="48 + sliceData.lesionY / 5" 
                :r="sliceData.lesionSize * 15" 
                fill="rgba(239, 68, 68, 0.45)" 
                stroke="#ef4444" 
                stroke-width="0.55" 
              />

            </svg>

            <!-- Unsegmented state overlay -->
            <div 
              v-if="activePatient.status === 'Ready' && !isInferenceRunning"
              class="absolute inset-0 bg-black/75 backdrop-blur-[2px] flex flex-col items-center justify-center gap-3 p-6 text-center"
            >
              <template v-if="!activePatient.hasFile">
                <UploadCloud class="w-8 h-8 text-sky-400 animate-pulse" />
                <h4 class="text-xs font-bold text-white uppercase tracking-wider">No Scan Volume Uploaded</h4>
                <p class="text-[10px] text-slate-400 max-w-xs leading-normal">
                  This patient demographics record was registered via DICOM PACS router, but the actual scan volume (.nii.gz or .dcm) has not yet been ingested.
                </p>
                <p class="text-[9px] text-slate-500 italic mt-1 font-bold">
                  Drag and drop a scan file or click browse to upload and enable AI analysis.
                </p>
              </template>
              <template v-else>
                <AlertCircle class="w-8 h-8 text-amber-500" />
                <h4 class="text-xs font-bold text-white uppercase tracking-wider">Unsegmented Scan Volume</h4>
                <p class="text-[10px] text-slate-400 max-w-xs leading-normal">
                  Execute AI segmentation to generate real-time masks and Dice score analysis on this case.
                </p>
                <button 
                  @click="handleTriggerSegment"
                  class="px-4 py-2 bg-teal-600 text-white rounded-xl text-xs font-bold hover:bg-teal-500 active-shrink flex items-center gap-1.5 mt-2"
                >
                  <Play class="w-3.5 h-3.5 fill-white" /> Run AI Segmentation
                </button>
              </template>
            </div>

            <!-- Pipeline Progress Overlay -->
            <div v-if="isInferenceRunning" class="absolute inset-0 bg-black/90 flex flex-col justify-between p-4 rounded-xl">
              <div class="flex items-center gap-3 border-b border-slate-800 pb-2">
                <Loader2 class="w-5 h-5 animate-spin text-teal-500" />
                <div class="flex-1">
                  <div class="flex justify-between text-xs text-white font-mono">
                    <span>{{ inferenceStage }}</span>
                    <span class="text-teal-400 font-bold">{{ inferenceProgress }}%</span>
                  </div>
                  <div class="w-full bg-slate-800 h-1 rounded-full overflow-hidden mt-1.5">
                    <div class="bg-teal-500 h-full transition-all duration-200" :style="{ width: inferenceProgress + '%' }"></div>
                  </div>
                </div>
              </div>
              
              <div class="flex-1 bg-black/60 p-3 rounded border border-slate-800 font-mono text-[9px] text-teal-400 space-y-1 overflow-y-auto leading-normal my-2">
                <div v-for="(log, idx) in activeConsoleLogs" :key="idx" class="truncate select-none">
                  {{ log }}
                </div>
              </div>
            </div>

          </div>

          <!-- Slider controllers -->
          <div class="space-y-2 border-t border-slate-200/50 pt-3">
            <div class="flex justify-between items-center text-xs">
              <span class="font-bold text-slate-700">Axial Slice Browser</span>
              <span class="font-mono text-slate-500 font-bold bg-slate-50 border px-2 py-0.5 rounded">Slice {{ currentSlice + 1 }} / 20</span>
            </div>
            
            <div class="flex items-center gap-4">
              <button 
                @click="currentSlice > 0 && currentSlice--" 
                :disabled="currentSlice === 0"
                class="p-1.5 rounded border border-slate-200 hover:border-teal-500 disabled:opacity-30"
              >
                <ChevronLeft class="w-4 h-4 text-slate-600" />
              </button>
              
              <input 
                v-model.number="currentSlice"
                type="range" 
                min="0" 
                max="19" 
                step="1"
                class="w-full accent-teal-600 cursor-pointer bg-slate-100 h-1.5 rounded-full"
              />
              
              <button 
                @click="currentSlice < 19 && currentSlice++" 
                :disabled="currentSlice === 19"
                class="p-1.5 rounded border border-slate-200 hover:border-teal-500 disabled:opacity-30"
              >
                <ChevronRight class="w-4 h-4 text-slate-600" />
              </button>
            </div>
          </div>

        </div>

        <div v-else class="frosted-glass-panel p-8 text-center flex flex-col items-center justify-center min-h-[480px] opacity-70">
          <AlertCircle class="w-12 h-12 text-slate-400 mb-4" />
          <h3 class="text-sm font-black text-slate-700 uppercase tracking-wider">No Patient Loaded</h3>
          <p class="text-[10px] text-slate-500 font-semibold mt-1">Please select an active patient or upload a scan file to view real-time segments.</p>
        </div>

        <!-- Real-Time Metrics & Comparison Toggles (8 columns split) -->
        <div v-if="activePatient && activePatient.status === 'Completed'" class="grid grid-cols-1 md:grid-cols-12 gap-4">
          
          <!-- Image manipulation sliders (8 cols) -->
          <div class="frosted-glass-panel p-4 md:col-span-8 space-y-4">
            <div class="grid grid-cols-3 gap-3">
              <div class="space-y-1">
                <div class="flex justify-between items-center text-[9px] text-slate-500 font-bold">
                  <span>Window Width</span>
                  <span class="font-mono">{{ wwValue }} HU</span>
                </div>
                <input v-model.number="wwValue" type="range" min="100" max="800" step="10" class="w-full accent-teal-600 cursor-pointer bg-slate-100 h-1 rounded-full" />
              </div>

              <div class="space-y-1">
                <div class="flex justify-between items-center text-[9px] text-slate-500 font-bold">
                  <span>Window Level</span>
                  <span class="font-mono">{{ wlValue }} HU</span>
                </div>
                <input v-model.number="wlValue" type="range" min="-100" max="200" step="5" class="w-full accent-teal-600 cursor-pointer bg-slate-100 h-1 rounded-full" />
              </div>

              <div class="space-y-1">
                <div class="flex justify-between items-center text-[9px] text-slate-500 font-bold">
                  <span>Teal Mask Opacity</span>
                  <span class="font-mono">{{ maskOpacity }}%</span>
                </div>
                <input v-model.number="maskOpacity" type="range" min="0" max="100" step="5" class="w-full accent-teal-600 cursor-pointer bg-slate-100 h-1 rounded-full" />
              </div>
            </div>
            
            <div class="flex gap-4 pt-1.5 border-t border-slate-100">
              <label class="flex items-center gap-1.5 text-[9px] font-bold text-slate-600 cursor-pointer select-none">
                <input v-model="showGroundTruth" type="checkbox" class="rounded text-teal-600 focus:ring-teal-500 border-slate-300" />
                <span>Show Ground Truth (Real-Time Comparison)</span>
              </label>
              <label class="flex items-center gap-1.5 text-[9px] font-bold text-slate-600 cursor-pointer select-none">
                <input v-model="showLesions" type="checkbox" class="rounded text-teal-600 focus:ring-teal-500 border-slate-300" />
                <span>Show Tumoral Lesions</span>
              </label>
            </div>
          </div>

          <!-- Quick Segmentation Stats (4 cols) -->
          <div class="frosted-glass-panel p-4 md:col-span-4 flex flex-col justify-between">
            <div class="section-title flex items-center gap-1.5"><BrainCircuit class="w-3.5 h-3.5 text-teal-600" /> Segment Stats</div>
            <div class="space-y-2 mt-2">
              <div class="flex justify-between text-[10px] font-bold">
                <span class="text-slate-400">Dice Accuracy:</span>
                <span class="text-teal-600 font-black">{{ activePatient.metrics?.dice || '—' }}</span>
              </div>
              <div class="flex justify-between text-[10px] font-bold">
                <span class="text-slate-400">Liver Volume:</span>
                <span class="text-slate-800">{{ activePatient.metrics?.volume || '—' }}</span>
              </div>
              <div class="flex justify-between text-[10px] font-bold">
                <span class="text-slate-400">Inference Time:</span>
                <span class="text-slate-800">{{ activePatient.metrics?.processingTime || '—' }}</span>
              </div>
            </div>
          </div>

        </div>

      </div>

      <!-- FULL WIDTH BOTTOM: Recently Uploaded Cases Queue -->
      <div class="lg:col-span-12">
        <div class="frosted-glass-panel overflow-hidden">
          <div class="px-5 py-3.5 border-b border-slate-200/50 bg-white/30">
            <div class="section-title">Queue</div>
            <h3 class="text-xs font-black text-slate-800 mt-0.5">Recently Uploaded Patient Scan Database</h3>
          </div>
          <table class="w-full clinical-table">
            <thead>
              <tr>
                <th>Patient</th>
                <th>Modality</th>
                <th>Uploaded</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="p in patients.slice(-4).reverse()" :key="p.id" class="hover:bg-slate-50/50 cursor-pointer" @click="selectPatient(p.id)">
                <td>
                  <div class="text-[10px] font-bold text-slate-800">{{ p.name }}</div>
                  <div class="text-[8px] font-mono text-slate-400">{{ p.id }}</div>
                </td>
                <td class="text-[10px] text-slate-600">{{ p.modality.replace('CT Abdomen ', '') }}</td>
                <td class="text-[9px] font-mono text-slate-500">{{ p.scanDate?.substring(0,10) }}</td>
                <td>
                  <span :class="['inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[8px] font-bold', p.status === 'Completed' ? 'badge-completed' : p.status === 'Analyzing' ? 'badge-analyzing' : 'badge-pending']">
                    {{ p.status }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  </div>
</template>
