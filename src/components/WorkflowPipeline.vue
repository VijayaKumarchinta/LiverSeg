
<script setup>
import { Sliders, Brain, Cpu, BarChart3, CheckCircle } from 'lucide-vue-next'

const pipelineSteps = [
  {
    num: '01',
    title: 'Image Preprocessing',
    icon: Sliders,
    points: [
      'Isotropic resampling of anisotropic voxels',
      'Hounsfield Unit (HU) window clamp [ -100, 400 ]',
      'Gaussian normalization of pixel intensities',
      'Data augmentation via elastic transforms'
    ]
  },
  {
    num: '02',
    title: 'Attention U-Net Core',
    icon: Brain,
    points: [
      'Multi-level encoder/decoder convolutions',
      'Skip connections with active attention gates',
      'Focal Tversky loss optimization weights',
      'Dilation convolutions for contextual capture'
    ]
  },
  {
    num: '03',
    title: 'Post-Process Optimization',
    icon: Cpu,
    points: [
      'Morphological opening to eliminate small voids',
      'Largest connected component boundary filtering',
      '3D Gaussian surface smoothing contours',
      'Anatomical constraint volume check'
    ]
  },
  {
    num: '04',
    title: 'Clinical Evaluation',
    icon: BarChart3,
    points: [
      'Dice similarity coefficient matching test',
      'Hausdorff distance 95th percentile metric',
      'Volumetric calculation in cubic centimeters',
      'Automated structure report serialization'
    ]
  }
]
</script>

<template>
  <section class="relative py-20 bg-white/60 border-b border-clinicalBorder/40">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <!-- Section Header -->
      <div 
        class="max-w-3xl mx-auto text-center mb-16 space-y-4"
        v-motion
        :initial="{ opacity: 0, y: 30 }"
        :enter="{ opacity: 1, y: 0, transition: { duration: 600, ease: 'easeOut' } }"
      >
        <span class="text-xs font-bold uppercase tracking-widest text-clinicalCyan bg-clinicalCyan/10 px-3 py-1 rounded-full">
          Technical Pipeline
        </span>
        <h2 class="text-3xl sm:text-4xl font-extrabold tracking-tight text-clinicalNavy">
          Segmentor Deep Learning Architecture
        </h2>
        <div class="w-16 h-1 bg-gradient-to-r from-clinicalCyan to-clinicalEmerald mx-auto rounded-full"></div>
        <p class="text-base text-clinicalMuted leading-relaxed">
          Deep dive into the 3D neural pipeline that processes raw CT voxels into clinically validated contours.
        </p>
      </div>

      <!-- Pipeline Cards Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div 
          v-for="(step, idx) in pipelineSteps" 
          :key="step.num"
          class="glass-card rounded-xl2 p-7.5 border border-clinicalBorder shadow-soft hover:shadow-clinical hover:border-clinicalCyan/40 hover:-translate-y-1 group relative overflow-hidden transition-all duration-300"
          v-motion
          :initial="{ opacity: 0, scale: 0.95 }"
          :enter="{ opacity: 1, scale: 1, transition: { duration: 550, ease: 'easeOut', delay: idx * 100 } }"
        >
          <!-- Giant Faded Step Number in Background -->
          <div class="absolute right-4 bottom-2 text-8xl font-black text-slate-100 font-mono select-none group-hover:text-clinicalCyan/5 transition-colors duration-300">
            {{ step.num }}
          </div>

          <div class="relative z-10 space-y-5">
            <!-- Icon Area with gradient border hover glow -->
            <div class="flex items-center gap-4">
              <div class="relative w-12 h-12 rounded-xl bg-gradient-to-tr from-clinicalCyan to-clinicalEmerald p-[1.5px] group-hover:shadow-[0_0_20px_rgba(6,182,212,0.25)] transition-shadow duration-300">
                <div class="w-full h-full bg-white rounded-[10.5px] flex items-center justify-center text-clinicalCyan group-hover:text-clinicalEmerald transition-colors duration-300">
                  <component :is="step.icon" class="w-5.5 h-5.5" />
                </div>
              </div>
              <h3 class="text-lg font-bold text-clinicalNavy group-hover:text-clinicalCyan transition-colors">
                {{ step.title }}
              </h3>
            </div>

            <!-- Bullet Points list -->
            <ul class="space-y-3">
              <li 
                v-for="(point, pIdx) in step.points" 
                :key="pIdx"
                class="flex items-start gap-2 text-xs text-clinicalMuted"
              >
                <CheckCircle class="w-3.5 h-3.5 text-clinicalCyan/75 mt-0.5 flex-shrink-0" />
                <span class="leading-normal">{{ point }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>

    </div>
  </section>
</template>
