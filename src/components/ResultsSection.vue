<script setup>
import { Check, CheckCircle2, TrendingUp, ShieldAlert, Monitor, Activity } from 'lucide-vue-next'

const checklist = [
  'Validated on multi-center abdominal CT datasets',
  'Attention U-Net architecture minimizing boundary loss',
  'Optimized latency for real-time clinical workflows',
  'Interoperable with research PACS and clinical DICOM standard routers'
]
</script>

<template>
  <section id="results" class="relative py-20 bg-gradient-to-b from-clinicalBg to-white border-t border-clinicalBorder/40">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
        
        <!-- Left Side: Copy and Checklist -->
        <div 
          class="lg:col-span-6 space-y-8"
          v-motion
          :initial="{ opacity: 0, x: -40 }"
          :enter="{ opacity: 1, x: 0, transition: { duration: 600, ease: 'easeOut' } }"
        >
          <div class="space-y-4">
            <span class="text-xs font-bold uppercase tracking-widest text-clinicalEmerald bg-clinicalEmerald/10 px-3 py-1 rounded-full">
              Clinical Validation
            </span>
            <h2 class="text-3xl sm:text-4xl font-extrabold tracking-tight text-clinicalNavy">
              Validated Precision. <br />
              Trusted in Radiology.
            </h2>
            <div class="w-16 h-1 bg-gradient-to-r from-clinicalCyan to-clinicalEmerald rounded-full"></div>
            <p class="text-base text-clinicalMuted leading-relaxed">
              Our automated segmentation pipelines are rigorously validated against gold-standard manual readings, assuring diagnostic-grade outputs suitable for transplant sizing and oncology reviews.
            </p>
          </div>

          <!-- Checklist with staggered entrance support -->
          <div class="space-y-4">
            <div 
              v-for="(item, idx) in checklist" 
              :key="idx"
              class="flex items-start gap-3 bg-white/70 border border-clinicalBorder/50 rounded-xl p-4 shadow-sm hover:shadow-soft transition-shadow duration-300"
              v-motion
              :initial="{ opacity: 0, y: 15 }"
              :enter="{ opacity: 1, y: 0, transition: { duration: 400, delay: idx * 100 } }"
            >
              <span class="p-1 rounded-full bg-clinicalEmerald/15 text-clinicalEmerald flex-shrink-0 mt-0.5">
                <Check class="w-4 h-4 stroke-[3]" />
              </span>
              <span class="text-sm font-semibold text-clinicalNavy/90">{{ item }}</span>
            </div>
          </div>
        </div>

        <!-- Right Side: Clinician Workstation Illustration & Floating Card -->
        <div 
          class="lg:col-span-6 relative flex justify-center items-center h-[400px]"
          v-motion
          :initial="{ opacity: 0, x: 40 }"
          :enter="{ opacity: 1, x: 0, transition: { duration: 600, delay: 200 } }"
        >
          <!-- Modern Workstation Graphics frame -->
          <div class="relative w-full max-w-[420px] aspect-[4/3] rounded-2xl bg-white border border-clinicalBorder shadow-clinical flex items-center justify-center p-6 overflow-hidden">
            <div class="absolute inset-0 bg-gradient-to-tr from-clinicalCyan/5 via-transparent to-clinicalEmerald/5 pointer-events-none"></div>
            
            <!-- Graphic layout -->
            <svg viewBox="0 0 200 150" class="w-full h-full text-slate-200">
              <!-- Monitor workstation base -->
              <rect x="50" y="20" width="100" height="70" rx="4" fill="#0f172a" stroke="#1e293b" stroke-width="1.5" />
              <rect x="53" y="23" width="94" height="54" rx="2" fill="#1e293b" />
              <line x1="100" y1="90" x2="100" y2="115" stroke="#0f172a" stroke-width="6" />
              <rect x="80" y="115" width="40" height="6" rx="2" fill="#0f172a" />
              
              <!-- Keyboard -->
              <rect x="70" y="128" width="60" height="4" rx="1" fill="#475569" />

              <!-- Doctor/Clinician silhouette sitting next to monitor -->
              <path d="M25,120 C25,95 40,90 45,90 C50,90 53,92 53,96 C53,105 50,110 50,120 Z" fill="#64748b" opacity="0.15" />
              <circle cx="45" cy="80" r="8" fill="#64748b" opacity="0.15" />

              <!-- Monitor screen content representation -->
              <!-- Grid lines inside screen -->
              <line x1="53" y1="50" x2="147" y2="50" stroke="#334155" stroke-width="0.5" stroke-dasharray="1,2" />
              <line x1="100" y1="23" x2="100" y2="77" stroke="#334155" stroke-width="0.5" stroke-dasharray="1,2" />

              <!-- Volumetric curve graph inside screen -->
              <path d="M56,70 Q70,45 85,60 T120,40 T144,30" fill="none" stroke="#06b6d4" stroke-width="1.5" stroke-linecap="round" />
              <circle cx="85" cy="60" r="2" fill="#10b981" />
              <circle cx="120" cy="40" r="2" fill="#06b6d4" />
            </svg>

            <!-- Floating Medical AI Card overlay -->
            <div 
              class="absolute top-8 right-0 bg-white/95 border border-clinicalBorder shadow-clinical rounded-xl p-4.5 w-60 z-20"
              v-motion
              :initial="{ y: 10 }"
              :enter="{ y: -10, transition: { repeat: Infinity, repeatType: 'reverse', duration: 3200, ease: 'easeInOut' } }"
            >
              <div class="flex items-center justify-between mb-3 pb-2.5 border-b border-clinicalBorder">
                <div class="flex items-center gap-1.5 text-clinicalCyan">
                  <Monitor class="w-4 h-4" />
                  <span class="text-[10px] font-bold uppercase tracking-wider font-mono">Inference Output</span>
                </div>
                <span class="w-1.5 h-1.5 rounded-full bg-clinicalEmerald animate-ping"></span>
              </div>
              
              <!-- Metrics list -->
              <div class="space-y-2">
                <div class="flex justify-between items-center text-xs">
                  <span class="text-clinicalMuted font-medium">Dice Score:</span>
                  <span class="font-bold text-clinicalNavy font-mono">95.8% Dice</span>
                </div>
                <div class="flex justify-between items-center text-xs">
                  <span class="text-clinicalMuted font-medium">Status:</span>
                  <span class="font-semibold text-clinicalEmerald flex items-center gap-1">
                    <CheckCircle2 class="w-3.5 h-3.5" /> Complete
                  </span>
                </div>
                <div class="flex justify-between items-center text-xs">
                  <span class="text-clinicalMuted font-medium">Avg Latency:</span>
                  <span class="font-bold text-clinicalNavy font-mono">~3.2s / vol</span>
                </div>
              </div>
            </div>

            <!-- Floating Accuracy badge overlay -->
            <div 
              class="absolute bottom-8 left-4 bg-white/95 border border-clinicalBorder shadow-clinical rounded-lg px-3.5 py-2 flex items-center gap-2.5 z-20"
              v-motion
              :initial="{ y: -5 }"
              :enter="{ y: 5, transition: { repeat: Infinity, repeatType: 'reverse', duration: 2800, ease: 'easeInOut' } }"
            >
              <div class="p-1.5 bg-clinicalEmerald/15 text-clinicalEmerald rounded-md">
                <TrendingUp class="w-4 h-4" />
              </div>
              <div class="flex flex-col">
                <span class="text-[8px] uppercase tracking-wider font-extrabold text-clinicalMuted">Accuracy Gain</span>
                <span class="text-xs font-black text-clinicalNavy">+18.5% over U-Net</span>
              </div>
            </div>

          </div>
        </div>

      </div>
    </div>
  </section>
</template>
