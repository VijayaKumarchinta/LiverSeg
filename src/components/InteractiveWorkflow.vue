<script setup>
import { ref, watch } from 'vue'
import { 
  Upload, 
  Sliders, 
  Brain, 
  ScanLine, 
  Stethoscope, 
  FileText, 
  Check, 
  Play, 
  RefreshCw, 
  Loader2, 
  ChevronRight,
  Database,
  Layers,
  Sparkles
} from 'lucide-vue-next'

const activeStep = ref(0)

// Simulated Upload States
const uploadedFiles = ref([
  { name: 'IMG_084_PORTAL_VEIN.dcm', size: '12.4 MB', status: 'ready', series: 'Axial Portal Venous Phase' },
  { name: 'IMG_085_PORTAL_VEIN.dcm', size: '12.4 MB', status: 'ready', series: 'Axial Portal Venous Phase' },
  { name: 'IMG_086_PORTAL_VEIN.dcm', size: '12.4 MB', status: 'ready', series: 'Axial Portal Venous Phase' },
  { name: 'IMG_087_PORTAL_VEIN.dcm', size: '12.4 MB', status: 'ready', series: 'Axial Portal Venous Phase' }
])
const isUploading = ref(false)
const uploadProgress = ref(100)

// Simulated Preprocessing States
const windowWidth = ref(400)
const windowLevel = ref(40)
const denoiseStrength = ref(75)

// Simulated AI Inference States
const isInferenceRunning = ref(false)
const inferenceProgress = ref(0)
const inferenceStage = ref('Ready to analyze')
const isAnalyzed = ref(false)

// Simulated Segmentation Mask Opacity
const maskOpacity = ref(50)

// Checklist approval states
const checklist = ref([
  { id: 0, text: 'Confirm automatic liver contour boundary accuracy', checked: false },
  { id: 1, text: 'Validate calculated volume (1,418.5 cc) matches body size', checked: false },
  { id: 2, text: 'Review lesion contour regions if present', checked: false },
  { id: 3, text: 'Generate DICOM Structured Report (SR) metadata', checked: false }
])

const isReportSigned = ref(false)

const triggerUpload = () => {
  isUploading.value = true
  uploadProgress.value = 0
  
  const interval = setInterval(() => {
    uploadProgress.value += 20
    if (uploadProgress.value >= 100) {
      clearInterval(interval)
      isUploading.value = false
    }
  }, 300)
}

const runAIInference = () => {
  isInferenceRunning.value = true
  inferenceProgress.value = 0
  isAnalyzed.value = false
  
  const stages = [
    { progress: 15, text: 'Parsing DICOM series header tags...' },
    { progress: 35, text: 'Applying isotropic resampling (1.0 x 1.0 x 1.5 mm)...' },
    { progress: 60, text: 'Evaluating Attention U-Net encoder feature maps...' },
    { progress: 85, text: 'Executing sigmoid thresholding & morphological cleaning...' },
    { progress: 100, text: 'AI segmentation pipeline complete.' }
  ]
  
  let currentStageIndex = 0
  
  const timer = setInterval(() => {
    inferenceProgress.value += 4
    
    // Update stage text based on progress thresholds
    if (currentStageIndex < stages.length && inferenceProgress.value >= stages[currentStageIndex].progress) {
      inferenceStage.value = stages[currentStageIndex].text
      currentStageIndex++
    }
    
    if (inferenceProgress.value >= 100) {
      clearInterval(timer)
      isInferenceRunning.value = false
      isAnalyzed.value = true
    }
  }, 100)
}

const resetWorkflow = () => {
  isAnalyzed.value = false
  inferenceProgress.value = 0
  inferenceStage.value = 'Ready to analyze'
  isReportSigned.value = false
  checklist.value.forEach(item => item.checked = false)
}

