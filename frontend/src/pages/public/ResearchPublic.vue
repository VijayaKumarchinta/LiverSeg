<script setup>
import { Activity, ShieldCheck, Cpu, Code, Brain } from 'lucide-vue-next'

const cnnStats = [
  { label: "Dice Similarity Coefficient", val: "95.8%" },
  { label: "Mean Intersection over Union", val: "91.2%" },
  { label: "Average Inference Latency", val: "3.24s" },
  { label: "Training Epochs", val: "250 Epochs" }
]
</script>

<template>
  <div class="relative bg-white min-h-[90vh] py-16">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
      
      <!-- HEADER -->
      <div class="text-center max-w-3xl mx-auto mb-16 space-y-4">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-teal-50 border border-teal-100 text-teal-700 text-xs font-semibold uppercase tracking-wider">
          Neural Architecture
        </div>
        <h1 class="text-3xl sm:text-4xl font-extrabold tracking-tight text-slate-900">
          Convolutional Neural Network Design
        </h1>
        <p class="text-sm text-slate-500 max-w-xl mx-auto leading-relaxed">
          Powered by a deep 3D Attention U-Net trained on clinical abdominal cohorts to deliver pixel-level segmentation boundaries.
        </p>
      </div>

      <!-- GRID INFO -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 items-start mb-16">
        
        <!-- Deep model specs -->
        <div class="lg:col-span-7 space-y-6">
          <h2 class="text-xl font-bold text-slate-900">Model Architectural Features</h2>
          <div class="space-y-4">
            <div class="p-4 border border-slate-200 rounded-xl bg-slate-50 flex gap-3">
              <Brain class="w-5 h-5 text-teal-600 mt-0.5 flex-shrink-0" />
              <div>
                <h4 class="font-bold text-slate-800 text-xs uppercase tracking-wider">Attention Gating Modules</h4>
                <p class="text-xs text-slate-500 mt-1 leading-relaxed">
                  Suppress background regions like the kidneys and spleen, directing the network to focus on liver parenchyma edges.
                </p>
              </div>
            </div>

            <div class="p-4 border border-slate-200 rounded-xl bg-slate-50 flex gap-3">
              <Cpu class="w-5 h-5 text-teal-600 mt-0.5 flex-shrink-0" />
              <div>
                <h4 class="font-bold text-slate-800 text-xs uppercase tracking-wider">Residual Skip Connections</h4>
                <p class="text-xs text-slate-500 mt-1 leading-relaxed">
                  Mitigate vanishing gradients, ensuring fine boundaries and voxel contours are preserved throughout deep spatial contractions.
                </p>
              </div>
            </div>

            <div class="p-4 border border-slate-200 rounded-xl bg-slate-50 flex gap-3">
              <Code class="w-5 h-5 text-teal-600 mt-0.5 flex-shrink-0" />
              <div>
                <h4 class="font-bold text-slate-800 text-xs uppercase tracking-wider">Hybrid Loss Minimization</h4>
                <p class="text-xs text-slate-500 mt-1 leading-relaxed">
                  Optimized using a combo Dice and Binary Cross Entropy (BCE) loss to handle highly unbalanced segmentations.
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Metric Table Cards -->
        <div class="lg:col-span-5 bg-slate-50 border border-slate-200 rounded-2xl p-6 space-y-6">
          <h3 class="font-bold text-slate-900 text-sm uppercase tracking-wider">Benchmark Metrics</h3>
          <div class="divide-y divide-slate-200">
            <div 
              v-for="(stat, idx) in cnnStats" 
              :key="idx" 
              class="flex justify-between py-3 text-xs"
            >
              <span class="text-slate-500">{{ stat.label }}</span>
              <span class="font-bold text-slate-900">{{ stat.val }}</span>
            </div>
          </div>
          <div class="text-[10px] text-slate-400 text-center leading-relaxed">
            *Validated on the LiTS (Liver Tumor Segmentation) Benchmark Dataset and local clinical test queues.
          </div>
        </div>
      </div>

    </div>
  </div>
</template>
