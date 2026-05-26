<script setup>
import { Brain, ScanLine, Activity, ArrowRight, Layers, HelpCircle, CheckCircle, Database } from 'lucide-vue-next'

const stats = [
  { name: 'Segmentation Accuracy', value: '95.8% Dice', icon: Activity, desc: 'Validated on clinical datasets' },
  { name: 'Model Architecture', value: 'Attention U-Net', icon: Brain, desc: 'Deep learning medical backbone' },
  { name: 'Target Modality', value: 'Abdominal CT', icon: ScanLine, desc: 'Contrast & non-contrast scans' }
]
</script>

<template>
  <section id="hero" class="relative pt-32 pb-20 md:pt-40 md:pb-28 overflow-hidden">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-8 items-center">
        
        <!-- Left Side: Copy and Stats -->
        <div 
          class="lg:col-span-6 space-y-8 z-10"
          v-motion
          :initial="{ opacity: 0, x: -50 }"
          :enter="{ opacity: 1, x: 0, transition: { duration: 600, ease: 'easeOut' } }"
        >
          <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-clinicalCyan/10 border border-clinicalCyan/30 text-clinicalCyan text-xs font-semibold uppercase tracking-wider">
            <span class="w-2 h-2 rounded-full bg-clinicalCyan animate-pulse"></span>
            Clinical Decision Support Platform
          </div>
          
          <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-clinicalNavy leading-[1.1]">
            AI-Powered <br />
            <span class="bg-gradient-to-r from-clinicalCyan via-clinicalCyan to-clinicalEmerald bg-clip-text text-transparent">
              Liver Segmentation
            </span>
          </h1>

          <p class="text-lg font-medium text-clinicalNavy/80 max-w-xl">
            Automated, high-precision contouring of liver parenchyma and lesions from abdominal CT scans in under 5 seconds.
          </p>

          <p class="text-base text-clinicalMuted max-w-xl leading-relaxed">
            Integrating advanced Attention U-Net convolutional networks into clinical PACS/DICOM workflows. Empowers radiologists with precise volumetric measurements, saving reading time and minimizing inter-observer variability.
          </p>

          <!-- Buttons -->
          <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-4">
            <a 
              href="#workflow" 
              class="flex items-center justify-center gap-2 px-7 py-3.5 text-sm font-semibold text-white bg-gradient-to-r from-clinicalCyan to-clinicalEmerald rounded-full shadow-clinical hover:shadow-lg hover:brightness-105 active:scale-98 transition-all duration-300"
              v-motion
              :hovered="{ scale: 1.03 }"
              :tapped="{ scale: 0.98 }"
            >
              Explore Clinical Workflow
              <ArrowRight class="w-4 h-4" />
            </a>
            <a 
              href="#technology" 
              class="flex items-center justify-center gap-2 px-7 py-3.5 text-sm font-semibold text-clinicalNavy/90 bg-white border border-clinicalBorder rounded-full shadow-soft hover:bg-clinicalBg hover:text-clinicalCyan active:scale-98 transition-all duration-300"
              v-motion
              :hovered="{ scale: 1.03 }"
              :tapped="{ scale: 0.98 }"
            >
              View Architecture
            </a>
          </div>

          <!-- Quick Stats Grid -->
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-6 border-t border-clinicalBorder/60">
            <div 
              v-for="(stat, idx) in stats" 
              :key="idx"
              class="glass-card p-4 rounded-xl2 flex flex-col justify-between hover:shadow-soft transition-all duration-300 hover:-translate-y-0.5 border border-clinicalBorder group"
            >
              <div class="flex items-center justify-between mb-2">
                <span class="p-2 rounded-lg bg-clinicalCyan/10 text-clinicalCyan group-hover:bg-clinicalCyan/20 group-hover:text-clinicalEmerald transition-colors duration-300">
                  <component :is="stat.icon" class="w-4.5 h-4.5" />
                </span>
                <span class="text-[9px] uppercase tracking-wider font-bold text-clinicalMuted">Active</span>
              </div>
              <div>
                <div class="text-base font-bold text-clinicalNavy">{{ stat.value }}</div>
                <div class="text-[11px] text-clinicalMuted font-medium mt-0.5">{{ stat.name }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Side: Interactive AI Radiography Dashboard -->
        <div 
          class="lg:col-span-6 relative flex justify-center items-center"
          v-motion
          :initial="{ opacity: 0, x: 50 }"
          :enter="{ opacity: 1, x: 0, transition: { duration: 600, ease: 'easeOut', delay: 100 } }"
        >
          <!-- Outer Dashboard Frame -->
          <div class="relative w-full max-w-[500px] aspect-square rounded-xl2 bg-slate-900 border border-slate-800 shadow-clinical overflow-hidden flex flex-col p-4 glow-cyan">
            <!-- Scan grid lines -->
            <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_center,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:16px_16px] pointer-events-none"></div>
            
            <!-- Header bar of dashboard -->
            <div class="flex items-center justify-between pb-3 border-b border-slate-800 text-[11px] font-mono text-slate-400 z-10">
              <div class="flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-clinicalCyan animate-ping"></span>
                <span>CT_AXIAL_ABDOMEN_084</span>
              </div>
              <div class="flex items-center gap-3">
                <span>ZOOM: 100%</span>
                <span>W/L: 400/40</span>
              </div>
            </div>

            <!-- Main CT Slice Canvas representation -->
            <div class="relative flex-1 flex items-center justify-center my-3 rounded-lg bg-black/60 overflow-hidden border border-slate-800/80">
              <!-- Scale bar -->
              <div class="absolute left-2 top-0 bottom-0 w-2 flex flex-col justify-between py-4 text-[9px] font-mono text-slate-500">
                <span>10cm</span>
                <span>5cm</span>
                <span>0cm</span>
              </div>
              
              <!-- Transverse CT Abdomen simulation with SVG -->
              <svg viewBox="0 0 300 240" class="w-full h-full p-2 select-none">
                <!-- Spine (posterior anatomy) -->
                <path d="M150,195 Q140,190 142,175 Q150,182 158,175 Q160,190 150,195" fill="#475569" stroke="#64748b" stroke-width="1.5"/>
                <!-- Aorta -->
                <circle cx="150" cy="165" r="9" fill="#1e293b" stroke="#ef4444" stroke-width="1" />
                <circle cx="150" cy="165" r="5" fill="#ef4444" opacity="0.3" />
                
                <!-- Stomach / Bowel Loops (clinical dark voids) -->
                <path d="M175,120 Q190,95 215,100 Q235,115 220,145 Q190,160 175,120 Z" fill="#0f172a" stroke="#334155" stroke-width="1"/>
                
                <!-- Kidney Left -->
                <path d="M210,160 Q225,165 220,185 Q205,190 195,175 Z" fill="#334155" stroke="#475569" stroke-width="1"/>
                <!-- Kidney Right -->
                <path d="M90,160 Q75,165 80,185 Q95,190 105,175 Z" fill="#334155" stroke="#475569" stroke-width="1"/>

                <!-- Liver Parenchymal Anatomy (grey background body) -->
                <path id="liver-body" d="M60,120 Q55,75 110,65 Q170,55 175,90 Q180,120 160,145 Q130,170 100,160 Q80,150 60,120 Z" fill="#334155" stroke="#475569" stroke-width="1" />

                <!-- AI SEGMENTATION OVERLAY MASK (Emerald green glowing overlay) -->
                <path 
                  id="liver-mask" 
                  d="M60,120 Q55,75 110,65 Q170,55 175,90 Q180,120 160,145 Q130,170 100,160 Q80,150 60,120 Z" 
                  fill="url(#emeraldGrad)" 
                  stroke="#10b981" 
                  stroke-width="2" 
                  stroke-dasharray="3,3"
                  class="animate-pulse"
                  style="animation-duration: 4s;"
                />

                <!-- Defending Gradient -->
                <defs>
                  <linearGradient id="emeraldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#06b6d4" stop-opacity="0.35" />
                    <stop offset="100%" stop-color="#10b981" stop-opacity="0.5" />
                  </linearGradient>
                </defs>

                <!-- Annotation pointers -->
                <g class="transition-opacity duration-300">
                  <line x1="110" y1="100" x2="60" y2="40" stroke="#06b6d4" stroke-width="1" />
                  <circle cx="110" cy="100" r="2.5" fill="#06b6d4" />
                  <rect x="15" y="20" width="70" height="15" rx="3" fill="#0f172a" stroke="#06b6d4" stroke-width="1" />
                  <text x="22" y="31" fill="#06b6d4" font-size="8" font-family="monospace">LIVER_LOBE_R</text>
                </g>

                <g class="transition-opacity duration-300">
                  <line x1="165" y1="105" x2="230" y2="50" stroke="#10b981" stroke-width="1" />
                  <circle cx="165" cy="105" r="2.5" fill="#10b981" />
                  <rect x="205" y="30" width="80" height="15" rx="3" fill="#0f172a" stroke="#10b981" stroke-width="1" />
                  <text x="210" y="41" fill="#10b981" font-size="8" font-family="monospace">SEGMENT_V_VI</text>
                </g>
              </svg>

              <!-- Target reticle -->
              <div class="absolute inset-0 border border-dashed border-slate-800/40 pointer-events-none"></div>
              <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-8 h-8 pointer-events-none flex items-center justify-center text-slate-500">
                <span class="absolute w-full h-[0.5px] bg-slate-500/30"></span>
                <span class="absolute h-full w-[0.5px] bg-slate-500/30"></span>
                <span class="w-1.5 h-1.5 rounded-full bg-clinicalCyan"></span>
              </div>
            </div>

            <!-- Interactive Metrics & Status footer -->
            <div class="grid grid-cols-3 gap-2 mt-2 z-10">
              <div class="bg-slate-950/80 border border-slate-800 p-2.5 rounded-lg flex flex-col">
                <span class="text-[8px] uppercase tracking-wider text-slate-500 font-semibold font-mono">DICE COEFFICIENT</span>
                <span class="text-sm font-bold text-clinicalCyan font-mono">0.9631</span>
              </div>
              <div class="bg-slate-950/80 border border-slate-800 p-2.5 rounded-lg flex flex-col">
                <span class="text-[8px] uppercase tracking-wider text-slate-500 font-semibold font-mono">LIVER VOLUME</span>
                <span class="text-sm font-bold text-white font-mono">1,418.5 cc</span>
              </div>
              <div class="bg-slate-950/80 border border-slate-800 p-2.5 rounded-lg flex flex-col">
                <span class="text-[8px] uppercase tracking-wider text-slate-500 font-semibold font-mono">PREDICTION STATUS</span>
                <span class="text-sm font-bold text-clinicalEmerald font-mono flex items-center gap-1">
                  <span class="w-1.5 h-1.5 rounded-full bg-clinicalEmerald animate-pulse"></span>
                  READY
                </span>
              </div>
            </div>

            <!-- Floating Overlay Badge 1 (Dice overlay) -->
            <div 
              class="absolute top-10 -right-4 bg-white/90 border border-clinicalBorder shadow-clinical px-4 py-2.5 rounded-xl flex items-center gap-3 z-25 text-clinicalNavy"
              v-motion
              :initial="{ y: 15 }"
              :enter="{ y: 0, transition: { repeat: Infinity, repeatType: 'reverse', duration: 3000, ease: 'easeInOut' } }"
            >
              <div class="p-1.5 bg-clinicalCyan/10 rounded-lg text-clinicalCyan">
                <Layers class="w-4 h-4" />
              </div>
              <div class="flex flex-col">
                <span class="text-[9px] uppercase tracking-wider font-bold text-clinicalMuted">Attention U-Net v2</span>
                <span class="text-xs font-extrabold text-clinicalNavy">Inference: 3.12s</span>
              </div>
            </div>

            <!-- Floating Overlay Badge 2 (AI verification status) -->
            <div 
              class="absolute bottom-16 -left-6 bg-white/90 border border-clinicalBorder shadow-clinical px-4 py-2.5 rounded-xl flex items-center gap-3 z-25 text-clinicalNavy"
              v-motion
              :initial="{ y: -10 }"
              :enter="{ y: 5, transition: { repeat: Infinity, repeatType: 'reverse', duration: 2500, ease: 'easeInOut' } }"
            >
              <div class="p-1.5 bg-clinicalEmerald/10 rounded-lg text-clinicalEmerald">
                <CheckCircle class="w-4 h-4" />
              </div>
              <div class="flex flex-col">
                <span class="text-[9px] uppercase tracking-wider font-bold text-clinicalMuted">DICOM Verification</span>
                <span class="text-xs font-extrabold text-clinicalNavy">FDA Class II Compliant</span>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </section>
</template>
