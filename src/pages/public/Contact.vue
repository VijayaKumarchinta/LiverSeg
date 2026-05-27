<script setup>
import { Send, MapPin, Mail, PhoneCall } from 'lucide-vue-next'
</script>

<template>
  <div class="relative min-h-[90vh] py-24 clinical-workspace">
    <!-- Immersive clinical glow backdrops -->
    <div class="absolute top-[15%] right-[10%] w-[450px] h-[450px] bg-teal-500/5 rounded-full blur-[100px] pointer-events-none"></div>
    <div class="absolute bottom-[10%] left-[10%] w-[400px] h-[400px] bg-sky-500/5 rounded-full blur-[100px] pointer-events-none"></div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
      
      <!-- HEADER -->
      <div class="text-center max-w-3xl mx-auto mb-16 space-y-4">
        <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/80 border border-teal-200/50 text-teal-700 text-xs font-bold uppercase tracking-wider backdrop-blur-sm shadow-sm">
          Contact Us
        </div>
        <h1 class="text-3xl sm:text-4xl font-black tracking-tight text-slate-900">
          Get in Touch
        </h1>
        <p class="text-sm text-slate-500 max-w-xl mx-auto leading-relaxed font-semibold">
          Need custom deployment settings or details on network validation weights? Our engineering team is here to assist.
        </p>
      </div>

      <!-- GRID -->
      <div class="grid grid-cols-1 md:grid-cols-12 gap-12 max-w-5xl mx-auto">
        <!-- Details -->
        <div class="md:col-span-5 space-y-8 flex flex-col justify-center">
          <div class="space-y-3">
            <h2 class="text-xl font-black text-slate-800">Hospital Support Desk</h2>
            <p class="text-xs text-slate-500 leading-relaxed font-semibold">
              We provide remote installation packages, custom PACS router scripting, and standard DICOM mapping checklists.
            </p>
          </div>

          <div class="space-y-4 text-xs font-semibold text-slate-650 text-slate-600">
            <div class="flex items-center gap-3.5">
              <div class="w-9 h-9 rounded-xl bg-teal-50 text-teal-650 flex items-center justify-center border border-teal-100 shadow-sm">
                <MapPin class="w-4 h-4" />
              </div>
              <div>
                <p class="text-[9px] font-bold uppercase text-slate-400">Location</p>
                <p class="text-slate-800 font-bold">Medical Center Innovation Hub, SF</p>
              </div>
            </div>
            <div class="flex items-center gap-3.5">
              <div class="w-9 h-9 rounded-xl bg-teal-50 text-teal-650 flex items-center justify-center border border-teal-100 shadow-sm">
                <Mail class="w-4 h-4" />
              </div>
              <div>
                <p class="text-[9px] font-bold uppercase text-slate-400">Email</p>
                <p class="text-slate-800 font-bold">support@liverseg.ai</p>
              </div>
            </div>
            <div class="flex items-center gap-3.5">
              <div class="w-9 h-9 rounded-xl bg-teal-50 text-teal-650 flex items-center justify-center border border-teal-100 shadow-sm">
                <PhoneCall class="w-4 h-4" />
              </div>
              <div>
                <p class="text-[9px] font-bold uppercase text-slate-400">Phone</p>
                <p class="text-slate-800 font-bold">+1 (800) 555-LIVER</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Form -->
        <div class="md:col-span-7 frosted-glass-panel p-6 sm:p-8">
          <form class="space-y-4" @submit.prevent>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-[9px] font-bold uppercase tracking-wider text-slate-500 mb-1.5">First Name</label>
                <input type="text" placeholder="John" class="w-full clinical-input px-3.5 py-2 text-xs font-semibold" />
              </div>
              <div>
                <label class="block text-[9px] font-bold uppercase tracking-wider text-slate-500 mb-1.5">Email</label>
                <input type="email" placeholder="john@hospital.org" class="w-full clinical-input px-3.5 py-2 text-xs font-semibold" />
              </div>
            </div>
            <div>
              <label class="block text-[9px] font-bold uppercase tracking-wider text-slate-500 mb-1.5">Hospital / Organization</label>
              <input type="text" placeholder="Mayo Clinic" class="w-full clinical-input px-3.5 py-2 text-xs font-semibold" />
            </div>
            <div>
              <label class="block text-[9px] font-bold uppercase tracking-wider text-slate-500 mb-1.5">Message</label>
              <textarea rows="4" placeholder="How can we assist your clinical imaging pipeline?" class="w-full clinical-input p-3 text-xs font-semibold"></textarea>
            </div>
            <button type="submit" class="flex items-center justify-center gap-2 w-full py-3.5 text-xs font-bold uppercase tracking-wider rounded-xl clinical-btn-primary active-shrink">
              Send Message
              <Send class="w-3.5 h-3.5" />
            </button>
          </form>
        </div>
      </div>

    </div>
  </div>
</template>
