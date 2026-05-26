<script setup>
import { 
  Cpu, 
  Layers, 
  Brain, 
  Database, 
  Activity, 
  ScanLine, 
  Sliders, 
  Zap 
} from 'lucide-vue-next'

const frameworks = [
  { title: 'PyTorch Core', desc: 'Used for neural network training and layer development.', icon: Cpu },
  { title: 'TensorFlow Serving', desc: 'Enables high-throughput production DICOM endpoints.', icon: Layers },
  { title: 'DICOM IO Engine', desc: 'SimpleITK and Nibabel bindings for pixel array parsing.', icon: Database },
  { title: 'GPU Acceleration', desc: 'CUDA-optimized tensor operations for rapid inference.', icon: Zap }
]

const concepts = [
  { title: 'Attention U-Net', desc: 'Active spatial gates targeting liver soft tissue regions.', icon: Brain },
  { title: 'Dice Similarity Loss', desc: 'Loss function optimizing overlap and contour precision.', icon: Activity },
  { title: 'Volumetric CT Masking', desc: '3D segmentations of organ bounds and vascular paths.', icon: ScanLine },
  { title: 'Elastic Deformation', desc: 'Augmentation pipelines simulating patient posture shifts.', icon: Sliders }
]
</script>

<template>
  <section id="technology" class="relative py-20 bg-gradient-to-b from-white to-clinicalBg">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <!-- Section Header -->
      <div 
        class="max-w-3xl mx-auto text-center mb-16 space-y-4"
        v-motion
        :initial="{ opacity: 0, y: 30 }"
        :enter="{ opacity: 1, y: 0, transition: { duration: 600, ease: 'easeOut' } }"
      >
        <span class="text-xs font-bold uppercase tracking-widest text-clinicalCyan bg-clinicalCyan/10 px-3 py-1 rounded-full">
          Platform Architecture
        </span>
        <h2 class="text-3xl sm:text-4xl font-extrabold tracking-tight text-clinicalNavy">
          Technological Foundation
        </h2>
        <div class="w-16 h-1 bg-gradient-to-r from-clinicalCyan to-clinicalEmerald mx-auto rounded-full"></div>
        <p class="text-base text-clinicalMuted leading-relaxed">
          Standardizing the radiology workspace through robust enterprise frameworks and proven mathematical algorithms.
        </p>
      </div>

      <!-- Frameworks Subtitle -->
      <div class="mb-8" v-motion :initial="{ opacity: 0 }" :enter="{ opacity: 1, transition: { delay: 200 } }">
        <h3 class="text-xs font-bold uppercase tracking-wider text-clinicalMuted/80 border-b border-clinicalBorder pb-2.5 flex items-center gap-2">
          <span class="w-1.5 h-1.5 rounded-full bg-clinicalCyan"></span> Frameworks & Infrastructure
        </h3>
      </div>

      <!-- Frameworks Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
        <div 
          v-for="(tech, idx) in frameworks" 
          :key="tech.title"
          class="glass-card rounded-xl border border-clinicalBorder p-5 hover:shadow-soft hover:border-clinicalCyan/30 hover:scale-[1.02] transition-all duration-300 group flex flex-col justify-between min-h-[140px]"
          v-motion
          :initial="{ opacity: 0, y: 20 }"
          :enter="{ opacity: 1, y: 0, transition: { duration: 500, delay: idx * 100 } }"
        >
          <div class="flex items-center gap-3">
            <span class="p-2 bg-clinicalCyan/10 text-clinicalCyan rounded-lg group-hover:bg-clinicalCyan group-hover:text-white transition-colors duration-300">
              <component :is="tech.icon" class="w-4.5 h-4.5" />
            </span>
            <h4 class="text-sm font-bold text-clinicalNavy">{{ tech.title }}</h4>
          </div>
          <p class="text-xs text-clinicalMuted leading-relaxed mt-3">
            {{ tech.desc }}
          </p>
        </div>
      </div>

      <!-- Concepts Subtitle -->
      <div class="mb-8" v-motion :initial="{ opacity: 0 }" :enter="{ opacity: 1, transition: { delay: 400 } }">
        <h3 class="text-xs font-bold uppercase tracking-wider text-clinicalMuted/80 border-b border-clinicalBorder pb-2.5 flex items-center gap-2">
          <span class="w-1.5 h-1.5 rounded-full bg-clinicalEmerald"></span> Algorithms & Theoretical Core
        </h3>
      </div>

      <!-- Concepts Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div 
          v-for="(tech, idx) in concepts" 
          :key="tech.title"
          class="glass-card rounded-xl border border-clinicalBorder p-5 hover:shadow-soft hover:border-clinicalEmerald/30 hover:scale-[1.02] transition-all duration-300 group flex flex-col justify-between min-h-[140px]"
          v-motion
          :initial="{ opacity: 0, y: 20 }"
          :enter="{ opacity: 1, y: 0, transition: { duration: 500, delay: 200 + (idx * 100) } }"
        >
          <div class="flex items-center gap-3">
            <span class="p-2 bg-clinicalEmerald/10 text-clinicalEmerald rounded-lg group-hover:bg-clinicalEmerald group-hover:text-white transition-colors duration-300">
              <component :is="tech.icon" class="w-4.5 h-4.5" />
            </span>
            <h4 class="text-sm font-bold text-clinicalNavy">{{ tech.title }}</h4>
          </div>
          <p class="text-xs text-clinicalMuted leading-relaxed mt-3">
            {{ tech.desc }}
          </p>
        </div>
      </div>

    </div>
  </section>
</template>
