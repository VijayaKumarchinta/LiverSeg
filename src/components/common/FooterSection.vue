<script setup>
import { Activity, CheckCircle } from 'lucide-vue-next'
</script>

<template>
  <footer class="relative bg-slate-50 border-t border-slate-200 pt-16 pb-12 overflow-hidden">
    <!-- Subtle clinical background gradient grid -->
    <div class="absolute inset-0 bg-[radial-gradient(#e2e8f0_1px,transparent_1px)] bg-[size:24px_24px] opacity-60 pointer-events-none"></div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
      <div class="grid grid-cols-1 md:grid-cols-12 gap-8 md:gap-12 pb-10 border-b border-slate-200">
        
        <!-- Column 1: Info and Badges -->
        <div class="md:col-span-8 space-y-4">
          <div class="flex items-center gap-2.5">
            <div class="flex items-center justify-center w-9 h-9 rounded-lg bg-gradient-to-tr from-teal-500 to-sky-600 text-white">
              <Activity class="w-5 h-5" />
            </div>
            <span class="text-base font-bold text-slate-900 tracking-tight">
              LiverSeg<span class="text-teal-600">AI</span>
            </span>
          </div>
          
          <p class="text-xs text-slate-500 max-w-sm leading-relaxed">
            Enterprise-grade deep learning solution for automated 3D liver volumetry and lesion boundary outline. Streamlining diagnostic workflows, reducing variability, and assisting clinical transplant evaluations.
          </p>

          <div class="flex items-center gap-2 text-[10px] text-slate-600 font-semibold bg-white border border-slate-200 px-3 py-1.5 rounded-lg w-max shadow-sm">
            <CheckCircle class="w-4 h-4 text-teal-600" />
            <span>HIPAA Compliant &amp; GDPR Data Protection Certified</span>
          </div>
        </div>

        <!-- Column 2: Section Links -->
        <div class="md:col-span-4 space-y-4">
          <h4 class="text-xs font-bold uppercase tracking-wider text-slate-900">Platform Portal</h4>
          <ul class="space-y-2">
            <li><router-link to="/" class="text-xs text-slate-500 hover:text-teal-600 transition-colors">Home</router-link></li>
            <li><router-link to="/platform" class="text-xs text-slate-500 hover:text-teal-600 transition-colors">SaaS Platform</router-link></li>
            <li><router-link to="/research" class="text-xs text-slate-500 hover:text-teal-600 transition-colors">Research &amp; CNN</router-link></li>
            <li><router-link to="/about" class="text-xs text-slate-500 hover:text-teal-600 transition-colors">Safety &amp; About</router-link></li>
          </ul>
        </div>
      </div>

      <!-- Bottom Bar -->
      <div class="pt-8 flex flex-col md:flex-row items-center justify-between gap-4 text-center md:text-left text-[11px] text-slate-400">
        <div>
          &copy; {{ new Date().getFullYear() }} LiverSeg AI Inc. For investigational clinical decision support.
        </div>
        <div class="font-medium">
          Technology Core: 
          <span class="text-slate-600">Vue 3</span> &middot; 
          <span class="text-slate-600">Tailwind CSS</span> &middot; 
          <span class="text-slate-600">MONAI Core</span>
        </div>
      </div>
    </div>
  </footer>
</template>
