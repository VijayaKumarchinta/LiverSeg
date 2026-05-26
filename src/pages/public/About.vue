<script setup>
import { ShieldCheck, Scale, Globe } from 'lucide-vue-next'
</script>

<template>
  <div class="relative bg-slate-50 min-h-[90vh] py-16">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
      
      <!-- HEADER -->
      <div class="text-center max-w-3xl mx-auto mb-16 space-y-4">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-teal-50 border border-teal-100 text-teal-700 text-xs font-semibold uppercase tracking-wider">
          Safety &amp; Compliance
        </div>
        <h1 class="text-3xl sm:text-4xl font-extrabold tracking-tight text-slate-900">
          About LiverSeg AI
        </h1>
        <p class="text-sm text-slate-500 max-w-xl mx-auto leading-relaxed">
          Developing state-of-the-art medical segmentation models while adhering to strict privacy, security, and quality benchmarks.
        </p>
      </div>

      <!-- COMPLIANCE DETAIL CARDS -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
        <div class="bg-white border border-slate-200 p-6 rounded-2xl space-y-4 shadow-sm">
          <div class="w-10 h-10 rounded-xl bg-teal-50 text-teal-600 flex items-center justify-center">
            <ShieldCheck class="w-5 h-5" />
          </div>
          <h3 class="font-bold text-slate-900 text-sm uppercase tracking-wider">HIPAA &amp; GDPR</h3>
          <p class="text-xs text-slate-500 leading-relaxed">
            All volumetric data ingested is processed locally in-browser or on designated local nodes, preserving patient PHI anonymity.
          </p>
        </div>

        <div class="bg-white border border-slate-200 p-6 rounded-2xl space-y-4 shadow-sm">
          <div class="w-10 h-10 rounded-xl bg-teal-50 text-teal-600 flex items-center justify-center">
            <Scale class="w-5 h-5" />
          </div>
          <h3 class="font-bold text-slate-900 text-sm uppercase tracking-wider">Decision Support</h3>
          <p class="text-xs text-slate-500 leading-relaxed">
            This platform acts as a secondary verification tool. All computed volumes and contours must be verified by certified medical practitioners.
          </p>
        </div>

        <div class="bg-white border border-slate-200 p-6 rounded-2xl space-y-4 shadow-sm">
          <div class="w-10 h-10 rounded-xl bg-teal-50 text-teal-600 flex items-center justify-center">
            <Globe class="w-5 h-5" />
          </div>
          <h3 class="font-bold text-slate-900 text-sm uppercase tracking-wider">Clinical Integrity</h3>
          <p class="text-xs text-slate-500 leading-relaxed">
            Partnering with transplant teams and research labs globally to enhance model reliability across varying liver lesions.
          </p>
        </div>
      </div>

    </div>
  </div>
</template>
