<script setup>
import { Activity, ShieldCheck, ArrowRight, Brain, Zap, HardDrive, CheckCircle2 } from 'lucide-vue-next'

const coreStats = [
  { name: 'Segmentation Accuracy', value: '95.8% Dice', desc: 'Validated on LiTS datasets' },
  { name: 'Processing Latency', value: '3.12 Seconds', desc: 'Per volume axial ingestion' },
  { name: 'Model Backbone', value: 'Attention U-Net', desc: 'Active spatial weighting gates' }
]

const features = [
  {
    title: 'Precise Voxel Segmentation',
    desc: 'Deep learning contours isolate liver parenchyma, lobes, and lesion margins from abdominal contrast-enhanced CT scans.',
    icon: Brain
  },
  {
    title: 'PACS Router Integration',
    desc: 'Supports direct ingestion from DICOM routers via AE Title validation, auto-mapping output directly back to host servers.',
    icon: HardDrive
  },
  {
    title: 'Quantitative Reports',
    desc: 'Calculates liver volume, ratios, and lesion size indices automatically, generating print-ready DICOM Structured Reports.',
    icon: Zap
  }
]
</script>

<template>
  <div class="relative min-h-screen pt-28 pb-20 clinical-futuristic-bg overflow-hidden">
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
            Next-Gen Radiology AI
          </div>

          <!-- Title -->
          <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-slate-900 leading-[1.08]">
            Automated <br />
            <span class="bg-gradient-to-r from-teal-600 via-teal-500 to-sky-600 bg-clip-text text-transparent">
              Liver Segmentation
            </span>
          </h1>

          <p class="text-base sm:text-lg text-slate-500 max-w-xl leading-relaxed">
            High-precision automated contouring of liver parenchyma and lesions from abdominal CT slices. Designed for clinical decision support and seamless PACS integration.
          </p>

          <!-- Buttons -->
          <div class="flex flex-wrap items-center gap-4">
            <router-link 
              to="/app" 
              class="flex items-center gap-2 px-7 py-4 text-sm font-semibold rounded-xl clinical-btn-primary active-shrink"
            >
              Launch Workstation
              <ArrowRight class="w-4 h-4" />
            </router-link>
            
            <router-link 
              to="/platform" 
              class="flex items-center gap-2 px-7 py-4 text-sm font-semibold rounded-xl clinical-btn-secondary active-shrink"
            >
              Explore Pipeline
            </router-link>
          </div>

          <!-- Quick Statistics in Frosted Panel -->
          <div class="p-6 rounded-2xl frosted-glass-panel max-w-2xl">
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
              <div v-for="(stat, idx) in coreStats" :key="idx" class="space-y-1">
                <div class="text-2xl font-extrabold text-slate-900 bg-gradient-to-r from-teal-700 to-sky-700 bg-clip-text text-transparent">
                  {{ stat.value }}
                </div>
                <div class="text-xs font-bold text-slate-700 tracking-tight">{{ stat.name }}</div>
                <div class="text-[10px] text-slate-400 font-semibold leading-snug">{{ stat.desc }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- HERO GRAPHIC (Clinical Mockup representation with Floating Cards) -->
        <div class="lg:col-span-5 relative flex justify-center py-6">
          <!-- Gantry Scanner Ring Accent (behind container) -->
          <div class="absolute -inset-4 rounded-full border border-dashed border-teal-500/10 animate-spin [animation-duration:120s] pointer-events-none"></div>
          <div class="absolute -inset-8 rounded-full border border-slate-200/40 pointer-events-none"></div>

          <!-- Main Frosted PACS Console Card -->
          <div class="relative w-full max-w-[440px] aspect-[4/3] rounded-2xl p-4 flex flex-col justify-between frosted-glass-panel hover:scale-[1.02] duration-500 group">
            
            <!-- Top bar -->
            <div class="flex items-center justify-between pb-2.5 border-b border-slate-200/50 text-[10px] font-mono text-slate-550 font-semibold text-slate-550 text-slate-500">
              <span class="flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-teal-500 animate-ping"></span>
                CT_AXIAL_PARENCHYMA
              </span>
              <span>SL: 12 / 20</span>
            </div>

            <!-- Slice display (SVG mockup of liver) -->
            <div class="flex-1 flex items-center justify-center my-3 bg-black/95 rounded-xl border border-slate-800 relative overflow-hidden shadow-inner">
              <!-- Scan Crosshairs -->
              <div class="absolute inset-0 bg-[radial-gradient(rgba(255,255,255,0.015)_1px,transparent_1px)] bg-[size:14px_14px] pointer-events-none"></div>
              <line x1="50" y1="0" x2="50" y2="100" class="absolute w-full h-full stroke-white/5 stroke-dasharray-[2,2] pointer-events-none" />
              
              <svg viewBox="0 0 100 100" class="w-48 h-48 opacity-90 select-none">
                <!-- Abdominal boundary -->
                <circle cx="50" cy="50" r="42" fill="none" stroke="#1e293b" stroke-width="1.2" />
                <path d="M16,50 Q13,32 35,26 Q60,21 63,35 Q66,50 58,62 Q45,72 32,68 Q23,64 16,50 Z" fill="#0f172a" stroke="#334155" stroke-width="0.8" />
                <!-- Segmentation contour -->
                <path d="M16,50 Q13,32 35,26 Q60,21 63,35 Q66,50 58,62 Q45,72 32,68 Q23,64 16,50 Z" fill="rgba(20, 184, 166, 0.25)" stroke="#14b8a6" stroke-width="1.2" stroke-dasharray="2,2" class="animate-pulse" />
                <!-- Lesion -->
                <circle cx="34" cy="42" r="4.5" fill="rgba(239, 68, 68, 0.4)" stroke="#ef4444" stroke-width="0.5" />
              </svg>
              
              <!-- Scan line effect -->
              <div class="absolute left-0 right-0 h-px bg-teal-400/80 animate-scan"></div>
            </div>

            <!-- Mini metrics panel -->
            <div class="grid grid-cols-2 gap-2 text-[9px] font-mono text-slate-500 font-bold">
              <div class="bg-white/60 p-2 rounded-lg border border-slate-200/50 flex justify-between">
                <span>DICE COEFFICIENT:</span>
                <span class="text-teal-600 font-extrabold">0.958</span>
              </div>
              <div class="bg-white/60 p-2 rounded-lg border border-slate-200/50 flex justify-between">
                <span>VOLUME:</span>
                <span class="text-slate-800 font-extrabold">1418.5 cc</span>
              </div>
            </div>

            <!-- Floating Overlay Card 1: Accuracy Indicator (overlaps left) -->
            <div class="absolute -left-10 top-1/4 bg-white/90 border border-slate-250 border-slate-200/60 rounded-xl p-3 shadow-lg backdrop-blur-sm pointer-events-none transform -rotate-3 transition-transform group-hover:rotate-0 duration-300">
              <div class="flex items-center gap-2">
                <div class="w-6 h-6 rounded-lg bg-teal-50 text-teal-600 flex items-center justify-center">
                  <CheckCircle2 class="w-4 h-4" />
                </div>
                <div class="leading-none">
                  <div class="text-[9px] font-bold text-slate-400 uppercase">Verification</div>
                  <div class="text-xs font-extrabold text-slate-800">95.8% Overlap</div>
                </div>
              </div>
            </div>

            <!-- Floating Overlay Card 2: Regulatory Badge (overlaps bottom-right) -->
            <div class="absolute -right-8 bottom-8 bg-white/95 border border-slate-200/60 rounded-xl p-3 shadow-lg backdrop-blur-sm pointer-events-none transform rotate-3 transition-transform group-hover:rotate-0 duration-300">
              <div class="flex items-center gap-2.5">
                <div class="w-6 h-6 rounded-lg bg-sky-50 text-sky-600 flex items-center justify-center">
                  <ShieldCheck class="w-4.5 h-4.5" />
                </div>
                <div class="leading-none">
                  <div class="text-[9px] font-bold text-slate-400 uppercase">Compliance</div>
                  <div class="text-xs font-extrabold text-slate-800">HIPAA Certified</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- HIGHLIGHTS SECTION -->
      <div class="mt-32 py-16 border-t border-slate-200/60">
        <div class="text-center max-w-3xl mx-auto mb-20 space-y-4">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-teal-50 border border-teal-100 text-teal-700 text-[10px] font-bold uppercase tracking-wider">
            Clinical Standards
          </div>
          <h2 class="text-3xl sm:text-4xl font-extrabold tracking-tight text-slate-900">
            Validated Clinical Performance
          </h2>
          <p class="text-sm text-slate-500 max-w-xl mx-auto leading-relaxed">
            Engineered to coordinate with hospital PACS routers, standardizing liver volumetry measurements and focal lesion tracking.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div 
            v-for="(feature, idx) in features" 
            :key="idx" 
            class="p-7 rounded-2xl frosted-glass-panel hover:border-teal-500/40 transition-all duration-300 group flex flex-col justify-between"
          >
            <div class="space-y-4">
              <div class="w-11 h-11 rounded-xl bg-teal-50 text-teal-600 flex items-center justify-center group-hover:bg-teal-600 group-hover:text-white transition-colors duration-300 shadow-sm">
                <component :is="feature.icon" class="w-5 h-5" />
              </div>
              <h3 class="font-bold text-slate-900 text-base leading-snug tracking-tight">{{ feature.title }}</h3>
              <p class="text-xs text-slate-500 leading-relaxed font-semibold">{{ feature.desc }}</p>
            </div>
            
            <div class="mt-8 pt-4 border-t border-slate-100 flex items-center text-[10px] font-bold text-teal-600 group-hover:text-teal-700 tracking-wider">
              LEARN MORE <ArrowRight class="w-3 h-3 ml-1.5 transition-transform group-hover:translate-x-1" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
