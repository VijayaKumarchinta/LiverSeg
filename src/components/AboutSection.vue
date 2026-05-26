<script setup>
import { AlertCircle, Cpu, Hospital, Check } from 'lucide-vue-next'

const features = [
  {
    title: 'Clinical Problem',
    icon: AlertCircle,
    color: 'text-red-500',
    bgColor: 'bg-red-50 border-red-100',
    description: 'Manual contouring of the liver and lesions is slow, tedious, and prone to clinical variability.',
    points: [
      'Takes 15-20 minutes per patient scan',
      'High inter-reader and intra-reader variability',
      'Increasing volume of abdominal imaging scans',
      'Radiologist cognitive overload and fatigue'
    ]
  },
  {
    title: 'AI Solution',
    icon: Cpu,
    color: 'text-clinicalCyan',
    bgColor: 'bg-cyan-50 border-clinicalBorder',
    description: 'Automated deep learning model designed for precision liver segmentation on abdominal CT.',
    points: [
      'Attention U-Net concentrates on target organs',
      'Full 3D volumetric segmentation in under 5s',
      'Integrates seamlessly via DICOM/PACS routers',
      'Automated lesion boundary detection support'
    ]
  },
  {
    title: 'Healthcare Impact',
    icon: Hospital,
    color: 'text-clinicalEmerald',
    bgColor: 'bg-emerald-50 border-emerald-100',
    description: 'Empowering clinical departments with quantitative metrics to optimize patient outcomes.',
    points: [
      'Saves up to 90% of manual annotation time',
      'Standardized reporting and repeatable metrics',
      'Precise volume calculation for transplant planning',
      'Enhanced tumor response tracking in oncology'
    ]
  }
]
</script>

<template>
  <section id="about" class="relative py-20 bg-white/40 border-t border-b border-clinicalBorder/40">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <!-- Section Header -->
      <div 
        class="text-center max-w-3xl mx-auto mb-16 space-y-4"
        v-motion
        :initial="{ opacity: 0, y: 30 }"
        :enter="{ opacity: 1, y: 0, transition: { duration: 600, ease: 'easeOut' } }"
      >
        <span class="text-xs font-bold uppercase tracking-widest text-clinicalCyan bg-clinicalCyan/10 px-3 py-1 rounded-full">
          Platform Overview
        </span>
        <h2 class="text-3xl sm:text-4xl font-extrabold tracking-tight text-clinicalNavy">
          Empowering Radiologists with Automated Segmentations
        </h2>
        <div class="w-16 h-1 bg-gradient-to-r from-clinicalCyan to-clinicalEmerald mx-auto rounded-full"></div>
        <p class="text-base text-clinicalMuted leading-relaxed">
          LiverSeg AI bridges the gap between state-of-the-art deep learning research and daily clinical workflows, standardizing liver volumetry and oncology reporting.
        </p>
      </div>

      <!-- Feature Cards Grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div 
          v-for="(feat, idx) in features" 
          :key="idx"
          class="glass-card rounded-xl2 p-8 flex flex-col justify-between shadow-soft border border-clinicalBorder transition-all duration-300 hover:shadow-clinical hover:-translate-y-2 hover:border-clinicalCyan/40 group relative overflow-hidden"
          v-motion
          :initial="{ opacity: 0, y: 50 }"
          :enter="{ opacity: 1, y: 0, transition: { duration: 600, ease: 'easeOut', delay: idx * 150 } }"
        >
          <!-- Background light accent glow -->
          <div class="absolute top-0 right-0 w-24 h-24 bg-gradient-to-bl from-clinicalCyan/5 to-transparent rounded-bl-full pointer-events-none"></div>

          <div>
            <!-- Header section of card -->
            <div class="flex items-center gap-4 mb-6">
              <div :class="['p-3 rounded-xl flex items-center justify-center border shadow-sm group-hover:scale-105 transition-transform duration-300', feat.bgColor]">
                <component :is="feat.icon" :class="['w-6 h-6', feat.color]" />
              </div>
              <h3 class="text-xl font-bold text-clinicalNavy">{{ feat.title }}</h3>
            </div>
            
            <p class="text-sm font-medium text-clinicalNavy/80 mb-6 leading-relaxed">
              {{ feat.description }}
            </p>
            
            <hr class="border-clinicalBorder/60 mb-6" />

            <!-- Core points -->
            <ul class="space-y-3.5">
              <li 
                v-for="(point, pIdx) in feat.points" 
                :key="pIdx"
                class="flex items-start gap-2.5 text-xs text-clinicalMuted"
              >
                <span class="p-0.5 rounded-full bg-clinicalCyan/10 text-clinicalCyan mt-0.5 flex-shrink-0">
                  <Check class="w-3.5 h-3.5 stroke-[3]" />
                </span>
                <span class="leading-normal">{{ point }}</span>
              </li>
            </ul>
          </div>

          <!-- Bottom bar accent -->
          <div class="mt-8 pt-4 border-t border-clinicalBorder/40">
            <span class="text-[10px] uppercase font-bold tracking-wider text-clinicalCyan flex items-center gap-1 group-hover:text-clinicalEmerald transition-colors">
              Read Protocol Details &rarr;
            </span>
          </div>
        </div>
      </div>

    </div>
  </section>
</template>
