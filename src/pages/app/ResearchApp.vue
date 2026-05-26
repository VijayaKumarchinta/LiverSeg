<script setup>
import { ref, computed } from 'vue'
import { useAppState } from '../../composables/useAppState'

const modelPerformanceHistory = []
const dailyScanActivity = []
import {
  Brain, Cpu, Layers, TrendingUp, Activity, Database, AlertCircle,
  CheckCircle2, RefreshCw, BarChart3, Zap, Server, Clock
} from 'lucide-vue-next'

const { patients } = useAppState()

const modelParams = [
  { param: 'Architecture',    val: '3D Attention U-Net' },
  { param: 'Input Size',      val: '512×512×20 voxels' },
  { param: 'Optimizer',       val: 'AdamW · lr=3e-4' },
  { param: 'Pre-trained',     val: 'MONAI Liver CT Zoo' },
  { param: 'Precision',       val: 'FP16 Half Precision' },
  { param: 'Batch Size',      val: '2 per GPU' },
  { param: 'Loss Function',   val: 'DiceCE + Focal' },
  { param: 'Training Epochs', val: '400 · Convergence at 350' },
]

const layers = [
  { name: 'Input Resample Block',       details: 'Isotropic voxel spacing normalization [1mm, 1mm, 1mm]',   node: '#01' },
  { name: 'Encoding Residuals L1–L4',   details: 'Extracts low-level edge features · kernel 3×3×3',          node: '#02' },
  { name: 'Attention Gate Junctions',   details: 'Masks non-hepatic background · Dice weight +2.1%',         node: '#03' },
  { name: 'Bottleneck ASPP Block',      details: 'Atrous spatial pyramid pooling for multi-scale context',    node: '#04' },
  { name: 'Decoding Conv Block L1–L4',  details: 'Interpolates spatial resolution back to input dimensions', node: '#05' },
  { name: 'Sigmoid Normalizer Outlet',  details: 'Voxel-wise liver probability thresholding [0.0, 1.0]',     node: '#06' },
]

const gpuUtilization = ref(48)
const memoryUsed = ref(9.2)
const memoryTotal = ref(16)

const inferenceLogs = []

const chartMax = computed(() => {
  if (modelPerformanceHistory.length === 0) return 100
  return Math.max(...modelPerformanceHistory.map(d => d.dice))
})
const chartMin = 85
const diceRange = computed(() => chartMax.value - chartMin > 0 ? chartMax.value - chartMin : 1)

const chartPoint = (i, val) => {
  const x = modelPerformanceHistory.length > 1 ? (i / (modelPerformanceHistory.length - 1)) * 260 + 10 : 10
  const y = 80 - ((val - chartMin) / diceRange.value) * 65
  return { x, y }
}

const pathD = computed(() => {
  return modelPerformanceHistory.map((d, i) => {
    const { x, y } = chartPoint(i, d.dice)
    return `${i === 0 ? 'M' : 'L'} ${x},${y}`
  }).join(' ')
})

const currentModel = { version: 'v1.4.2', dice: '95.8%', iou: '91.2%', params: '31.2M', status: 'Production' }
</script>

