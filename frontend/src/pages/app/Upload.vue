<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAppState } from '../../composables/useAppState'
import api from '../../api'
import {
  UploadCloud, FileText, CheckCircle2, Loader2, AlertCircle,
  X, ShieldCheck, ChevronRight, Database, Zap, Play, RotateCcw,
  ChevronLeft, BrainCircuit, Activity, Sliders, Layers, Award, CheckSquare, FileSignature
} from 'lucide-vue-next'
import CTViewer from '../../components/CTViewer.vue'
import MetricsPanel from '../../components/MetricsPanel.vue'


const router = useRouter()
const {
  uploadQueue,
  realUpload,
  patients,
  activePatient,
  selectPatient,
  runSegmentation,
  isInferenceRunning,
  inferenceProgress,
  inferenceStage
} = useAppState()

const uploadError = ref('')

const currentStep = ref(1)

const isDragging = ref(false)
const findingsText = ref('')
const signature = ref('')
const qaChecked = ref({
  parenchyma: false,
  lesions: false,
  margins: false,
  artifacts: false
})
const isReportSaved = ref(false)

// Viewer Controls
const currentSlice = ref(10)
const wwValue = ref(400) // Window Width
const wlValue = ref(40)  // Window Level
const maskOpacity = ref(65) // Percentage opacity of teal mask
const showGroundTruth = ref(false)
const showLesions = ref(true)

// Sync steps based on patient file status and processing state
watch(activePatient, (p) => {
  if (!p) {
    currentStep.value = 1
  } else if (!p.hasFile) {
    currentStep.value = 1
  } else if (p.status === 'Ready') {
    currentStep.value = 2
  } else if (p.status === 'Analyzing') {
    currentStep.value = 3
  } else if (p.status === 'Completed') {
    // If completed and we are not already on visualize or report, reset to visualize
    if (currentStep.value < 4) {
      currentStep.value = 4
    }
  }
  
  // Load findings and signature from patient if they exist
  if (p) {
    findingsText.value = p.findings || ''
    signature.value = p.signature || ''
    isReportSaved.value = !!p.signature
  }
}, { immediate: true })

watch(isInferenceRunning, (running) => {
  if (running) {
    currentStep.value = 3
  } else if (activePatient.value?.status === 'Completed') {
    currentStep.value = 4
  }
})

const handleDragOver = (e) => { e.preventDefault(); isDragging.value = true }
const handleDragLeave = () => { isDragging.value = false }
const handleDrop = (e) => { e.preventDefault(); isDragging.value = false; processFiles(e.dataTransfer.files) }
const handleFileSelect = (e) => processFiles(e.target.files)

