<script setup>
import { ShieldCheck, Scale, Globe } from 'lucide-vue-next'
</script>

<template>
  <div class="relative min-h-[90vh] py-24 clinical-workspace">
    <!-- Immersive clinical glow backdrops -->
    <div class="absolute top-[10%] right-[15%] w-[400px] h-[400px] bg-teal-500/5 rounded-full blur-[100px] pointer-events-none"></div>
    
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
      
      <!-- HEADER -->
      <div class="text-center max-w-3xl mx-auto mb-16 space-y-4">
        <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/80 border border-teal-200/50 text-teal-700 text-xs font-bold uppercase tracking-wider backdrop-blur-sm shadow-sm">
          Safety &amp; Compliance
        </div>
        <h1 class="text-3xl sm:text-4xl font-black tracking-tight text-slate-900">
          About LiverSeg AI
        </h1>
        <p class="text-sm text-slate-500 max-w-xl mx-auto leading-relaxed font-semibold">
          Developing state-of-the-art medical segmentation models while adhering to strict privacy and quality benchmarks.
        </p>
      </div>

      <!-- COMPLIANCE DETAIL CARDS -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
        <div class="frosted-glass-panel p-6 space-y-4 hover:border-teal-500/30 hover:shadow-md transition-all duration-300">
          <div class="w-10 h-10 rounded-xl bg-teal-50 text-teal-600 flex items-center justify-center shadow-sm">
            <ShieldCheck class="w-5 h-5" />
          </div>
          <h3 class="font-bold text-slate-900 text-sm uppercase tracking-wider">HIPAA &amp; GDPR</h3>
          <p class="text-xs text-slate-500 leading-relaxed font-semibold">
            All volumetric data ingested is processed locally in-browser or on designated local nodes, preserving patient PHI anonymity.
          </p>
        </div>

        <div class="frosted-glass-panel p-6 space-y-4 hover:border-teal-500/30 hover:shadow-md transition-all duration-300">
          <div class="w-10 h-10 rounded-xl bg-teal-50 text-teal-600 flex items-center justify-center shadow-sm">
            <Scale class="w-5 h-5" />
          </div>
          <h3 class="font-bold text-slate-900 text-sm uppercase tracking-wider">Decision Support</h3>
          <p class="text-xs text-slate-500 leading-relaxed font-semibold">
            This platform acts as a secondary verification tool. All computed volumes and contours must be verified by certified medical practitioners.
          </p>
        </div>

        <div class="frosted-glass-panel p-6 space-y-4 hover:border-teal-500/30 hover:shadow-md transition-all duration-300">
          <div class="w-10 h-10 rounded-xl bg-teal-50 text-teal-600 flex items-center justify-center shadow-sm">
            <Globe class="w-5 h-5" />
          </div>
          <h3 class="font-bold text-slate-900 text-sm uppercase tracking-wider">Clinical Integrity</h3>
          <p class="text-xs text-slate-500 leading-relaxed font-semibold">
            Partnering with transplant teams and research labs globally to enhance model reliability across varying liver lesions.
          </p>
        </div>
      </div>

    </div>
  </div>
</template>
