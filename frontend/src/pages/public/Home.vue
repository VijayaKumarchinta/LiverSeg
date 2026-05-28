<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { 
  Activity, 
  ShieldCheck, 
  ArrowRight, 
  UploadCloud, 
  BrainCircuit, 
  ActivitySquare, 
  CheckCircle,
  FileSpreadsheet,
  Layers,
  LineChart,
  ShieldAlert
} from 'lucide-vue-next'

const coreStats = [
  { name: 'Segmentation Accuracy', value: '95.8% Dice', desc: 'Validated on LiTS datasets' },
  { name: 'Processing Latency', value: '< 3.5 Seconds', desc: 'Per volume axial inference' },
  { name: 'Model Backbone', value: 'Attention 3D U-Net', desc: 'Active spatial weighting gates' }
]

// Demo slice data for interactive simulation
const demoSlices = [
  {
    id: 1,
    liverPath: "M22,50 Q20,38 35,32 Q55,27 58,38 Q61,50 54,58 Q45,66 35,64 Q27,62 22,50 Z",
    lesionSize: 0, lesionX: 0, lesionY: 0,
    dice: "0.942", volume: "1024 cc"
  },
  {
    id: 2,
    liverPath: "M19,50 Q16,35 35,29 Q58,24 61,36 Q64,50 56,60 Q45,69 33,66 Q24,63 19,50 Z",
    lesionSize: 3, lesionX: 36, lesionY: 44,
    dice: "0.956", volume: "1280 cc"
  },
  {
    id: 3,
    liverPath: "M16,50 Q13,32 35,26 Q60,21 63,35 Q66,50 58,62 Q45,72 32,68 Q23,64 16,50 Z",
    lesionSize: 4.5, lesionX: 34, lesionY: 42,
    dice: "0.958", volume: "1418 cc"
  },
  {
    id: 4,
    liverPath: "M18,50 Q15,34 35,28 Q59,23 62,35 Q65,50 57,61 Q45,70 32.5,67 Q23.5,63.5 18,50 Z",
    lesionSize: 5.5, lesionX: 32, lesionY: 40,
    dice: "0.961", volume: "1350 cc"
  },
  {
    id: 5,
    liverPath: "M24,50 Q22,40 35,35 Q52,30 55,40 Q58,50 52,56 Q45,62 36,61 Q29,60 24,50 Z",
    lesionSize: 0, lesionX: 0, lesionY: 0,
    dice: "0.938", volume: "910 cc"
  }
]

const activeSliceIdx = ref(2)
let sliceInterval = null

onMounted(() => {
  sliceInterval = setInterval(() => {
    activeSliceIdx.value = (activeSliceIdx.value + 1) % demoSlices.length
  }, 1800)
})

onUnmounted(() => {
  if (sliceInterval) clearInterval(sliceInterval)
})

const workflowSteps = [
  {
    step: '01',
    title: 'Upload Scans',
    desc: 'Ingest NIfTI or DICOM slices directly via secure browser drag-and-drop or local PACS sync.',
    icon: UploadCloud,
    accent: 'from-teal-400 to-teal-500'
  },
  {
    step: '02',
    title: 'AI Processing',
    desc: 'Intensity windowing (Hounsfield) and spatial resampling normalize inputs for inference.',
    icon: BrainCircuit,
    accent: 'from-teal-500 to-teal-600'
  },
  {
    step: '03',
    title: 'Segment Parenchyma',
    desc: 'UNet3D deep network generates semantic segmentation masks isolating liver borders.',
    icon: Layers,
    accent: 'from-teal-600 to-sky-500'
  },
  {
    step: '04',
    title: 'Compare Predictions',
    desc: 'Draggable comparison slider overlays ground truth labels to highlight accuracy thresholds.',
    icon: LineChart,
    accent: 'from-sky-500 to-sky-600'
  },
  {
    step: '05',
    title: 'Generate Report',
    desc: 'Dynamic volumetrics summarize findings and enable one-click PACS router exporting.',
    icon: FileSpreadsheet,
    accent: 'from-sky-600 to-indigo-600'
  }
]
</script>

