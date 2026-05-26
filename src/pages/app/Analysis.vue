<script setup>
import { ref, computed, watch } from 'vue'
import { useAppState } from '../../composables/useAppState'
import { 
  Play, 
  CheckCircle, 
  RotateCcw, 
  Sliders, 
  Layers, 
  Share2, 
  Activity, 
  Loader2, 
  AlertCircle,
  ChevronLeft,
  ChevronRight,
  UploadCloud,
  FileText,
  ShieldCheck,
  HeartPulse,
  BrainCircuit
} from 'lucide-vue-next'

const { 
  activePatient, 
  patients, 
  selectPatient, 
  runSegmentation, 
  isInferenceRunning, 
  inferenceProgress, 
  inferenceStage,
  uploadQueue,
  simulateUpload
} = useAppState()

// Viewer Controls
const currentSlice = ref(10)
const wwValue = ref(400) // Window Width
const wlValue = ref(40)  // Window Level
const maskOpacity = ref(60) // Percentage opacity of teal mask
const showGroundTruth = ref(false)
const showLesions = ref(true)

// Checklist Verification
const chkContours = ref(false)
const chkOutliers = ref(false)
const chkLesions = ref(false)
const isSigned = ref(false)
const isExporting = ref(false)
const exportSuccess = ref(false)

// Selectable Patient Case Queue dropdown
const queuePatients = computed(() => patients.value)

// Reset controls when active patient changes
watch(activePatient, () => {
  currentSlice.value = 10
  chkContours.value = false
  chkOutliers.value = false
  chkLesions.value = false
  isSigned.value = false
  exportSuccess.value = false
})

// CSS grayscale filter computed based on WW / WL adjustments
const ctFilterStyle = computed(() => {
  const contrast = (400 / wwValue.value).toFixed(2)
  const brightness = ((wlValue.value + 100) / 140).toFixed(2)
  return {
    filter: `contrast(${contrast}) brightness(${brightness})`
  }
})

// Current slice data based on scroll selection
const sliceData = computed(() => {
  if (!activePatient.value || !activePatient.value.slices) return null
  return activePatient.value.slices[currentSlice.value]
})

const handleTriggerSegment = () => {
  runSegmentation(activePatient.value.id)
}

const handleSignReport = () => {
  if (!chkContours.value || !chkOutliers.value) {
    alert("Please check all verification checklist steps before signature.")
    return
  }
  isSigned.value = true
}

const handleExportPacs = () => {
  isExporting.value = true
  setTimeout(() => {
    isExporting.value = false
    exportSuccess.value = true
  }, 1500)
}

const handleResetWorkstation = () => {
  wwValue.value = 400
  wlValue.value = 40
  maskOpacity.value = 60
  showGroundTruth.value = false
  showLesions.value = true
}

// Ingest drag/drop logic
const isDragging = ref(false)

const handleDragOver = (e) => {
  e.preventDefault()
  isDragging.value = true
}

const handleDragLeave = () => {
  isDragging.value = false
}

const handleDrop = (e) => {
  e.preventDefault()
  isDragging.value = false
  processFiles(e.dataTransfer.files)
}

const handleFileSelect = (e) => {
  processFiles(e.target.files)
}

const processFiles = (files) => {
  for (let i = 0; i < files.length; i++) {
    const file = files[i]
    const ext = file.name.split('.').pop().toLowerCase()
    
    let type = 'unknown'
    if (ext === 'dcm') type = 'dicom'
    else if (ext === 'nii' || file.name.endsWith('.nii.gz')) type = 'nifti'
    else if (ext === 'pdf') type = 'pdf'
    
    if (type === 'unknown') {
      alert(`Format .${ext} is not supported. Please upload NIfTI (.nii/.nii.gz), DICOM (.dcm), or PDF.`)
      continue
    }

    const sizeStr = (file.size / (1024 * 1024)).toFixed(1) + ' MB'
    simulateUpload(file.name, sizeStr, type)
  }
}

// Watcher to simulate real-time ML diagnostic console logs
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
</script>

