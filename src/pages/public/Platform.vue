<script setup>
import { Activity, ShieldCheck, Cpu, HardDrive, CheckCircle2, Clipboard, ArrowRight } from 'lucide-vue-next'

const pipelineSteps = [
  {
    title: "1. Multi-Format Ingestion",
    desc: "Drag and drop DICOM (.dcm) folder structures, NIfTI volumes (.nii/.nii.gz), or clinical diagnostic PDF files directly into the web console. Automated header parser registers patient IDs instantly.",
    icon: HardDrive
  },
  {
    title: "2. Preprocessing & Windowing",
    desc: "Scans are resampled to isotropic 1mm spacing and scaled using target Hounsfield Unit (HU) windows optimized for liver parenchyma tissue density visualization.",
    icon: Cpu
  },
  {
    title: "3. Deep CNN Inference",
    desc: "A pre-trained Attention U-Net segments the liver and separates tissue nodules. Evaluates 20 axial slice layers in milliseconds with automated volumetric computations.",
    icon: Activity
  },
  {
    title: "4. Verification & Signing",
    desc: "Radiologists scroll through axial slices, toggling overlay contours, reviewing automatic volume computations, filling out the diagnostic checklist, and signing reports with PACS export capabilities.",
    icon: Clipboard
  }
]
</script>

<template>
  <div class="relative min-h-[90vh] py-24 clinical-futuristic-bg">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
      
      <!-- HEADER -->
      <div class="text-center max-w-3xl mx-auto mb-16 space-y-4">
        <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/80 border border-teal-200/50 text-teal-700 text-xs font-bold uppercase tracking-wider backdrop-blur-sm shadow-sm">
          Workstation Overview
        </div>
        <h1 class="text-3xl sm:text-4xl font-extrabold tracking-tight text-slate-900">
          The LiverSeg AI Workflow
        </h1>
        <p class="text-sm sm:text-base text-slate-500 max-w-xl mx-auto leading-relaxed">
          From DICOM ingestion to structured report verification, discover the pipeline behind automated medical liver volumetry.
        </p>
      </div>

      <!-- PIPELINE PIPELINE -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-16">
        <div 
          v-for="(step, idx) in pipelineSteps" 
          :key="idx" 
          class="frosted-glass-panel p-7 flex gap-4 hover:border-teal-500/30 duration-300"
        >
          <div class="w-10 h-10 rounded-xl bg-teal-50 text-teal-600 flex items-center justify-center flex-shrink-0 shadow-sm">
            <component :is="step.icon" class="w-5 h-5" />
          </div>
          <div class="space-y-2">
            <h3 class="font-bold text-slate-900 text-base leading-snug tracking-tight">{{ step.title }}</h3>
            <p class="text-xs text-slate-500 leading-relaxed font-semibold">{{ step.desc }}</p>
          </div>
        </div>
      </div>

      <!-- BOTTOM BANNER -->
      <div class="frosted-glass-panel p-8 md:p-12 text-center max-w-4xl mx-auto space-y-6 relative overflow-hidden">
        <div class="absolute top-[-50px] right-[-50px] w-48 h-48 bg-teal-50/50 rounded-full blur-3xl pointer-events-none"></div>
        
        <h2 class="text-2xl font-bold text-slate-900 tracking-tight">Ready to test the workstation?</h2>
        <p class="text-xs text-slate-500 max-w-lg mx-auto leading-relaxed font-semibold">
          Access our secure radiology sandbox. No software installation or local server configuration is required for evaluation.
        </p>
        
        <div class="flex justify-center gap-4">
          <router-link 
            to="/app/upload" 
            class="flex items-center gap-2 px-6 py-3.5 text-xs font-semibold uppercase tracking-wider rounded-xl clinical-btn-primary active-shrink"
          >
            Launch Upload Sandbox
            <ArrowRight class="w-3.5 h-3.5" />
          </router-link>
        </div>
      </div>

    </div>
  </div>
</template>