<template>
  <div class="relative min-h-screen pt-28 pb-20 clinical-workspace overflow-hidden">
    <!-- Immersive clinical glow backdrops -->
    <div class="absolute top-[5%] right-[10%] w-[500px] h-[500px] bg-teal-500/5 rounded-full blur-[120px] pointer-events-none"></div>
    <div class="absolute bottom-[10%] left-[5%] w-[450px] h-[450px] bg-sky-500/5 rounded-full blur-[120px] pointer-events-none"></div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
      
      <!-- HERO AREA -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-16 items-center">
        <div class="lg:col-span-7 space-y-8">
          <!-- Animated Tag Badge -->
          <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/70 border border-teal-200/55 shadow-sm text-teal-700 text-xs font-bold uppercase tracking-wider backdrop-blur-sm">
            <span class="w-1.5 h-1.5 rounded-full bg-teal-500 animate-pulse"></span>
            Automated Clinical Volumetrics
          </div>

          <!-- Title -->
          <h1 class="text-4xl sm:text-5xl lg:text-6xl font-black tracking-tight text-slate-900 leading-[1.08]">
            AI-Powered <br />
            <span class="bg-gradient-to-r from-teal-600 via-teal-500 to-sky-600 bg-clip-text text-transparent">
              Liver Segmentation
            </span>
          </h1>

          <p class="text-base sm:text-lg text-slate-500 max-w-xl leading-relaxed font-medium">
            Deploy deep learning spatial gates to identify liver parenchymal anomalies and lesions from abdominal contrast CT volumes. Tailored for enterprise PACS networks.
          </p>

          <!-- Buttons -->
          <div class="flex flex-wrap items-center gap-4">
            <router-link 
              to="/app" 
              class="flex items-center gap-2 px-7 py-4 text-xs font-bold uppercase tracking-wider rounded-xl clinical-btn-primary active-shrink"
            >
              Launch Workstation
              <ArrowRight class="w-4 h-4" />
            </router-link>
            
            <router-link 
              to="/platform" 
              class="flex items-center gap-2 px-7 py-4 text-xs font-bold uppercase tracking-wider rounded-xl clinical-btn-secondary active-shrink"
            >
              Explore Platform
            </router-link>
          </div>

          <!-- Quick Statistics in Frosted Panel -->
          <div class="p-6 rounded-2xl frosted-glass-panel max-w-2xl">
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
              <div v-for="(stat, idx) in coreStats" :key="idx" class="space-y-1">
                <div class="text-2xl font-black text-slate-900 bg-gradient-to-r from-teal-700 to-sky-700 bg-clip-text text-transparent">
                  {{ stat.value }}
                </div>
                <div class="text-xs font-bold text-slate-700 tracking-tight">{{ stat.name }}</div>
                <div class="text-[10px] text-slate-400 font-semibold leading-snug">{{ stat.desc }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- HERO GRAPHIC (Interactive Clinical Mockup representation with Floating Cards) -->
        <div class="lg:col-span-5 relative flex justify-center py-6">
          <!-- Gantry Scanner Ring Accent (behind container) -->
          <div class="absolute -inset-4 rounded-full border border-dashed border-teal-500/10 animate-spin [animation-duration:120s] pointer-events-none"></div>
          <div class="absolute -inset-8 rounded-full border border-slate-200/40 pointer-events-none"></div>

          <!-- Main Frosted PACS Console Card -->
          <div class="relative w-full max-w-[440px] aspect-[4/3] rounded-2xl p-4 flex flex-col justify-between frosted-glass-panel hover:scale-[1.02] duration-500 group">
            
            <!-- Top bar -->
            <div class="flex items-center justify-between pb-2.5 border-b border-slate-200/50 text-[10px] font-mono text-slate-500 font-bold">
              <span class="flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-teal-500 animate-pulse"></span>
                CT_AXIAL_PARENCHYMA
              </span>
              <span>Slice {{ demoSlices[activeSliceIdx].id }} / 5</span>
            </div>

            <!-- Slice display (SVG mockup of liver) -->
            <div class="flex-1 flex items-center justify-center my-3 bg-black/95 rounded-xl border border-slate-800 relative overflow-hidden shadow-inner min-h-[180px]">
              <!-- Scan Crosshairs -->
              <div class="absolute inset-0 bg-[radial-gradient(rgba(255,255,255,0.015)_1px,transparent_1px)] bg-[size:14px_14px] pointer-events-none"></div>
              
              <svg viewBox="0 0 100 100" class="w-48 h-48 opacity-90 select-none">
                <!-- Abdominal boundary -->
                <circle cx="50" cy="50" r="42" fill="none" stroke="#27272a" stroke-width="0.8" />
                <path 
                  d="M16,50 Q13,32 35,26 Q60,21 63,35 Q66,50 58,62 Q45,72 32,68 Q23,64 16,50 Z" 
                  fill="#0c0c0e" 
                  stroke="#27272a" 
                  stroke-width="0.6" 
                />
                
                <!-- Liver parenchyma -->
                <path 
                  :d="demoSlices[activeSliceIdx].liverPath" 
                  fill="#1c1c22" 
                  stroke="#3f3f46" 
                  stroke-width="0.7" 
                />

                <!-- Segmentation contour -->
                <path 
                  :d="demoSlices[activeSliceIdx].liverPath" 
                  fill="rgba(20, 184, 166, 0.25)" 
                  stroke="#14b8a6" 
                  stroke-width="1.0" 
                  class="transition-all duration-300"
                />

                <!-- Lesion -->
                <circle 
                  v-if="demoSlices[activeSliceIdx].lesionSize > 0"
                  :cx="demoSlices[activeSliceIdx].lesionX" 
                  :cy="demoSlices[activeSliceIdx].lesionY" 
                  :r="demoSlices[activeSliceIdx].lesionSize" 
                  fill="rgba(239, 68, 68, 0.45)" 
                  stroke="#ef4444" 
                  stroke-width="0.5" 
                />
              </svg>
              
              <!-- Scan line effect -->
              <div class="absolute left-0 right-0 h-0.5 bg-teal-400/80 animate-scan"></div>
            </div>

            <!-- Mini metrics panel -->
            <div class="grid grid-cols-2 gap-2 text-[9px] font-mono text-slate-500 font-bold">
              <div class="bg-white/60 p-2 rounded-lg border border-slate-200/50 flex justify-between items-center">
                <span>DICE SCORE:</span>
                <span class="text-teal-600 font-extrabold">{{ demoSlices[activeSliceIdx].dice }}</span>
              </div>
              <div class="bg-white/60 p-2 rounded-lg border border-slate-200/50 flex justify-between items-center">
                <span>VOLUME:</span>
                <span class="text-slate-800 font-extrabold">{{ demoSlices[activeSliceIdx].volume }}</span>
              </div>
            </div>

            <!-- Floating Overlay Card 1: Accuracy Indicator (overlaps left) -->
            <div class="absolute -left-10 top-1/4 bg-white/90 border border-slate-200/60 rounded-xl p-3 shadow-md backdrop-blur-sm pointer-events-none transform -rotate-3 transition-transform group-hover:rotate-0 duration-300 hidden sm:block">
              <div class="flex items-center gap-2">
                <div class="w-6 h-6 rounded-lg bg-teal-50 text-teal-600 flex items-center justify-center">
                  <CheckCircle class="w-4 h-4" />
                </div>
                <div class="leading-none">
                  <div class="text-[9px] font-bold text-slate-400 uppercase">CNN Core</div>
                  <div class="text-xs font-black text-slate-800">UNet 3D Model</div>
                </div>
              </div>
            </div>

            <!-- Floating Overlay Card 2: Regulatory Badge (overlaps bottom-right) -->
            <div class="absolute -right-8 bottom-8 bg-white/95 border border-slate-200/60 rounded-xl p-3 shadow-md backdrop-blur-sm pointer-events-none transform rotate-3 transition-transform group-hover:rotate-0 duration-300 hidden sm:block">
              <div class="flex items-center gap-2.5">
                <div class="w-6 h-6 rounded-lg bg-sky-50 text-sky-600 flex items-center justify-center">
                  <ShieldCheck class="w-4 h-4" />
                </div>
                <div class="leading-none">
                  <div class="text-[9px] font-bold text-slate-400 uppercase">Security</div>
                  <div class="text-xs font-black text-slate-800">HIPAA Compliant</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 5-STEP CLINICAL WORKFLOW SECTION -->
      <div class="mt-32 py-16 border-t border-slate-200/60">
        <div class="text-center max-w-3xl mx-auto mb-20 space-y-4">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-teal-50 border border-teal-100 text-teal-700 text-[10px] font-bold uppercase tracking-wider">
            Diagnostic Workflow
          </div>
          <h2 class="text-3xl sm:text-4xl font-black tracking-tight text-slate-900">
            Connected 5-Step Volumetric Flow
          </h2>
          <p class="text-sm text-slate-500 max-w-xl mx-auto leading-relaxed font-semibold">
            Follow the seamless path from patient raw scan imports to verified PACS diagnostic reporting.
          </p>
        </div>

        <!-- Workflow steps list with line connector -->
        <div class="relative">
          <!-- Horizontal connector line for large screens -->
          <div class="hidden lg:block absolute top-[44px] left-[5%] right-[5%] h-0.5 bg-gradient-to-r from-teal-400/30 via-sky-400/30 to-indigo-400/20 pointer-events-none"></div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8">
            <div 
              v-for="(step, idx) in workflowSteps" 
              :key="idx" 
              class="relative p-6 rounded-2xl frosted-glass-panel hover:border-teal-500/30 hover:shadow-lg transition-all duration-300 group flex flex-col justify-between"
            >
              <div class="space-y-4">
                <!-- Step Badge and Icon -->
                <div class="flex items-center justify-between">
                  <div class="w-12 h-12 rounded-xl bg-gradient-to-br text-white flex items-center justify-center shadow-sm duration-300" :class="step.accent">
                    <component :is="step.icon" class="w-5 h-5" />
                  </div>
                  <span class="text-2xl font-black text-slate-200 group-hover:text-teal-200/60 transition-colors duration-300">
                    {{ step.step }}
                  </span>
                </div>

                <h3 class="font-bold text-slate-900 text-base leading-snug tracking-tight">{{ step.title }}</h3>
                <p class="text-xs text-slate-500 leading-relaxed font-semibold">{{ step.desc }}</p>
              </div>
              
              <!-- Subtle card footer indicator -->
              <div class="mt-6 pt-3 border-t border-slate-100/60 flex items-center justify-between text-[8px] font-bold text-slate-400 uppercase tracking-widest">
                <span>Phase Status</span>
                <span class="text-teal-600 font-extrabold flex items-center gap-1">
                  <span class="w-1 h-1 rounded-full bg-teal-500"></span> Verified
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