<template>
  <div v-if="activePatient" class="grid grid-cols-1 lg:grid-cols-12 gap-6 min-h-[calc(100vh-8.5rem)]">
    
    <!-- LEFT PANEL: INGEST, PATIENTS & DICOM METADATA (3 columns) -->
    <div class="lg:col-span-3 space-y-6">
      
      <!-- Ingest Scans Box -->
      <div class="frosted-glass-panel p-4 space-y-4">
        <h4 class="text-[10px] font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1.5 font-extrabold border-b border-slate-200/50 pb-2">
          <UploadCloud class="w-4 h-4 text-teal-650" /> Ingest Imaging Volume
        </h4>

        <!-- Tiny drag & drop zone -->
        <div 
          @dragover="handleDragOver"
          @dragleave="handleDragLeave"
          @drop="handleDrop"
          :class="[
            'border border-dashed rounded-lg p-4 flex flex-col items-center justify-center gap-2 transition-all cursor-pointer text-center',
            isDragging ? 'border-teal-500 bg-teal-50/20' : 'border-slate-200/80 bg-white/30 hover:bg-white/50'
          ]"
        >
          <input 
            type="file" 
            id="workspace-upload" 
            class="hidden" 
            multiple 
            accept=".dcm,.nii,.nii.gz,.pdf" 
            @change="handleFileSelect"
          />
          <label for="workspace-upload" class="cursor-pointer space-y-1 block w-full">
            <div class="text-[10px] font-bold text-slate-700">
              Drag file here or <span class="text-teal-600 underline">Browse</span>
            </div>
            <div class="text-[8px] text-slate-400 font-bold">DICOM, NIfTI, PDF</div>
          </label>
        </div>

        <!-- Testing shortcuts -->
        <div class="flex gap-1.5 flex-wrap">
          <button 
            @click="simulateUpload('CT_Abdomen_LIVER_PORTAL.nii.gz', '48.2 MB', 'nifti')"
            class="px-2 py-1 text-[8.5px] font-bold rounded bg-slate-100/80 border border-slate-200 hover:bg-white/90 active-shrink text-slate-600"
          >
            + Add NIfTI
          </button>
          <button 
            @click="simulateUpload('DICOM_ROUTE_CASE_29.dcm', '84.1 MB', 'dicom')"
            class="px-2 py-1 text-[8.5px] font-bold rounded bg-slate-100/80 border border-slate-200 hover:bg-white/90 active-shrink text-slate-600"
          >
            + Add DICOM
          </button>
        </div>

        <!-- Upload Statuses (compact) -->
        <div v-if="uploadQueue.length > 0" class="space-y-1.5 max-h-[110px] overflow-y-auto pr-1">
          <div 
            v-for="item in uploadQueue.slice(-3)" 
            :key="item.id" 
            class="text-[9px] bg-white/60 border border-slate-200/50 p-1.5 rounded flex items-center justify-between"
          >
            <span class="truncate font-semibold text-slate-700 w-2/3">{{ item.name }}</span>
            <span v-if="item.status === 'uploading'" class="text-sky-600 animate-pulse font-bold">
              {{ item.progress }}%
            </span>
            <span v-else class="text-teal-600 font-bold flex items-center gap-0.5">
              <CheckCircle class="w-2.5 h-2.5" /> Ingested
            </span>
          </div>
        </div>
      </div>

      <!-- Active Patient Selector -->
      <div class="frosted-glass-panel p-4 space-y-3">
        <h4 class="text-[10px] font-bold uppercase tracking-wider text-slate-500 font-extrabold border-b border-slate-200/50 pb-2 flex items-center justify-between">
          <span>Active Patient Case</span>
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
        </h4>

        <div class="space-y-3">
          <div>
            <label class="block text-[8px] font-bold text-slate-400 uppercase mb-1">Select Active Workspace</label>
            <select 
              :value="activePatient.id" 
              @change="selectPatient($event.target.value)"
              class="w-full bg-white/80 border border-slate-200 rounded-lg px-2.5 py-1.5 text-xs font-bold text-slate-850 focus:outline-none focus:border-teal-500"
            >
              <option v-for="p in queuePatients" :key="p.id" :value="p.id">
                {{ p.name }} ({{ p.id }})
              </option>
            </select>
          </div>

          <!-- Patient Profile details -->
          <div class="text-[10px] space-y-1.5 text-slate-600 font-semibold bg-white/40 border border-slate-200/50 p-2.5 rounded-xl">
            <div class="flex justify-between"><span class="text-slate-400">MRN ID:</span> <span class="font-mono text-slate-800 font-bold">{{ activePatient.id }}</span></div>
            <div class="flex justify-between"><span class="text-slate-400">DOB:</span> <span class="text-slate-800">{{ activePatient.dob }}</span></div>
            <div class="flex justify-between"><span class="text-slate-400">Age / Sex:</span> <span class="text-slate-800">{{ activePatient.age }}y / {{ activePatient.gender }}</span></div>
            <div class="flex justify-between"><span class="text-slate-400">Study Date:</span> <span class="text-slate-800">{{ activePatient.scanDate }}</span></div>
            <div class="flex justify-between"><span class="text-slate-400">Modality:</span> <span class="text-slate-800">{{ activePatient.modality }}</span></div>
          </div>
        </div>
      </div>

      <!-- DICOM Tag Header Validation Checklist -->
      <div class="frosted-glass-panel p-4 space-y-3">
        <h4 class="text-[10px] font-bold uppercase tracking-wider text-slate-500 font-extrabold border-b border-slate-200/50 pb-2">
          DICOM Tag Ingest Validation
        </h4>
        
        <div class="space-y-2 text-[10px] text-slate-600 font-semibold">
          <div class="flex items-center justify-between py-0.5">
            <span class="flex items-center gap-1.5">
              <ShieldCheck class="w-3.5 h-3.5 text-teal-600" /> (0010,0010) PatientName
            </span>
            <span class="text-teal-700 font-extrabold">PASS</span>
          </div>
          <div class="flex items-center justify-between py-0.5">
            <span class="flex items-center gap-1.5">
              <ShieldCheck class="w-3.5 h-3.5 text-teal-600" /> (0010,0020) PatientID
            </span>
            <span class="text-teal-700 font-extrabold">PASS</span>
          </div>
          <div class="flex items-center justify-between py-0.5">
            <span class="flex items-center gap-1.5">
              <ShieldCheck class="w-3.5 h-3.5 text-teal-600" /> (0008,0060) Modality
            </span>
            <span class="text-teal-700 font-extrabold">PASS</span>
          </div>
          <div class="flex items-center justify-between py-0.5">
            <span class="flex items-center gap-1.5">
              <ShieldCheck class="w-3.5 h-3.5 text-teal-600" /> (0018,0050) SliceThickness
            </span>
            <span class="text-teal-700 font-extrabold">1.0mm</span>
          </div>
        </div>
      </div>

    </div>

    <!-- CENTER PANEL: DENSE CT VIEWERS & GRAPHIC SLIDERS (6 columns) -->
    <div class="lg:col-span-6 space-y-4 flex flex-col">
      
      <div class="frosted-glass-panel flex-1 flex flex-col justify-between p-4 min-h-[480px]">
        
        <!-- Viewer Header -->
        <div class="flex items-center justify-between pb-2 border-b border-slate-200/50">
          <div class="text-[9px] font-mono text-slate-400 space-y-0.5 font-semibold">
            <div>MODALITY: {{ activePatient.modality }}</div>
            <div>RESOLUTION: 512 x 512 x 20 voxels &middot; Slice {{ currentSlice + 1 }} of 20</div>
          </div>
          
          <div class="flex items-center gap-2">
            <!-- Run AI segmentation trigger -->
            <button 
              v-if="activePatient.status === 'Ready' && !isInferenceRunning"
              @click="handleTriggerSegment"
              class="flex items-center gap-1 px-3 py-1.5 rounded-lg text-[9.5px] font-bold uppercase tracking-wider clinical-btn-primary active-shrink"
            >
              <Play class="w-3 h-3 fill-white" /> Run AI
            </button>
            <button 
              @click="handleResetWorkstation"
              class="flex items-center gap-1 text-[9px] font-bold rounded px-2.5 py-1.5 clinical-btn-secondary active-shrink"
            >
              <RotateCcw class="w-3 h-3" /> Reset
            </button>
          </div>
        </div>

        <!-- Rendered CT Anatomy Canvas (Grayscale & Segmentations) -->
        <div class="flex-1 flex items-center justify-center bg-black/95 rounded-xl border border-slate-800/80 my-4 relative overflow-hidden select-none min-h-[300px]">
          <!-- Ambient calibration crosshair background -->
          <div class="absolute inset-0 bg-[radial-gradient(rgba(255,255,255,0.015)_1px,transparent_1px)] bg-[size:16px_16px] pointer-events-none"></div>
          
          <!-- Outer CT Scanner circular gantry layout -->
          <div class="absolute w-[95%] h-[95%] rounded-full border border-dashed border-slate-800/40 pointer-events-none flex items-center justify-center">
            <div class="w-[90%] h-[90%] rounded-full border border-slate-800/20"></div>
          </div>

          <!-- PACS HUD OVERLAY: Top Left (Demographics) -->
          <div class="absolute top-3.5 left-4 text-[9px] font-mono text-slate-400 space-y-0.5 leading-normal pointer-events-none">
            <div class="font-bold text-slate-300">{{ activePatient.name }}</div>
            <div>MRN: {{ activePatient.id }}</div>
            <div>Age/Sex: {{ activePatient.age }}y / {{ activePatient.gender }}</div>
          </div>

          <!-- PACS HUD OVERLAY: Top Right (Scanner Specs) -->
          <div class="absolute top-3.5 right-4 text-[9px] font-mono text-slate-400 text-right space-y-0.5 leading-normal pointer-events-none">
            <div class="font-bold text-teal-500">LiversegAI v1.4.0</div>
            <div>kVp: 120 &middot; mAs: 250</div>
            <div>Thk: 1.0 mm</div>
          </div>

          <!-- PACS HUD OVERLAY: Bottom Left (Display Metrics) -->
          <div class="absolute bottom-3.5 left-4 text-[9px] font-mono text-slate-400 space-y-0.5 leading-normal pointer-events-none">
            <div>WW: {{ wwValue }} &middot; WL: {{ wlValue }}</div>
            <div>Zoom: 100% (Fit)</div>
            <div>Slice: {{ currentSlice + 1 }} / 20</div>
          </div>

          <!-- PACS HUD OVERLAY: Bottom Right (Orientation & Target Status) -->
          <div class="absolute bottom-3.5 right-4 text-[9px] font-mono text-slate-400 text-right space-y-0.5 leading-normal pointer-events-none">
            <div>Status: <span :class="activePatient.status === 'Completed' ? 'text-teal-400' : 'text-amber-500'">{{ activePatient.status }}</span></div>
            <div>PACS Router: Connected</div>
          </div>

          <!-- Anatomical Orientation Markers -->
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

            <!-- body fat wall -->
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

            <!-- crescent gantry -->
            <path d="M 12,74 C 25,92 75,92 88,74" fill="none" stroke="#2a2a2f" stroke-width="1.2" />

            <!-- rib bones -->
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

            <!-- stomach -->
            <path 
              v-if="currentSlice >= 2 && currentSlice <= 13"
              d="M 52,27 C 62,25 73,29 73,38 C 73,46 64,48 54,44 Z"
              fill="#101012" 
              stroke="#3f3f46" 
              stroke-width="0.6" 
            />

            <!-- spleen -->
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

            <!-- GROUND TRUTH CONTOUR -->
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

          <!-- Warning overlay if case is not yet segmented -->
          <div 
            v-if="activePatient.status === 'Ready' && !isInferenceRunning"
            class="absolute inset-0 bg-black/70 backdrop-blur-[2px] flex flex-col items-center justify-center gap-3 p-6 text-center"
          >
            <AlertCircle class="w-8 h-8 text-amber-500" />
            <h4 class="text-xs font-bold text-white uppercase tracking-wider">Volumetric data unsegmented</h4>
            <p class="text-[10px] text-slate-400 max-w-xs leading-normal">
              Click the "Run AI" button in the toolbar header or execute the pipeline below to render contours.
            </p>
          </div>

          <!-- Inference Telemetry Terminal overlay -->
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
            
            <div class="flex-1 bg-black/60 p-3 rounded border border-slate-850 font-mono text-[9px] text-teal-400 space-y-1 overflow-y-auto leading-normal my-2">
              <div v-for="(log, idx) in activeConsoleLogs" :key="idx" class="truncate select-none">
                {{ log }}
              </div>
            </div>
          </div>

        </div>

        <!-- Slice navigation slider -->
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

      <!-- PACS Graphics controls (Sliders) -->
      <div class="frosted-glass-panel p-4 grid grid-cols-1 md:grid-cols-3 gap-4">
        
        <div class="space-y-1">
          <div class="flex justify-between items-center text-[10px] text-slate-500 font-bold">
            <span>WW (Window Width)</span>
            <span class="font-mono">{{ wwValue }} HU</span>
          </div>
          <input 
            v-model.number="wwValue"
            type="range" min="100" max="800" step="10"
            class="w-full accent-teal-600 cursor-pointer bg-slate-100 h-1 rounded-full"
          />
        </div>

        <div class="space-y-1">
          <div class="flex justify-between items-center text-[10px] text-slate-500 font-bold">
            <span>WL (Window Level)</span>
            <span class="font-mono">{{ wlValue }} HU</span>
          </div>
          <input 
            v-model.number="wlValue"
            type="range" min="-100" max="200" step="5"
            class="w-full accent-teal-600 cursor-pointer bg-slate-100 h-1 rounded-full"
          />
        </div>

        <div class="space-y-1">
          <div class="flex justify-between items-center text-[10px] text-slate-500 font-bold">
            <span>Teal Mask Opacity</span>
            <span class="font-mono">{{ maskOpacity }}%</span>
          </div>
          <input 
            v-model.number="maskOpacity"
            type="range" min="0" max="100" step="5"
            class="w-full accent-teal-600 cursor-pointer bg-slate-100 h-1 rounded-full"
          />
        </div>

      </div>

    </div>

    <!-- RIGHT PANEL: ML METRICS, FINDINGS & SIGN-OFF (3 columns) -->
    <div class="lg:col-span-3 space-y-6">
      
      <!-- Diagnostic Analytics Metrics -->
      <div class="frosted-glass-panel p-4 space-y-4">
        <h4 class="text-[10px] font-bold uppercase tracking-wider text-slate-500 font-extrabold border-b border-slate-200/50 pb-2 flex items-center gap-1.5">
          <BrainCircuit class="w-4 h-4 text-teal-650" /> Segmentation Analytics
        </h4>

        <div class="grid grid-cols-2 gap-2 text-xs font-semibold">
          <div class="bg-white/60 p-2 rounded border border-slate-200/50">
            <div class="text-[8px] text-slate-400 font-bold uppercase">Dice Score</div>
            <div class="text-sm font-extrabold text-teal-700 mt-0.5">{{ activePatient.metrics.dice }}</div>
          </div>
          <div class="bg-white/60 p-2 rounded border border-slate-200/50">
            <div class="text-[8px] text-slate-400 font-bold uppercase">Mean IoU</div>
            <div class="text-sm font-extrabold text-slate-800 mt-0.5">{{ activePatient.metrics.iou }}</div>
          </div>
          <div class="bg-white/60 p-2 rounded border border-slate-200/50">
            <div class="text-[8px] text-slate-400 font-bold uppercase">Confidence</div>
            <div class="text-sm font-extrabold text-slate-800 mt-0.5">{{ activePatient.metrics.confidence }}</div>
          </div>
          <div class="bg-white/60 p-2 rounded border border-slate-200/50">
            <div class="text-[8px] text-slate-400 font-bold uppercase">Inference Time</div>
            <div class="text-sm font-extrabold text-slate-800 mt-0.5">{{ activePatient.metrics.processingTime }}</div>
          </div>
          <div class="bg-white/60 p-2 rounded border border-slate-200/50 col-span-2">
            <div class="text-[8px] text-slate-400 font-bold uppercase">Estimated Liver Volume</div>
            <div class="text-sm font-extrabold text-slate-850 mt-0.5">{{ activePatient.metrics.volume }}</div>
          </div>
        </div>

        <!-- Render toggles -->
        <div class="pt-2 border-t border-slate-100 space-y-2">
          <label class="flex items-center justify-between text-[10px] font-bold text-slate-600 cursor-pointer select-none">
            <span>Show Ground Truth contour</span>
            <input v-model="showGroundTruth" type="checkbox" class="rounded text-teal-600 focus:ring-teal-500 border-slate-300" />
          </label>
          <label class="flex items-center justify-between text-[10px] font-bold text-slate-600 cursor-pointer select-none">
            <span>Show Tumoral lesions</span>
            <input v-model="showLesions" type="checkbox" class="rounded text-teal-600 focus:ring-teal-500 border-slate-300" />
          </label>
        </div>
      </div>

      <!-- Clinical Report summary -->
      <div class="frosted-glass-panel p-4 space-y-3">
        <h4 class="text-[10px] font-bold uppercase tracking-wider text-slate-500 font-extrabold border-b border-slate-200/50 pb-2">
          Volumetric Findings &amp; Summary
        </h4>
        <textarea 
          v-model="activePatient.findings"
          rows="4"
          class="w-full bg-white/80 border border-slate-200 rounded-lg p-2 text-[10px] font-semibold text-slate-600 focus:outline-none focus:border-teal-500 focus:bg-white leading-relaxed"
        ></textarea>
      </div>

      <!-- Clinical sign-off -->
      <div class="frosted-glass-panel p-4 space-y-3">
        <h4 class="text-[10px] font-bold uppercase tracking-wider text-slate-500 font-extrabold border-b border-slate-200/50 pb-2">
          QA Workstation Validation
        </h4>

        <div class="space-y-2 text-[10px] text-slate-655 text-slate-600 font-semibold">
          <label class="flex items-start gap-2 cursor-pointer select-none">
            <input v-model="chkContours" type="checkbox" class="mt-0.5 rounded text-teal-600 focus:ring-teal-500 border-slate-300" />
            <span>Anatomical margins verified across 20 slices</span>
          </label>
          <label class="flex items-start gap-2 cursor-pointer select-none">
            <input v-model="chkOutliers" type="checkbox" class="mt-0.5 rounded text-teal-600 focus:ring-teal-500 border-slate-300" />
            <span>No AI mask artifact anomalies observed</span>
          </label>
        </div>

        <div class="pt-2 border-t border-slate-100">
          <button 
            v-if="!isSigned"
            @click="handleSignReport"
            :disabled="activePatient.status !== 'Completed'"
            class="flex items-center justify-center gap-1.5 w-full py-2 rounded-lg text-[10px] font-bold uppercase tracking-wider disabled:opacity-50 clinical-btn-primary active-shrink"
          >
            <CheckCircle class="w-3.5 h-3.5" /> Sign Report &amp; Approve
          </button>
          
          <div v-else class="space-y-2">
            <div class="p-2 bg-emerald-50/70 border border-emerald-100 rounded-lg text-center text-[10.5px] text-emerald-800 font-bold flex items-center justify-center gap-1">
              <CheckCircle class="w-3.5 h-3.5" /> Approved
            </div>
            <button 
              @click="handleExportPacs"
              :disabled="isExporting || exportSuccess"
              class="flex items-center justify-center gap-1.5 w-full py-2 rounded-lg text-[10px] font-bold uppercase tracking-wider clinical-btn-primary active-shrink"
            >
              <Loader2 v-if="isExporting" class="w-3.5 h-3.5 animate-spin" />
              <Share2 v-else class="w-3.5 h-3.5" />
              {{ exportSuccess ? 'Exported to PACS' : 'Export DICOM to PACS' }}
            </button>
          </div>
        </div>
      </div>

    </div>

  </div>

  <div v-else class="flex flex-col items-center justify-center h-[calc(100vh-8.5rem)] opacity-70">
    <AlertCircle class="w-12 h-12 text-slate-400 mb-4" />
    <h3 class="text-lg font-black text-slate-700 uppercase tracking-wider">No Active Patient</h3>
    <p class="text-sm text-slate-500 font-semibold mt-1">Please upload a scan or select a patient from the dashboard.</p>
  </div>
</template>
