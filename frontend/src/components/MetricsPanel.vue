<script setup>
import { computed } from 'vue'
import { 
  Activity, Sliders, ShieldCheck, AlertTriangle, 
  Settings, Cpu, ChevronRight, CheckCircle2 
} from 'lucide-vue-next'

const props = defineProps({
  patient: {
    type: Object,
    default: null
  },
  ww: {
    type: Number,
    required: true
  },
  wl: {
    type: Number,
    required: true
  },
  opacity: {
    type: Number,
    required: true
  },
  showGroundTruth: {
    type: Boolean,
    required: true
  },
  showLesions: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits([
  'update:ww',
  'update:wl',
  'update:opacity',
  'update:showGroundTruth',
  'update:showLesions',
  'proceed'
])

// Mock or calculated diagnostics based on patient
const diceScore = computed(() => props.patient?.metrics?.dice || '95.8%')
const volumeEstimate = computed(() => props.patient?.metrics?.volume || '1418 cc')
const iouScore = computed(() => {
  // Derive IoU from Dice if not explicitly provided
  if (props.patient?.metrics?.dice) {
    const diceNum = parseFloat(props.patient.metrics.dice)
    if (!isNaN(diceNum)) {
      return ((diceNum / 100) * 0.96 * 100).toFixed(1) + '%'
    }
  }
  return '91.8%'
})

const hasLesions = computed(() => {
  if (props.patient === null) return false
  return props.patient.hasLesions || false
})

const lesionText = computed(() => {
  if (hasLesions.value) {
    return '2 Focal Lesions Detected'
  }
  return 'No Focal Lesions Detected'
})

const processingDuration = computed(() => {
  // If the patient status is completed, show a simulated or actual duration
  return '4.8s'
})

const modelVersion = computed(() => 'MONAI 3D U-Net v1.4')
</script>

<template>
  <div class="space-y-4">
    <!-- AI Diagnostics Panel -->
    <div class="frosted-glass-panel p-5 space-y-4 border border-slate-200/80 dark:border-slate-800 bg-white/60">
      <div class="flex items-center justify-between pb-2.5 border-b border-slate-100 dark:border-slate-800">
        <h3 class="text-xs font-black text-slate-800 uppercase tracking-widest flex items-center gap-1.5">
          <Activity class="w-3.5 h-3.5 text-teal-600" /> AI Diagnostics Summary
        </h3>
        <span class="text-[8px] font-bold text-teal-650 bg-teal-50 px-2 py-0.5 rounded border border-teal-100 font-mono">
          {{ modelVersion }}
        </span>
      </div>

      <!-- Main Diagnostics Cards -->
      <div class="grid grid-cols-2 gap-3">
        <!-- Detection Status -->
        <div class="p-3 bg-slate-50 dark:bg-slate-900 border border-slate-150 dark:border-slate-800 rounded-xl">
          <div class="text-[9px] font-bold text-slate-400 uppercase tracking-wider">Liver Status</div>
          <div class="text-xs font-black text-slate-800 mt-1 flex items-center gap-1">
            <CheckCircle2 class="w-3.5 h-3.5 text-teal-500" />
            <span>Detected</span>
          </div>
        </div>
        
        <!-- Confidence -->
        <div class="p-3 bg-slate-50 dark:bg-slate-900 border border-slate-150 dark:border-slate-800 rounded-xl">
          <div class="text-[9px] font-bold text-slate-400 uppercase tracking-wider">Confidence</div>
          <div class="text-xs font-black text-slate-800 mt-1">98.4%</div>
        </div>
      </div>

      <!-- Segmentation Overlay & Metrics scores -->
      <div class="grid grid-cols-3 gap-2 text-center">
        <div class="py-2.5 bg-teal-50/30 border border-teal-100/50 rounded-xl">
          <div class="text-sm font-black text-teal-700">{{ diceScore }}</div>
          <div class="text-[8px] text-slate-400 font-bold uppercase">Dice Score</div>
        </div>
        <div class="py-2.5 bg-slate-50 dark:bg-slate-900 border border-slate-150 dark:border-slate-800 rounded-xl">
          <div class="text-sm font-black text-slate-800">{{ iouScore }}</div>
          <div class="text-[8px] text-slate-400 font-bold uppercase">Mean IoU</div>
        </div>
        <div class="py-2.5 bg-slate-50 dark:bg-slate-900 border border-slate-150 dark:border-slate-800 rounded-xl">
          <div class="text-sm font-black text-slate-800">{{ volumeEstimate }}</div>
          <div class="text-[8px] text-slate-400 font-bold uppercase">Volume</div>
        </div>
      </div>

      <!-- Alerts / Lesions badge -->
      <div 
        class="flex items-center gap-2 p-2.5 rounded-xl border font-semibold text-[10px]"
        :class="hasLesions 
          ? 'bg-rose-50 border-rose-100 text-rose-800' 
          : 'bg-teal-50 border-teal-100 text-teal-800'"
      >
        <component :is="hasLesions ? AlertTriangle : ShieldCheck" class="w-4 h-4 flex-shrink-0" />
        <span class="flex-1">{{ lesionText }}</span>
        <span class="text-[8px] font-mono px-1.5 py-0.5 rounded bg-white/80 border" :class="hasLesions ? 'border-rose-200' : 'border-teal-200'">
          {{ hasLesions ? 'Lesion: 0.35' : 'Clear' }}
        </span>
      </div>

      <!-- Telemetry Info -->
      <div class="flex justify-between items-center text-[9px] font-mono text-slate-400 border-t border-slate-100 dark:border-slate-800 pt-2.5">
        <span class="flex items-center gap-1"><Cpu class="w-3 h-3 text-slate-400" /> GPU Inference</span>
        <span>Duration: {{ processingDuration }}</span>
      </div>
    </div>

    <!-- Contrast Calibration Panel -->
    <div class="frosted-glass-panel p-5 space-y-4 border border-slate-200/80 dark:border-slate-800 bg-white/60">
      <div class="section-title flex items-center gap-1.5 border-b border-slate-100 dark:border-slate-800 pb-2.5">
        <Sliders class="w-3.5 h-3.5 text-teal-600" /> Contrast Calibration
      </div>
      
      <div class="space-y-3">
        <!-- Window Width -->
        <div class="space-y-1">
          <div class="flex justify-between items-center text-[9px] text-slate-500 font-bold">
            <span>Window Width (WW)</span>
            <span class="font-mono text-slate-800">{{ ww }} HU</span>
          </div>
          <input 
            :value="ww"
            @input="emit('update:ww', parseInt($event.target.value, 10))"
            type="range" 
            min="100" 
            max="800" 
            step="10" 
            class="w-full accent-teal-600 cursor-pointer bg-slate-100 dark:bg-slate-800 h-1 rounded-full appearance-none outline-none"
          />
        </div>

        <!-- Window Level -->
        <div class="space-y-1">
          <div class="flex justify-between items-center text-[9px] text-slate-500 font-bold">
            <span>Window Level (WL)</span>
            <span class="font-mono text-slate-800">{{ wl }} HU</span>
          </div>
          <input 
            :value="wl"
            @input="emit('update:wl', parseInt($event.target.value, 10))"
            type="range" 
            min="-100" 
            max="200" 
            step="5" 
            class="w-full accent-teal-600 cursor-pointer bg-slate-100 dark:bg-slate-800 h-1 rounded-full appearance-none outline-none"
          />
        </div>

        <!-- Mask Opacity -->
        <div class="space-y-1">
          <div class="flex justify-between items-center text-[9px] text-slate-500 font-bold">
            <span>Mask Opacity</span>
            <span class="font-mono text-slate-800">{{ opacity }}%</span>
          </div>
          <input 
            :value="opacity"
            @input="emit('update:opacity', parseInt($event.target.value, 10))"
            type="range" 
            min="0" 
            max="100" 
            step="5" 
            class="w-full accent-teal-600 cursor-pointer bg-slate-100 dark:bg-slate-800 h-1 rounded-full appearance-none outline-none"
          />
        </div>
      </div>

      <!-- Visibility Options -->
      <div class="space-y-2 pt-3 border-t border-slate-100 dark:border-slate-800">
        <label class="flex items-center gap-2 text-xs font-semibold text-slate-700 dark:text-slate-350 cursor-pointer select-none">
          <input 
            :checked="showGroundTruth"
            @change="emit('update:showGroundTruth', $event.target.checked)"
            type="checkbox" 
            class="rounded text-teal-600 focus:ring-teal-500 border-slate-300" 
          />
          <span>Show Ground Truth contour</span>
        </label>
        
        <label class="flex items-center gap-2 text-xs font-semibold text-slate-700 dark:text-slate-350 cursor-pointer select-none">
          <input 
            :checked="showLesions"
            @change="emit('update:showLesions', $event.target.checked)"
            type="checkbox" 
            class="rounded text-teal-600 focus:ring-teal-500 border-slate-300" 
          />
          <span>Highlight Focal Lesions</span>
        </label>
      </div>
    </div>

    <!-- Proceed Trigger Card -->
    <div class="frosted-glass-panel p-5 flex flex-col justify-between min-h-[130px] border border-slate-200/80 bg-white/60">
      <div class="space-y-2">
        <div class="section-title">Proceed to Metrics</div>
        <p class="text-[10px] text-slate-500 dark:text-slate-400 leading-normal font-semibold">
          Contrast calibration is complete. Continue to evaluate voxel-based similarity metrics.
        </p>
      </div>
      <button 
        @click="emit('proceed')"
        class="w-full flex items-center justify-center gap-1.5 py-3 text-xs font-bold uppercase tracking-wider rounded-xl clinical-btn-primary active-shrink mt-4"
      >
        Analyze Metrics <ChevronRight class="w-3.5 h-3.5" />
      </button>
    </div>
  </div>
</template>

<style scoped>
input[type="range"]::-webkit-slider-thumb {
  appearance: none;
  width: 10px;
  height: 10px;
  background: #f9fbfc;
border: 1px solid #e6eef2;
border-radius: 14px;
  cursor: pointer;
}
</style>