<template>
  <div class="space-y-5 animate-fade-in-up">

    <!-- Header + Stats strip -->
    <div class="frosted-glass-panel p-4 flex flex-wrap items-center justify-between gap-4">
      <div>
        <div class="section-title">AI Research & Monitoring</div>
        <h2 class="text-sm font-black text-slate-800 mt-0.5">Model Performance Dashboard</h2>
        <p class="text-[10px] text-slate-500 font-medium mt-0.5">3D Attention U-Net · MONAI Framework · Production v1.4.2</p>
      </div>
      <div class="flex items-center gap-2.5">
        <div class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-teal-50 border border-teal-100">
          <div class="w-2 h-2 rounded-full bg-teal-500 animate-pulse"></div>
          <span class="text-[9px] font-bold text-teal-700">Model Online · {{ currentModel.version }}</span>
        </div>
        <button class="clinical-btn-secondary px-3 py-1.5 rounded-lg text-[9px] font-bold flex items-center gap-1.5 active-shrink">
          <RefreshCw class="w-3 h-3" /> Refresh Metrics
        </button>
      </div>
    </div>

    <!-- KPI Row -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <div v-for="(kpi, i) in [
        { label: 'Validation Dice', value: '95.8%', icon: Activity, color: 'text-teal-600', bg: 'bg-teal-50', sub: 'Best epoch 400' },
        { label: 'Mean IoU', value: '91.2%', icon: BarChart3, color: 'text-sky-600', bg: 'bg-sky-50', sub: 'Test set average' },
        { label: 'GPU Utilization', value: gpuUtilization + '%', icon: Cpu, color: 'text-purple-600', bg: 'bg-purple-50', sub: 'NVIDIA T4 · Active' },
        { label: 'Model Parameters', value: '31.2M', icon: Database, color: 'text-amber-600', bg: 'bg-amber-50', sub: 'FP16 quantized' },
      ]" :key="i" class="metric-card p-4 flex items-center gap-3">
        <div :class="['w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0', kpi.bg]">
          <component :is="kpi.icon" :class="['w-5 h-5', kpi.color]" />
        </div>
        <div>
          <div class="text-[9px] font-bold uppercase tracking-wider text-slate-400">{{ kpi.label }}</div>
          <div class="text-xl font-black text-slate-900">{{ kpi.value }}</div>
          <div class="text-[9px] text-slate-500 font-semibold">{{ kpi.sub }}</div>
        </div>
      </div>
    </div>

    <!-- Main grid -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-5">

      <!-- Left: Dice Trend + Inference Logs -->
      <div class="lg:col-span-8 space-y-5">

        <!-- Dice Trend Chart -->
        <div class="frosted-glass-panel p-5">
          <div class="flex items-center justify-between mb-4">
            <div>
              <div class="section-title">Training Performance</div>
              <h3 class="text-xs font-black text-slate-800 mt-0.5">Dice Score vs Training Epoch</h3>
            </div>
            <span class="text-[9px] font-bold text-teal-600 bg-teal-50 border border-teal-100 px-2 py-1 rounded-lg">400 Epochs Converged</span>
          </div>

          <div class="relative">
            <svg viewBox="0 10 280 80" class="w-full h-36">
              <!-- Grid lines -->
              <g stroke="#e2e8f0" stroke-width="0.4">
                <line v-for="y in [20, 35, 50, 65, 80]" :key="y" x1="10" :y1="y" x2="270" :y2="y" />
              </g>
              <!-- Y labels -->
              <g class="hud-text" fill="#94a3b8" font-size="4.5">
                <text v-for="(v, i) in [chartMin, 88, 91, 94, 97]" :key="i" x="6" :y="80 - i * 16.25 + 1.5" text-anchor="end">{{ v }}</text>
              </g>
              <!-- Area fill -->
              <path :d="`${pathD} L 270,80 L 10,80 Z`" fill="url(#diceGrad)" opacity="0.25" />
              <!-- Line -->
              <path :d="pathD" fill="none" stroke="#14b8a6" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
              <!-- Data points -->
              <circle v-for="(d, i) in modelPerformanceHistory" :key="i"
                :cx="chartPoint(i, d.dice).x" :cy="chartPoint(i, d.dice).y"
                r="2" fill="#fff" stroke="#14b8a6" stroke-width="1.2" />
              <defs>
                <linearGradient id="diceGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stop-color="#14b8a6" />
                  <stop offset="100%" stop-color="#14b8a6" stop-opacity="0" />
                </linearGradient>
              </defs>
            </svg>
            <!-- Epoch labels -->
            <div class="flex justify-between mt-1 px-2">
              <span v-for="d in modelPerformanceHistory" :key="d.epoch" class="text-[7px] font-bold text-slate-400 font-mono">{{ d.epoch }}</span>
            </div>
          </div>
        </div>

        <!-- Inference Logs Table -->
        <div class="frosted-glass-panel overflow-hidden">
          <div class="flex items-center justify-between px-5 py-3.5 border-b border-slate-200/50 bg-white/30">
            <div>
              <div class="section-title">Inference Logs</div>
              <h3 class="text-xs font-black text-slate-800 mt-0.5">Recent Pipeline Executions</h3>
            </div>
            <Clock class="w-4 h-4 text-slate-300" />
          </div>
          <table class="w-full clinical-table">
            <thead>
              <tr>
                <th>Timestamp</th>
                <th>Patient ID</th>
                <th>Stage</th>
                <th>Dice Score</th>
                <th>Inference Time</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="log in inferenceLogs" :key="log.ts">
                <td class="font-mono text-[10px] text-slate-500">{{ log.ts }}</td>
                <td class="font-mono text-[11px] font-bold text-slate-700">{{ log.patientId }}</td>
                <td class="text-[11px] text-slate-600">{{ log.stage }}</td>
                <td class="font-mono text-[11px] font-bold text-teal-600">{{ log.dice }}</td>
                <td class="font-mono text-[11px] text-slate-500">{{ log.time }}</td>
                <td>
                  <span :class="['inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[8px] font-bold', log.status === 'ok' ? 'badge-completed' : 'badge-pending']">
                    <CheckCircle2 v-if="log.status==='ok'" class="w-2.5 h-2.5" />
                    <AlertCircle v-else class="w-2.5 h-2.5" />
                    {{ log.status === 'ok' ? 'Success' : 'Warning' }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Right: Model Config + GPU + Layer Map -->
      <div class="lg:col-span-4 space-y-4">

        <!-- GPU Monitor -->
        <div class="frosted-glass-panel p-4 space-y-3">
          <div class="flex items-center justify-between">
            <div class="section-title flex items-center gap-1.5"><Cpu class="w-3.5 h-3.5" /> Hardware</div>
            <span class="text-[8px] font-bold text-teal-600 bg-teal-50 px-1.5 py-0.5 rounded border border-teal-100">NVIDIA T4 · Online</span>
          </div>
          <div class="space-y-3">
            <div>
              <div class="flex justify-between text-[9px] font-bold text-slate-500 mb-1.5">
                <span>GPU Utilization</span><span class="text-slate-700">{{ gpuUtilization }}%</span>
              </div>
              <div class="progress-track h-2">
                <div class="progress-fill" :style="`width: ${gpuUtilization}%`"></div>
              </div>
            </div>
            <div>
              <div class="flex justify-between text-[9px] font-bold text-slate-500 mb-1.5">
                <span>VRAM Usage</span><span class="text-slate-700">{{ memoryUsed }}GB / {{ memoryTotal }}GB</span>
              </div>
              <div class="progress-track h-2">
                <div class="progress-fill" :style="`width: ${(memoryUsed/memoryTotal)*100}%`"></div>
              </div>
            </div>
            <div class="grid grid-cols-2 gap-2 pt-1">
              <div class="bg-slate-50/70 border border-slate-200/50 rounded-lg p-2 text-center">
                <div class="text-[8px] font-bold text-slate-400 uppercase">Throughput</div>
                <div class="text-xs font-black text-slate-800">3.1s avg</div>
              </div>
              <div class="bg-slate-50/70 border border-slate-200/50 rounded-lg p-2 text-center">
                <div class="text-[8px] font-bold text-slate-400 uppercase">Temperature</div>
                <div class="text-xs font-black text-slate-800">61°C</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Model Config -->
        <div class="frosted-glass-panel p-4 space-y-3">
          <div class="section-title flex items-center gap-1.5"><Layers class="w-3.5 h-3.5" /> Model Config</div>
          <div class="space-y-1.5">
            <div v-for="p in modelParams" :key="p.param"
              class="flex justify-between items-center py-1.5 border-b border-slate-100/60 last:border-0 text-[10px]">
              <span class="text-slate-500 font-medium">{{ p.param }}</span>
              <span class="font-bold text-slate-800 text-right ml-2">{{ p.val }}</span>
            </div>
          </div>
        </div>

        <!-- Validation metric highlight -->
        <div class="frosted-glass-panel p-4 space-y-2 border border-teal-100/60 bg-gradient-to-br from-teal-50/40 to-transparent">
          <div class="section-title text-teal-600">Validation Results</div>
          <div class="text-2xl font-black text-teal-800">95.8%</div>
          <div class="text-[9px] font-bold text-teal-700">Validation Dice Score</div>
          <p class="text-[9px] text-teal-600/80 leading-relaxed">
            Maintains reliable boundaries on contrast variations and metallic implant scattering. ONNX-accelerated inference.
          </p>
        </div>
      </div>
    </div>

    <!-- Layer Architecture -->
    <div class="frosted-glass-panel p-5">
      <div class="flex items-center gap-2 mb-4">
        <Brain class="w-4 h-4 text-teal-600" />
        <div>
          <div class="section-title">Network Architecture</div>
          <h3 class="text-xs font-black text-slate-800">3D Attention U-Net Pipeline Flow</h3>
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
        <div
          v-for="(layer, idx) in layers"
          :key="idx"
          class="flex items-start gap-3 p-3 bg-white/60 border border-slate-200/50 rounded-xl hover:border-teal-200 hover:bg-teal-50/20 transition-all"
        >
          <span class="font-mono text-[8px] bg-slate-100 border border-slate-200/60 text-slate-500 px-1.5 py-0.5 rounded font-bold flex-shrink-0 mt-0.5">{{ layer.node }}</span>
          <div>
            <div class="text-[10px] font-bold text-slate-800">{{ layer.name }}</div>
            <div class="text-[9px] text-slate-500 font-medium mt-0.5 leading-relaxed">{{ layer.details }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