const processFiles = async (files) => {
  uploadError.value = ''
  for (const file of files) {
    const filename = file.name.toLowerCase()
    let type = 'unknown'
    if (filename.endsWith('.dcm')) type = 'dicom'
    else if (filename.endsWith('.nii') || filename.endsWith('.nii.gz')) type = 'nifti'
    else if (filename.endsWith('.pdf')) type = 'pdf'

    if (type === 'unknown') {
      const ext = filename.split('.').pop()
      uploadError.value = `Format .${ext} not supported. Use .nii, .nii.gz, or .dcm.`
      continue
    }

    if (!activePatient.value) {
      uploadError.value =
        'Please select a patient before uploading a scan.'
      return
    }

    try {
      await realUpload(
        file,
        activePatient.value.id
      )
    }
    catch(error) {

      uploadError.value =
        error.response?.data?.error ||
        'Upload failed'

    }
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
  maskOpacity.value = 65
  showGroundTruth.value = false
  showLesions.value = true
}

const saveReport = async () => {
  if (!activePatient.value) return
  try {
    const res = await api.patch(`/patients/${activePatient.value.id}/`, {
      findings: findingsText.value,
      signature: signature.value,
      status: 'Completed'
    })
    if (res.data) {
      activePatient.value.findings = res.data.findings
      activePatient.value.signature = res.data.signature
      isReportSaved.value = true
    }
  } catch (error) {
    console.error('Error saving patient report:', error)
  }
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

const stepsList = [
  { id: 1, name: 'Upload Scan', icon: UploadCloud },
  { id: 2, name: 'Preview', icon: Database },
  { id: 3, name: 'AI Core Processing', icon: BrainCircuit },
  { id: 4, name: 'Visualize Slices', icon: Layers },
  { id: 5, name: 'Metrics', icon: Award },
  { id: 6, name: 'Report', icon: FileText }
]

const canNavigateTo = (stepId) => {
  if (!activePatient.value) return stepId === 1
  if (stepId === 1) return true
  if (stepId === 2) return activePatient.value.hasFile
  if (stepId === 3) return activePatient.value.hasFile && (activePatient.value.status === 'Analyzing' || activePatient.value.status === 'Completed' || activePatient.value.status === 'Ready')
  if (stepId === 4) return activePatient.value.status === 'Completed'
  if (stepId === 5) return activePatient.value.status === 'Completed'
  if (stepId === 6) return activePatient.value.status === 'Completed'
  return false
}

const navigateToStep = (stepId) => {
  if (canNavigateTo(stepId)) {
    currentStep.value = stepId
  }
}
</script>

<template>
  <div class="space-y-5 animate-fade-in-up">

    <!-- Header Block -->
    <div class="frosted-glass-panel p-5 flex flex-wrap items-center justify-between gap-4">
      <div>
        <div class="section-title uppercase tracking-widest text-[10px] text-teal-600 font-bold">Workspace Ingest Pipeline</div>
        <h2 class="text-sm font-black text-slate-800 mt-0.5">Clinical Workstation Upload Hub</h2>
        <p class="text-[10px] text-slate-500 font-medium mt-0.5">Ingest patient volume scans and evaluate real-time mask segmentation directly</p>
      </div>
      <button @click="router.push('/app/analysis')" class="clinical-btn-secondary flex items-center gap-2 px-3 py-2 rounded-xl text-xs font-bold active-shrink">
        Open Analysis Workspace <ChevronRight class="w-3.5 h-3.5" />
      </button>
    </div>

    <!-- Horizontal Wizard Steps Progress Tracker -->
    <div class="frosted-glass-panel p-4 overflow-x-auto clinical-scrollbar">
      <div class="flex items-center justify-between min-w-[700px] px-4">
        <div 
          v-for="(step, idx) in stepsList" 
          :key="step.id"
          class="flex items-center flex-1 last:flex-initial"
        >
          <!-- Active, Completed, or Locked indicators -->
          <button 
            @click="navigateToStep(step.id)"
            :disabled="!canNavigateTo(step.id)"
            class="flex items-center gap-2 group focus:outline-none disabled:cursor-not-allowed text-left"
          >
            <div 
              :class="[
                'w-8 h-8 rounded-xl flex items-center justify-center border transition-all duration-300 font-bold text-xs shadow-sm',
                currentStep === step.id 
                  ? 'bg-teal-500 border-teal-500 text-white ring-2 ring-teal-500/20' 
                  : canNavigateTo(step.id) 
                    ? 'bg-teal-50 border-teal-200 text-teal-650 hover:bg-teal-100/50' 
                    : 'bg-slate-50 border-slate-200 text-slate-400'
              ]"
            >
              <component :is="step.icon" class="w-4 h-4" />
            </div>
            <div class="leading-none select-none">
              <div class="text-[8px] uppercase tracking-wider text-slate-400 font-bold">Step 0{{ step.id }}</div>
              <div 
                :class="[
                  'text-[10px] font-bold tracking-tight',
                  currentStep === step.id ? 'text-teal-600' : canNavigateTo(step.id) ? 'text-slate-700 group-hover:text-slate-900' : 'text-slate-400'
                ]"
              >
                {{ step.name }}
              </div>
            </div>
          </button>

          <!-- Connector Line -->
          <div 
            v-if="idx < stepsList.length - 1"
            :class="[
              'h-[1.5px] flex-1 mx-4 transition-all duration-300',
              canNavigateTo(step.id + 1) ? 'bg-teal-500/30' : 'bg-slate-200'
            ]"
          />
        </div>
      </div>
    </div>

    <!-- Active Workspace Patient Selection (Float Bar) -->
    <div class="frosted-glass-panel p-4 flex flex-wrap items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 rounded-lg bg-teal-50 text-teal-600 flex items-center justify-center border border-teal-100 shadow-sm">
          <Database class="w-4 h-4" />
        </div>
        <div>
          <div class="text-[9px] font-bold uppercase text-slate-400">Active Workspace Patient</div>
          <div class="text-xs font-bold text-slate-800">{{ activePatient ? `${activePatient.name} (${activePatient.id})` : 'No Patient Selected' }}</div>
        </div>
      </div>
      <div class="flex items-center gap-3">
        <label class="block text-[9px] font-bold text-slate-500 uppercase">Change Active Case:</label>
        <select
          :value="activePatient?.id"
          @change="selectPatient($event.target.value)"
          class="bg-white/80 border border-slate-200 rounded-lg px-2.5 py-1 text-xs font-bold text-slate-800 focus:outline-none focus:border-teal-500"
        >
          <option v-for="p in patients" :key="p.id" :value="p.id">
            {{ p.name }} ({{ p.id }})
          </option>
        </select>
      </div>
    </div>

    <!-- ════════════════════════════════════════
         WIZARD STEP VIEWS
    ════════════════════════════════════════ -->
    <div class="grid grid-cols-1 gap-5">

      <!-- STEP 1: Upload Scans -->
      <div v-if="currentStep === 1" class="grid grid-cols-1 lg:grid-cols-12 gap-5">
        <div class="lg:col-span-8 frosted-glass-panel p-6 space-y-6">
          <div class="flex items-center justify-between border-b border-slate-100 pb-3">
            <h3 class="text-sm font-black text-slate-850 flex items-center gap-2"><UploadCloud class="w-4 h-4 text-teal-650" /> Ingest New Volume Scan</h3>
            <span class="text-[9px] font-bold text-slate-400 bg-slate-50 border px-2 py-0.5 rounded">PostgreSQL Link</span>
          </div>

          <div
            @dragover="handleDragOver" @dragleave="handleDragLeave" @drop="handleDrop"
            :class="[
              'border-2 border-dashed rounded-2xl p-12 flex flex-col items-center justify-center gap-4 text-center transition-all cursor-pointer min-h-[220px]',
              isDragging ? 'border-teal-500 bg-teal-50/40 scale-[1.01]' : 'border-slate-200 bg-white/30 hover:border-teal-400 hover:bg-teal-50/20'
            ]"
          >
            <input id="file-upload" type="file" class="hidden" multiple accept=".dcm,.nii,.nii.gz,.pdf" @change="handleFileSelect" />
            <label for="file-upload" class="cursor-pointer">
              <div class="w-14 h-14 rounded-full bg-teal-50 border border-teal-100 flex items-center justify-center mx-auto mb-2">
                <UploadCloud class="w-6 h-6 text-teal-600" />
              </div>
              <div class="text-xs font-bold text-slate-700">Drag & drop DICOM or NIfTI slice data</div>
              <div class="text-[10px] text-slate-400 font-medium mt-1">or <span class="text-teal-650 font-black">click to browse local files</span></div>
              <div class="text-[9px] text-slate-450 font-bold mt-2 bg-slate-100/80 border border-slate-200/60 px-3.5 py-1.5 rounded-full inline-block">
                DICOM (.dcm) · NIfTI (.nii/.nii.gz) · PDF Reports
              </div>
            </label>
          </div>

          <!-- Upload error display -->
          <div v-if="uploadError" class="flex items-center gap-2 p-3 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-700 font-semibold">
            <AlertCircle class="w-4 h-4 flex-shrink-0" />
            {{ uploadError }}
            <button @click="uploadError = ''" class="ml-auto text-rose-400 hover:text-rose-600">✕</button>
          </div>

          <!-- Upload mode indicator -->
          <div class="flex items-center gap-2 text-[9px] font-semibold">
            <span v-if="activePatient" class="flex items-center gap-1.5 text-teal-700 bg-teal-50 border border-teal-100 px-2.5 py-1 rounded-full">
              <span class="w-1.5 h-1.5 bg-teal-500 rounded-full"></span>
              Real upload mode — files sent to backend for patient {{ activePatient.id }}
            </span>
            <span v-else class="flex items-center gap-1.5 text-amber-700 bg-amber-50 border border-amber-100 px-2.5 py-1 rounded-full">
              <span class="w-1.5 h-1.5 bg-amber-500 rounded-full"></span>
                Select a patient before uploading.            </span>
          </div>
        </div>

        <div class="lg:col-span-4 space-y-4">
          <!-- Active progress -->
          <div class="frosted-glass-panel p-5 space-y-3 min-h-[140px]">
            <div class="section-title">Active Upload Ingestion</div>
            <div v-if="uploadQueue.filter(u => u.status === 'uploading').length === 0" class="text-xs text-slate-400 py-4 font-semibold italic text-center">
              No active uploads currently in queue.
            </div>
            <div v-for="u in uploadQueue.filter(u => u.status === 'uploading')" :key="u.id" class="p-3 bg-sky-50/65 border border-sky-100 rounded-xl">
              <div class="flex items-center justify-between mb-1.5">
                <span class="text-[10px] font-bold text-slate-700 truncate max-w-[80%]">{{ u.filename }}</span>
                <span class="text-[9px] font-bold text-sky-600">{{ u.progress }}%</span>
              </div>
              <div class="progress-track h-1.5">
                <div class="progress-fill" :style="`width:${u.progress}%`"></div>
              </div>
            </div>
          </div>

          <!-- Recently Completed files -->
          <div class="frosted-glass-panel p-5 space-y-3">
            <div class="section-title">Upload Log History</div>
            <div v-if="uploadQueue.filter(u => u.status === 'completed').length === 0" class="text-xs text-slate-400 py-4 font-semibold italic text-center">
              No files uploaded yet in this session.
            </div>
            <div class="space-y-2">
              <div v-for="u in uploadQueue.filter(u => u.status === 'completed').slice(-3)" :key="u.id"
                class="flex items-center gap-2 p-2 bg-white/60 border border-slate-200/50 rounded-xl"
              >
                <CheckCircle2 class="w-4 h-4 text-teal-500 flex-shrink-0" />
                <span class="text-[9.5px] font-semibold text-slate-700 truncate flex-1">{{ u.filename }}</span>
                <span class="text-[8px] font-bold text-slate-400 uppercase bg-slate-50 border px-1.5 py-0.5 rounded">{{ u.type }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- STEP 2: Preview -->
      <div v-if="currentStep === 2" class="grid grid-cols-1 lg:grid-cols-12 gap-5">
        <div class="lg:col-span-7 frosted-glass-panel p-6 space-y-6">
          <div class="flex items-center justify-between border-b border-slate-100 pb-3">
            <h3 class="text-sm font-black text-slate-850 flex items-center gap-2"><Database class="w-4 h-4 text-teal-650" /> Volumetric Metadata Preview</h3>
            <span class="text-[9.5px] font-bold text-teal-650 bg-teal-50 px-2 py-0.5 rounded uppercase tracking-wider">File Ingested</span>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div class="p-3.5 bg-slate-50 border border-slate-200/50 rounded-2xl">
              <div class="text-[9px] font-bold text-slate-400 uppercase">Patient Name</div>
              <div class="text-xs font-black text-slate-800 mt-0.5">{{ activePatient?.name }}</div>
            </div>
            <div class="p-3.5 bg-slate-50 border border-slate-200/50 rounded-2xl">
              <div class="text-[9px] font-bold text-slate-400 uppercase">Patient Age / Gender</div>
              <div class="text-xs font-black text-slate-800 mt-0.5">{{ activePatient?.age }}y / {{ activePatient?.gender }}</div>
            </div>
            <div class="p-3.5 bg-slate-50 border border-slate-200/50 rounded-2xl">
              <div class="text-[9px] font-bold text-slate-400 uppercase">Registered DOB</div>
              <div class="text-xs font-black text-slate-800 mt-0.5">{{ activePatient?.dob }}</div>
            </div>
            <div class="p-3.5 bg-slate-50 border border-slate-200/50 rounded-2xl">
              <div class="text-[9px] font-bold text-slate-400 uppercase">Scan Date & Modality</div>
              <div class="text-xs font-black text-slate-800 mt-0.5">{{ activePatient?.scanDate?.substring(0, 10) }} ({{ activePatient?.modality }})</div>
            </div>
          </div>
        </div>

        <div class="lg:col-span-5 frosted-glass-panel p-6 flex flex-col justify-between space-y-6">
          <div class="space-y-4">
            <div class="w-12 h-12 rounded-2xl bg-teal-50 border border-teal-150 flex items-center justify-center text-teal-600 shadow-sm">
              <BrainCircuit class="w-6 h-6 animate-pulse" />
            </div>
            <div class="space-y-2">
              <h3 class="font-black text-slate-900 text-base leading-snug tracking-tight">AI Segmentation Pipeline Ready</h3>
              <p class="text-xs text-slate-500 leading-relaxed font-semibold">
                The DICOM scan series has been normalized to target resolutions. The backend liver segmentation pipeline can now be triggered.
              </p>
            </div>

            <div class="p-3.5 bg-sky-50/65 border border-sky-100 rounded-xl flex items-start gap-2.5 text-[11px] text-sky-850 font-semibold leading-relaxed">
              <Activity class="w-4 h-4 text-sky-600 mt-0.5 flex-shrink-0" />
              <span>Pipeline processes uploaded NIFTI volumes and creates an overlayed mask to isolate liver lobes, masking extraneous anatomy for precise measurements.</span>
            </div>
          </div>

          <button 
            @click="handleTriggerSegment"
            class="w-full flex items-center justify-center gap-2 py-3.5 text-xs font-bold uppercase tracking-wider rounded-xl clinical-btn-primary active-shrink"
          >
            <Play class="w-4 h-4 fill-white" /> Initialize AI Inference
          </button>
        </div>
      </div>

      <!-- STEP 3: AI Processing -->
      <div v-if="currentStep === 3" class="frosted-glass-panel p-6 space-y-6 max-w-4xl mx-auto">
        <div class="flex items-center justify-between border-b border-slate-100 pb-3">
          <h3 class="text-sm font-black text-slate-850 flex items-center gap-2"><Loader2 class="w-4 h-4 animate-spin text-teal-550" />Volumetric Segmentation Pipeline</h3>
          <span class="text-[9.5px] font-bold text-slate-400 bg-slate-50 border px-2 py-0.5 rounded">GPU Slot Engaged</span>
        </div>

        <div class="space-y-3">
          <div class="flex justify-between text-xs font-bold text-slate-700">
            <span>{{ inferenceStage }}</span>
            <span class="text-teal-600">{{ inferenceProgress }}%</span>
          </div>
          <div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden border border-slate-200/50">
            <div class="bg-teal-500 h-full transition-all duration-200" :style="{ width: inferenceProgress + '%' }"></div>
          </div>
        </div>

        <!-- Terminal log console -->
        <div class="space-y-2">
          <div class="text-[9px] font-bold uppercase text-slate-400">Pipeline Pipeline Engine Console Output:</div>
          <div class="h-60 bg-slate-900 rounded-2xl p-4 font-mono text-[10px] text-teal-400 space-y-1.5 overflow-y-auto leading-normal shadow-inner border border-slate-800">
            <div v-if="activeConsoleLogs.length === 0" class="text-slate-500 italic select-none">
              Connecting to local inference socket...
            </div>
            <div v-for="(log, idx) in activeConsoleLogs" :key="idx" class="truncate select-none">
              {{ log }}
            </div>
          </div>
        </div>
      </div>

      <!-- STEP 4: Visualize Slices -->
      <div v-if="currentStep === 4" class="grid grid-cols-1 lg:grid-cols-12 gap-5">
        <!-- Visualizer Area (8 cols) -->
        <div class="lg:col-span-8">
          <CTViewer 
            :patient="activePatient"
            v-model:currentSlice="currentSlice"
            :ww="wwValue"
            :wl="wlValue"
            :maskOpacity="maskOpacity"
            :showGroundTruth="showGroundTruth"
            :showLesions="showLesions"
          />
        </div>

        <!-- Right Side Panel: Diagnostics & Contrast Sliders (4 cols) -->
        <div class="lg:col-span-4">
          <MetricsPanel 
            :patient="activePatient"
            v-model:ww="wwValue"
            v-model:wl="wlValue"
            v-model:opacity="maskOpacity"
            v-model:showGroundTruth="showGroundTruth"
            v-model:showLesions="showLesions"
            @proceed="currentStep = 5"
          />
        </div>
      </div>

      <!-- STEP 5: Results Metrics -->
      <div v-if="currentStep === 5" class="space-y-5 max-w-4xl mx-auto">
        <div class="frosted-glass-panel p-6 space-y-6">
          <div class="flex items-center justify-between border-b border-slate-100 pb-3">
            <h3 class="text-sm font-black text-slate-850 flex items-center gap-2"><Award class="w-4 h-4 text-teal-655" /> AI Model Quantitative Metrics</h3>
            <span class="text-[9.5px] font-bold text-teal-655 bg-teal-50 px-2 py-0.5 rounded border border-teal-100">Dice Accuracy Validated</span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div class="p-5 rounded-2xl border border-teal-200/50 bg-teal-50/20 text-center space-y-1 shadow-sm">
              <div class="text-3xl font-black text-teal-700">{{ activePatient?.metrics?.dice ?? 'N/A' }}</div>
              <div class="text-[9px] text-slate-500 uppercase tracking-wider font-bold">Dice Coefficient</div>
              <div class="text-[8px] text-teal-600 font-semibold leading-normal">Volumetric overlap index</div>
            </div>
            <div class="p-5 rounded-2xl border border-slate-200/60 bg-white/45 text-center space-y-1 shadow-sm">
              <div class="text-3xl font-black text-slate-800">{{ activePatient?.metrics?.iou ?? 'N/A' }}</div>
              <div class="text-[9px] text-slate-500 uppercase tracking-wider font-bold">Mean IoU</div>
              <div class="text-[8px] text-slate-400 font-semibold leading-normal">Intersection over Union</div>
            </div>
            <div class="p-5 rounded-2xl border border-slate-200/60 bg-white/45 text-center space-y-1 shadow-sm">
              <div class="text-3xl font-black text-slate-800">{{ activePatient?.metrics?.precision ?? 'N/A' }}</div>
              <div class="text-[9px] text-slate-500 uppercase tracking-wider font-bold">Precision</div>
              <div class="text-[8px] text-slate-400 font-semibold leading-normal">Voxel false positive suppression</div>
            </div>
            <div class="p-5 rounded-2xl border border-slate-200/60 bg-white/45 text-center space-y-1 shadow-sm">
              <div class="text-3xl font-black text-slate-800">{{ activePatient?.metrics?.recall ?? 'N/A' }}</div>
              <div class="text-[9px] text-slate-500 uppercase tracking-wider font-bold">Recall</div>
              <div class="text-[8px] text-slate-400 font-semibold leading-normal">Target boundary sensitivity</div>
            </div>
          </div>

          <div class="p-4 bg-slate-50 border border-slate-200/60 rounded-2xl space-y-2 text-xs font-semibold text-slate-600">
            <div class="text-slate-800 font-bold text-[10px] uppercase tracking-wider flex items-center gap-1.5"><Sliders class="w-3.5 h-3.5 text-teal-600" /> Derived Tissue Volumetrics:</div>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-1 font-medium">
              <div><span class="text-slate-450">Liver Volume:</span> <span class="text-slate-800 font-bold">{{ activePatient?.metrics?.volume ?? 'N/A' }} cm³ </span></div>
              <div><span class="text-slate-455 text-slate-400">Lesions Found:</span> <span :class="activePatient?.hasLesions ? 'text-rose-600 font-bold' : 'text-slate-800 font-bold'">{{ activePatient?.hasLesions ? 'Yes' : 'No' }}</span></div>
              <div><span class="text-slate-455 text-slate-400">Lesion Volume:</span> <span class="text-slate-800 font-bold">{{ activePatient?.lesionVolume || '—' }}</span></div>
              <div><span class="text-slate-455 text-slate-400">Resolution spacing:</span> <span class="text-slate-800 font-mono font-bold">1.0mm isotropic</span></div>
            </div>
          </div>
        </div>

        <div class="flex justify-end gap-3">
          <button 
            @click="currentStep = 4" 
            class="px-5 py-3 text-xs font-bold uppercase tracking-wider rounded-xl clinical-btn-secondary active-shrink"
          >
            Back to Visualize
          </button>
          <button 
            @click="currentStep = 6" 
            class="px-5 py-3 text-xs font-bold uppercase tracking-wider rounded-xl clinical-btn-primary active-shrink flex items-center gap-1.5"
          >
            Draft Diagnostic Report <ChevronRight class="w-4 h-4" />
          </button>
        </div>
      </div>

      <!-- STEP 6: Report -->
      <div v-if="currentStep === 6" class="space-y-5 max-w-4xl mx-auto">
        <div class="frosted-glass-panel p-6 space-y-6">
          <div class="flex items-center justify-between border-b border-slate-100 pb-3">
            <h3 class="text-sm font-black text-slate-850 flex items-center gap-2"><FileText class="w-4 h-4 text-teal-655" /> Diagnostic Report Verification</h3>
            <span class="text-[9.5px] font-bold text-slate-450 bg-slate-50 border px-2 py-0.5 rounded">FDA Class II Secondary Assist</span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- QA Checklist -->
            <div class="space-y-4">
              <h4 class="text-xs font-black text-slate-800 uppercase tracking-wider flex items-center gap-1.5"><CheckSquare class="w-4 h-4 text-teal-600" /> Clinician Verification Checklist</h4>
              <div class="space-y-3 bg-white/45 border border-slate-200/50 p-4 rounded-2xl">
                <label class="flex items-start gap-2.5 text-xs font-semibold text-slate-700 cursor-pointer select-none">
                  <input v-model="qaChecked.parenchyma" type="checkbox" class="rounded text-teal-600 border-slate-350 mt-0.5" />
                  <div>
                    <span class="font-bold">Liver parenchyma contour verified</span>
                    <p class="text-[9px] text-slate-400 mt-0.5">Segment accurately traces outer boundaries on all axial frames.</p>
                  </div>
                </label>

                <label class="flex items-start gap-2.5 text-xs font-semibold text-slate-700 cursor-pointer select-none">
                  <input v-model="qaChecked.lesions" type="checkbox" class="rounded text-teal-600 border-slate-350 mt-0.5" />
                  <div>
                    <span class="font-bold">lesion locations verified</span>
                    <p class="text-[9px] text-slate-400 mt-0.5">Identified hyperdense/hypodense nodules correlate with diagnostic scans.</p>
                  </div>
                </label>

                <label class="flex items-start gap-2.5 text-xs font-semibold text-slate-700 cursor-pointer select-none">
                  <input v-model="qaChecked.margins" type="checkbox" class="rounded text-teal-600 border-slate-350 mt-0.5" />
                  <div>
                    <span class="font-bold">Vascular margin thresholds checked</span>
                    <p class="text-[9px] text-slate-400 mt-0.5">Voxel boundaries avoid hepatic and portal vein overlap structures.</p>
                  </div>
                </label>

                <label class="flex items-start gap-2.5 text-xs font-semibold text-slate-700 cursor-pointer select-none">
                  <input v-model="qaChecked.artifacts" type="checkbox" class="rounded text-teal-600 border-slate-350 mt-0.5" />
                  <div>
                    <span class="font-bold">Ingest artifacts scan checks passed</span>
                    <p class="text-[9px] text-slate-400 mt-0.5">No movement artifacts or respiratory breathing gaps degrade precision.</p>
                  </div>
                </label>
              </div>
            </div>

            <!-- Findings editor -->
            <div class="space-y-4">
              <h4 class="text-xs font-black text-slate-800 uppercase tracking-wider flex items-center gap-1.5"><FileSignature class="w-4 h-4 text-teal-600" /> Clinical Diagnostic Findings</h4>
              
              <div class="space-y-4">
                <div>
                  <label class="block text-[9px] font-bold text-slate-500 uppercase mb-1">Diagnostic Summary / Clinical Notes</label>
                  <textarea 
                    v-model="findingsText"
                    rows="4" 
                    placeholder="Enter patient findings, tumor sizing benchmarks, liver parenchymal anomalies, or anatomical descriptions..."
                    class="clinical-input w-full p-3 text-xs font-semibold"
                  ></textarea>
                </div>

                <div>
                  <label class="block text-[9px] font-bold text-slate-500 uppercase mb-1">Attending Radiologist Digital Signature</label>
                  <input 
                    v-model="signature"
                    type="text" 
                    placeholder="Dr. Jane Smith, MD" 
                    class="clinical-input w-full px-3.5 py-2 text-xs font-bold"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- Save/PACS Router -->
          <div class="p-4 bg-sky-50/65 border border-sky-100 rounded-2xl flex items-start gap-3">
            <ShieldCheck class="w-5 h-5 text-sky-600 flex-shrink-0 mt-0.5" />
            <div>
              <h4 class="text-xs font-bold text-slate-800">Secure Database &amp; PACS Routing Sync</h4>
              <p class="text-[10px] text-slate-500 leading-relaxed font-semibold mt-0.5">
                Signing this case will update the patient record in PostgreSQL. If auto-route is enabled, the structured reports and volumetric masks will be pushed directly back to the active AE Title host.
              </p>
            </div>
          </div>

          <div v-if="isReportSaved" class="p-3 bg-teal-50 border border-teal-150 rounded-xl text-center text-xs font-bold text-teal-700">
            ✓ Report successfully saved to database &amp; routed to PACS server queue.
          </div>
        </div>

        <div class="flex justify-end gap-3">
          <button 
            @click="currentStep = 5" 
            class="px-5 py-3 text-xs font-bold uppercase tracking-wider rounded-xl clinical-btn-secondary active-shrink"
          >
            Back to Metrics
          </button>
          <button 
            @click="saveReport" 
            class="px-6 py-3.5 text-xs font-bold uppercase tracking-wider rounded-xl clinical-btn-primary active-shrink flex items-center gap-1.5"
          >
            Save &amp; Route to PACS
          </button>
        </div>
      </div>

    </div>

  </div>
</template>