const steps = [
  { id: 0, title: 'Upload CT Scan', desc: 'DICOM Series ingestion & tag validation', icon: Upload },
  { id: 1, title: 'Preprocessing', desc: 'Contrast adjustment & noise filtering', icon: Sliders },
  { id: 2, title: 'Attention U-Net', desc: 'Automated deep learning segmentor', icon: Brain },
  { id: 3, title: 'Segmentation Output', desc: 'Contour generation & metrics', icon: ScanLine },
  { id: 4, title: 'Clinical Evaluation', desc: 'Quality audit & DICOM structured export', icon: Stethoscope }
]
</script>

<template>
  <section id="workflow" class="relative py-20 bg-gradient-to-b from-clinicalBg to-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <!-- Section Header -->
      <div 
        class="max-w-3xl mx-auto text-center mb-16 space-y-4"
        v-motion
        :initial="{ opacity: 0, y: 30 }"
        :enter="{ opacity: 1, y: 0, transition: { duration: 600, ease: 'easeOut' } }"
      >
        <span class="text-xs font-bold uppercase tracking-widest text-clinicalCyan bg-clinicalCyan/10 px-3 py-1 rounded-full">
          Radiologist Workspace
        </span>
        <h2 class="text-3xl sm:text-4xl font-extrabold tracking-tight text-clinicalNavy">
          Interactive Segmentation Console
        </h2>
        <div class="w-16 h-1 bg-gradient-to-r from-clinicalCyan to-clinicalEmerald mx-auto rounded-full"></div>
        <p class="text-base text-clinicalMuted leading-relaxed">
          Experience the live execution of our medical AI model. Follow the steps from raw DICOM upload to validated report generation.
        </p>
      </div>

      <!-- Main Workspace Frame -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        <!-- Left Sidebar: Steps -->
        <div class="lg:col-span-4 space-y-3">
          <div 
            v-for="(step, idx) in steps" 
            :key="step.id"
            @click="activeStep = step.id"
            :class="[
              'w-full text-left p-4.5 rounded-xl transition-all duration-300 flex items-center gap-4 border cursor-pointer select-none',
              activeStep === step.id 
                ? 'bg-white border-clinicalCyan shadow-clinical glow-cyan translate-x-1.5' 
                : 'bg-white/60 border-clinicalBorder/60 hover:bg-white hover:border-clinicalCyan/40 hover:shadow-soft'
            ]"
          >
            <!-- Step icon and counter -->
            <div 
              :class="[
                'w-10 h-10 rounded-lg flex items-center justify-center font-bold text-sm transition-all duration-300',
                activeStep === step.id 
                  ? 'bg-gradient-to-tr from-clinicalCyan to-clinicalEmerald text-white scale-105' 
                  : 'bg-clinicalCyan/10 text-clinicalCyan'
              ]"
            >
              <component :is="step.icon" class="w-5 h-5" />
            </div>

            <!-- Step metadata -->
            <div class="flex-1 min-w-0">
              <div class="flex items-center justify-between">
                <span class="text-[9px] uppercase tracking-wider font-extrabold text-clinicalMuted">Step 0{{ idx + 1 }}</span>
                <!-- Completed indicator checkmark -->
                <span 
                  v-if="step.id === 2 && isAnalyzed" 
                  class="w-4 h-4 rounded-full bg-clinicalEmerald text-white flex items-center justify-center"
                >
                  <Check class="w-2.5 h-2.5 stroke-[3]" />
                </span>
                <span 
                  v-if="step.id === 4 && isReportSigned" 
                  class="w-4 h-4 rounded-full bg-clinicalEmerald text-white flex items-center justify-center"
                >
                  <Check class="w-2.5 h-2.5 stroke-[3]" />
                </span>
              </div>
              <h3 class="text-sm font-bold text-clinicalNavy truncate mt-0.5">{{ step.title }}</h3>
              <p class="text-[11px] text-clinicalMuted truncate mt-0.5">{{ step.desc }}</p>
            </div>
            
            <ChevronRight 
              :class="[
                'w-4 h-4 transition-transform duration-300',
                activeStep === step.id ? 'translate-x-1 text-clinicalCyan' : 'text-clinicalMuted/45'
              ]" 
            />
          </div>
        </div>

        <!-- Right Content Panel: Dynamic Dashboard View -->
        <div class="lg:col-span-8 bg-white border border-clinicalBorder rounded-xl2 shadow-clinical p-6 md:p-8 min-h-[480px] flex flex-col justify-between relative overflow-hidden">
          <!-- Subtle layout pattern background -->
          <div class="absolute inset-0 bg-[radial-gradient(#e2f1fd_1px,transparent_1px)] bg-[size:20px_20px] opacity-40 pointer-events-none"></div>

          <!-- Dynamic Panel Wrapper -->
          <div class="relative z-10 flex-1 flex flex-col justify-between">
            
            <!-- STEP 01: UPLOAD CT SCAN -->
            <div v-if="activeStep === 0" class="space-y-6 flex-1 flex flex-col justify-between" v-motion :initial="{ opacity: 0, x: 20 }" :enter="{ opacity: 1, x: 0 }">
              <div>
                <h3 class="text-xl font-bold text-clinicalNavy flex items-center gap-2">
                  <Upload class="w-5.5 h-5.5 text-clinicalCyan" /> Ingest DICOM Series
                </h3>
                <p class="text-xs text-clinicalMuted mt-1">
                  Upload axial slice series of abdominal contrast-enhanced CT scans. Accepts standard .dcm files.
                </p>
              </div>

              <!-- Upload Interactive Area -->
              <div 
                @click="triggerUpload"
                class="border-2 border-dashed border-clinicalBorder hover:border-clinicalCyan/60 bg-clinicalBg/30 hover:bg-clinicalBg/70 rounded-xl p-8 text-center cursor-pointer transition-all duration-300 flex flex-col items-center justify-center group my-4"
              >
                <div class="p-4 bg-white rounded-full shadow-soft group-hover:scale-110 transition-transform duration-300 mb-4 border border-clinicalBorder">
                  <Database class="w-8 h-8 text-clinicalCyan" />
                </div>
                
                <span class="text-sm font-semibold text-clinicalNavy">Select patient scan folder or drag & drop</span>
                <span class="text-xs text-clinicalMuted mt-1">DICOM 3.0 directory files (.dcm)</span>

                <!-- Progress indicators -->
                <div v-if="isUploading" class="w-full max-w-xs mt-6 space-y-2">
                  <div class="flex items-center justify-between text-xs font-mono text-clinicalCyan">
                    <span>Uploading series...</span>
                    <span>{{ uploadProgress }}%</span>
                  </div>
                  <div class="w-full h-1.5 bg-clinicalBorder rounded-full overflow-hidden">
                    <div class="h-full bg-clinicalCyan transition-all duration-300" :style="{ width: `${uploadProgress}%` }"></div>
                  </div>
                </div>
              </div>

              <!-- File List -->
              <div class="space-y-2.5">
                <span class="text-[10px] uppercase tracking-wider font-extrabold text-clinicalMuted">DICOM metadata header checklist</span>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div 
                    v-for="file in uploadedFiles" 
                    :key="file.name"
                    class="bg-clinicalBg/50 border border-clinicalBorder/80 px-3.5 py-2.5 rounded-lg flex items-center justify-between text-xs"
                  >
                    <div class="min-w-0">
                      <div class="font-semibold text-clinicalNavy truncate">{{ file.name }}</div>
                      <div class="text-[10px] text-clinicalMuted truncate mt-0.5">{{ file.series }} ({{ file.size }})</div>
                    </div>
                    <span class="flex-shrink-0 w-5 h-5 rounded-full bg-clinicalEmerald/10 text-clinicalEmerald flex items-center justify-center">
                      <Check class="w-3.5 h-3.5 stroke-[3]" />
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- STEP 02: PREPROCESSING -->
            <div v-if="activeStep === 1" class="space-y-6 flex-1 flex flex-col justify-between" v-motion :initial="{ opacity: 0, x: 20 }" :enter="{ opacity: 1, x: 0 }">
              <div>
                <h3 class="text-xl font-bold text-clinicalNavy flex items-center gap-2">
                  <Sliders class="w-5.5 h-5.5 text-clinicalCyan" /> Radiographic Contrast Tuning
                </h3>
                <p class="text-xs text-clinicalMuted mt-1">
                  Adjust Hounsfield Unit (HU) windowing to isolate liver tissue contrasts before feeding slices to the deep learning model.
                </p>
              </div>

              <!-- Interactive Controls and Visual Pre-check -->
              <div class="grid grid-cols-1 md:grid-cols-12 gap-6 items-center my-4">
                <!-- Sliders -->
                <div class="md:col-span-6 space-y-5">
                  <div class="space-y-2">
                    <div class="flex justify-between text-xs">
                      <span class="font-semibold text-clinicalNavy">Window Width (W)</span>
                      <span class="font-mono font-bold text-clinicalCyan">{{ windowWidth }} HU</span>
                    </div>
                    <input 
                      type="range" 
                      min="200" 
                      max="600" 
                      v-model="windowWidth"
                      class="w-full h-1.5 bg-clinicalBorder rounded-lg appearance-none cursor-pointer accent-clinicalCyan" 
                    />
                    <div class="flex justify-between text-[9px] text-clinicalMuted">
                      <span>Soft tissue view (200)</span>
                      <span>Wide dynamic range (600)</span>
                    </div>
                  </div>

                  <div class="space-y-2">
                    <div class="flex justify-between text-xs">
                      <span class="font-semibold text-clinicalNavy">Window Level (L)</span>
                      <span class="font-mono font-bold text-clinicalCyan">{{ windowLevel }} HU</span>
                    </div>
                    <input 
                      type="range" 
                      min="0" 
                      max="100" 
                      v-model="windowLevel"
                      class="w-full h-1.5 bg-clinicalBorder rounded-lg appearance-none cursor-pointer accent-clinicalCyan" 
                    />
                    <div class="flex justify-between text-[9px] text-clinicalMuted">
                      <span>Low contrast level (0)</span>
                      <span>High contrast level (100)</span>
                    </div>
                  </div>

                  <div class="space-y-2">
                    <div class="flex justify-between text-xs">
                      <span class="font-semibold text-clinicalNavy">Gaussian Denoising</span>
                      <span class="font-mono font-bold text-clinicalCyan">{{ denoiseStrength }}%</span>
                    </div>
                    <input 
                      type="range" 
                      min="0" 
                      max="100" 
                      v-model="denoiseStrength"
                      class="w-full h-1.5 bg-clinicalBorder rounded-lg appearance-none cursor-pointer accent-clinicalCyan" 
                    />
                  </div>
                </div>

                <!-- Contrast Live Preview simulation -->
                <div class="md:col-span-6 flex flex-col items-center">
                  <div class="relative w-48 h-48 rounded-xl bg-black overflow-hidden border border-clinicalBorder shadow-inner flex items-center justify-center">
                    <svg viewBox="0 0 100 100" class="w-full h-full p-2">
                      <!-- Simulated CT scan image responding to sliders -->
                      <!-- We represent Hounsfield changes by varying opacity/fill colors dynamically! -->
                      <circle cx="50" cy="50" r="45" fill="#18181b" />
                      
                      <!-- Liver cross section responsive to window width and level -->
                      <path 
                        d="M25,50 Q23,30 45,25 Q70,20 72,35 Q75,50 67,62 Q55,72 42,68 Q33,64 25,50 Z" 
                        :fill="`rgb(${Math.max(45, windowLevel * 1.5)}, ${Math.max(45, windowLevel * 1.5)}, ${Math.max(45, windowLevel * 1.5)})`" 
                        :opacity="`${0.3 + (windowWidth / 600) * 0.5}`"
                        stroke="#4b5563" 
                        stroke-width="0.8" 
                      />
                      <!-- Denoising effect simulation: blur filter changes on denoise strength slider -->
                      <filter id="gaussBlur">
                        <feGaussianBlur :stdDeviation="`${(100 - denoiseStrength) / 25}`" />
                      </filter>
                      <!-- Core structures -->
                      <circle cx="50" cy="72" r="4" fill="#3f3f46" />
                    </svg>

                    <!-- Indicators -->
                    <div class="absolute bottom-2 left-2 right-2 flex justify-between text-[8px] font-mono text-white/70">
                      <span>W: {{ windowWidth }}</span>
                      <span>L: {{ windowLevel }}</span>
                    </div>
                    <div class="absolute inset-0 border border-dashed border-white/10 pointer-events-none"></div>
                  </div>
                  <span class="text-[10px] text-clinicalMuted font-mono mt-2">Active Hounsfield Filter Frame</span>
                </div>
              </div>
            </div>

            <!-- STEP 03: ATTENTION U-NET ANALYSIS -->
            <div v-if="activeStep === 2" class="space-y-6 flex-1 flex flex-col justify-between" v-motion :initial="{ opacity: 0, x: 20 }" :enter="{ opacity: 1, x: 0 }">
              <div>
                <h3 class="text-xl font-bold text-clinicalNavy flex items-center gap-2">
                  <Brain class="w-5.5 h-5.5 text-clinicalCyan" /> Attention U-Net Convolution Core
                </h3>
                <p class="text-xs text-clinicalMuted mt-1">
                  Kickstart the automated segmentation pipeline. The model runs feature attention gates to filter background noise and map organ contours.
                </p>
              </div>

              <!-- AI Inference Simulator Panel -->
              <div class="bg-slate-950 text-slate-100 rounded-xl p-5 font-mono text-xs my-4 border border-slate-800 relative glow-cyan">
                <!-- Flashing scanner grid -->
                <div class="absolute inset-0 bg-[linear-gradient(to_bottom,transparent_95%,rgba(6,182,212,0.05)_95%)] bg-[size:100%_15px] pointer-events-none animate-pulse"></div>

                <div class="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
                  <div class="flex items-center gap-2">
                    <Brain class="w-4.5 h-4.5 text-clinicalCyan" />
                    <span class="font-bold text-white">DEEP_LEARNING_ENGINE v2.5</span>
                  </div>
                  <span class="text-[10px] bg-slate-800 px-2 py-0.5 rounded text-slate-400">FP32 Mode</span>
                </div>

                <!-- Simulation progress text -->
                <div class="space-y-2 min-h-[96px]">
                  <div class="flex items-center gap-2">
                    <span class="text-slate-500">>>></span>
                    <span :class="inferenceProgress > 0 ? 'text-clinicalCyan font-bold' : 'text-slate-400'">
                      {{ inferenceStage }}
                    </span>
                  </div>
                  <div v-if="isInferenceRunning" class="text-slate-500 text-[10px] space-y-1">
                    <div>[INFO] Loading network weights from path: /weights/attention_unet_liver.bin...</div>
                    <div class="animate-pulse">[COMPUTE] Executing deep layer convolution mapping...</div>
                  </div>
                  <div v-if="isAnalyzed" class="text-clinicalEmerald text-[11px] font-bold flex items-center gap-1.5 mt-2">
                    <Check class="w-4 h-4" />
                    <span>Inference successful. Volumetric mask generated! Dice = 0.9631.</span>
                  </div>
                </div>

                <!-- Progress bar -->
                <div class="mt-4 pt-3 border-t border-slate-800">
                  <div class="flex justify-between text-[10px] text-slate-400 mb-1.5">
                    <span>PROCESSING PIPELINE</span>
                    <span>{{ inferenceProgress }}%</span>
                  </div>
                  <div class="w-full h-2 bg-slate-900 rounded-full overflow-hidden border border-slate-800">
                    <div 
                      class="h-full bg-gradient-to-r from-clinicalCyan to-clinicalEmerald transition-all duration-100" 
                      :style="{ width: `${inferenceProgress}%` }"
                    ></div>
                  </div>
                </div>
              </div>

              <!-- Button Controls -->
              <div class="flex items-center gap-3">
                <button 
                  @click="runAIInference"
                  :disabled="isInferenceRunning"
                  class="flex items-center gap-2 px-6 py-3 text-xs uppercase tracking-wider font-bold text-white bg-gradient-to-r from-clinicalCyan to-clinicalEmerald rounded-lg hover:shadow shadow-sm active:scale-95 transition-all disabled:opacity-50 disabled:pointer-events-none"
                >
                  <component :is="isInferenceRunning ? Loader2 : Play" :class="['w-4 h-4', isInferenceRunning ? 'animate-spin' : '']" />
                  {{ isInferenceRunning ? 'Running Inference...' : 'Run AI Inference' }}
                </button>
                
                <button 
                  v-if="isAnalyzed"
                  @click="resetWorkflow"
                  class="flex items-center gap-1.5 px-4.5 py-3 text-xs uppercase tracking-wider font-semibold text-clinicalNavy/80 bg-clinicalBg border border-clinicalBorder rounded-lg hover:bg-clinicalBorder/40 transition-colors"
                >
                  <RefreshCw class="w-3.5 h-3.5" />
                  Reset
                </button>
              </div>
            </div>

            <!-- STEP 04: SEGMENTATION OUTPUT -->
            <div v-if="activeStep === 3" class="space-y-6 flex-1 flex flex-col justify-between" v-motion :initial="{ opacity: 0, x: 20 }" :enter="{ opacity: 1, x: 0 }">
              <div>
                <h3 class="text-xl font-bold text-clinicalNavy flex items-center gap-2">
                  <ScanLine class="w-5.5 h-5.5 text-clinicalCyan" /> Segmentation Overlay & Metrics
                </h3>
                <p class="text-xs text-clinicalMuted mt-1">
                  Review the generated contour boundary masks overlays and clinical metric estimates below.
                </p>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-12 gap-6 items-center my-4">
                <!-- CT Overlay Display -->
                <div class="md:col-span-6 flex flex-col items-center">
                  <div class="relative w-48 h-48 rounded-xl bg-black overflow-hidden border border-clinicalBorder shadow-md">
                    <!-- Base CT slice background image -->
                    <svg viewBox="0 0 100 100" class="w-full h-full p-2">
                      <circle cx="50" cy="50" r="45" fill="#18181b" />
                      <!-- Liver base organ shape -->
                      <path d="M25,50 Q23,30 45,25 Q70,20 72,35 Q75,50 67,62 Q55,72 42,68 Q33,64 25,50 Z" fill="#3f3f46" stroke="#52525b" stroke-width="0.5" />
                      
                      <!-- Overlay mask responsive to opacity slider -->
                      <path 
                        d="M25,50 Q23,30 45,25 Q70,20 72,35 Q75,50 67,62 Q55,72 42,68 Q33,64 25,50 Z" 
                        fill="#10b981" 
                        :opacity="maskOpacity / 100" 
                        stroke="#10b981" 
                        stroke-width="1.2" 
                      />
                    </svg>

                    <!-- Opacity indicator -->
                    <div class="absolute bottom-2 left-2 text-[9px] font-mono text-white/80 bg-black/60 px-1.5 py-0.5 rounded">
                      Mask Opacity: {{ maskOpacity }}%
                    </div>
                  </div>

                  <!-- Slider to control opacity -->
                  <div class="w-full max-w-xs mt-3.5 space-y-1 px-4">
                    <input 
                      type="range" 
                      min="0" 
                      max="100" 
                      v-model="maskOpacity"
                      class="w-full h-1 bg-clinicalBorder rounded-lg appearance-none cursor-pointer accent-clinicalCyan"
                    />
                    <div class="flex justify-between text-[9px] text-clinicalMuted font-mono">
                      <span>0% (Scan Only)</span>
                      <span>100% (Mask Only)</span>
                    </div>
                  </div>
                </div>

                <!-- Quantitative metrics card list -->
                <div class="md:col-span-6 space-y-3">
                  <div class="bg-clinicalBg/55 border border-clinicalBorder p-3 rounded-lg flex items-center justify-between">
                    <span class="text-xs font-semibold text-clinicalNavy">Dice Coefficient</span>
                    <span class="text-xs font-bold text-clinicalCyan font-mono">0.9631 (96.3%)</span>
                  </div>
                  <div class="bg-clinicalBg/55 border border-clinicalBorder p-3 rounded-lg flex items-center justify-between">
                    <span class="text-xs font-semibold text-clinicalNavy">Hausdorff Distance</span>
                    <span class="text-xs font-bold text-clinicalCyan font-mono">4.82 mm</span>
                  </div>
                  <div class="bg-clinicalBg/55 border border-clinicalBorder p-3 rounded-lg flex items-center justify-between">
                    <span class="text-xs font-semibold text-clinicalNavy">Computed Liver Volume</span>
                    <span class="text-xs font-bold text-clinicalEmerald font-mono">1,418.5 cc</span>
                  </div>
                  <div class="bg-clinicalBg/55 border border-clinicalBorder p-3 rounded-lg flex items-center justify-between">
                    <span class="text-xs font-semibold text-clinicalNavy">Estimated Process Time</span>
                    <span class="text-xs font-bold text-clinicalMuted font-mono">3.12s</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- STEP 05: CLINICAL EVALUATION -->
            <div v-if="activeStep === 4" class="space-y-6 flex-1 flex flex-col justify-between" v-motion :initial="{ opacity: 0, x: 20 }" :enter="{ opacity: 1, x: 0 }">
              <div>
                <h3 class="text-xl font-bold text-clinicalNavy flex items-center gap-2">
                  <Stethoscope class="w-5.5 h-5.5 text-clinicalCyan" /> Radiologist Quality Audit
                </h3>
                <p class="text-xs text-clinicalMuted mt-1">
                  Perform visual verification and check off tasks to sign and compile DICOM structures for PACS export.
                </p>
              </div>

              <!-- Interactive checklist -->
              <div class="space-y-3 my-4">
                <label 
                  v-for="item in checklist" 
                  :key="item.id"
                  class="flex items-center gap-3.5 p-3.5 bg-clinicalBg/45 hover:bg-clinicalBg/75 border border-clinicalBorder rounded-xl cursor-pointer select-none transition-colors duration-200"
                >
                  <input 
                    type="checkbox" 
                    v-model="item.checked"
                    class="w-4.5 h-4.5 rounded border-clinicalBorder text-clinicalCyan focus:ring-clinicalCyan/30 cursor-pointer"
                  />
                  <span :class="['text-xs font-medium transition-all duration-300', item.checked ? 'text-clinicalNavy line-through opacity-65' : 'text-clinicalNavy/90']">
                    {{ item.text }}
                  </span>
                </label>
              </div>

              <!-- Report Sign Action -->
              <div class="flex items-center gap-4">
                <button 
                  @click="isReportSigned = true"
                  :disabled="checklist.some(i => !i.checked) || isReportSigned"
                  class="flex items-center gap-2 px-6 py-3.5 text-xs uppercase tracking-wider font-bold text-white bg-gradient-to-r from-clinicalCyan to-clinicalEmerald rounded-lg hover:shadow shadow-sm active:scale-95 transition-all disabled:opacity-40 disabled:pointer-events-none"
                >
                  <FileText class="w-4 h-4" />
                  {{ isReportSigned ? 'Report Signed & Archived' : 'Sign & Export to PACS' }}
                </button>

                <div v-if="isReportSigned" class="text-clinicalEmerald text-xs font-bold flex items-center gap-1.5 animate-bounce">
                  <Check class="w-4.5 h-4.5 stroke-[3]" /> PACS Export Complete
                </div>
              </div>
            </div>

          </div>

          <!-- Bottom Panel Context Bar -->
          <div class="mt-8 pt-4 border-t border-clinicalBorder/60 flex flex-wrap items-center justify-between gap-3 text-[10px] font-mono text-clinicalMuted z-10">
            <span class="flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-full bg-clinicalCyan"></span>
              Workspace Active Session
            </span>
            <div class="flex items-center gap-4">
              <span>Patient ID: PT_2938_AB</span>
              <span>Slice Count: 144</span>
              <span>PACS Node: CLINICAL_ROUTER_1</span>
            </div>
          </div>
        </div>

      </div>
      
    </div>
  </section>
</template>
