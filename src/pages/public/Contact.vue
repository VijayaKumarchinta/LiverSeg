<script setup>
import { Mail, Phone, MapPin, Send } from 'lucide-vue-next'
</script>

<template>
  <div class="relative bg-white min-h-[90vh] py-16">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
      
      <!-- HEADER -->
      <div class="text-center max-w-3xl mx-auto mb-16 space-y-4">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-teal-50 border border-teal-100 text-teal-700 text-xs font-semibold uppercase tracking-wider">
          Contact Us
        </div>
        <h1 class="text-3xl sm:text-4xl font-extrabold tracking-tight text-slate-900">
          Get in Touch
        </h1>
        <p class="text-sm text-slate-500 max-w-xl mx-auto leading-relaxed">
          Need custom deployment settings or details on network validation weights? Our engineering team is here to assist.
        </p>
      </div>

      <!-- GRID -->
      <div class="grid grid-cols-1 md:grid-cols-12 gap-12 max-w-5xl mx-auto">
        <!-- Details -->
        <div class="md:col-span-5 space-y-6">
          <h2 class="text-lg font-bold text-slate-900">Hospital Support Desk</h2>
          <p class="text-xs text-slate-500 leading-relaxed">
            We provide remote installation packages, custom PACS router scripting, and standard DICOM mapping checklists.
          </p>

          <div class="space-y-4">
            <div class="flex items-center gap-3 text-xs">
              <Mail class="w-4 h-4 text-teal-600" />
              <span class="text-slate-655 text-slate-600">institutional-support@liverseg.ai</span>
            </div>
            <div class="flex items-center gap-3 text-xs">
              <Phone class="w-4 h-4 text-teal-600" />
              <span class="text-slate-655 text-slate-600">+1 (800) 555-LIVER</span>
            </div>
            <div class="flex items-start gap-3 text-xs">
              <MapPin class="w-4 h-4 text-teal-600 mt-0.5" />
              <span class="text-slate-655 text-slate-600">Medical Systems Division<br />Bio-Innovation Hub, Suite 305</span>
            </div>
          </div>
        </div>

        <!-- Form -->
        <div class="md:col-span-7 bg-slate-50 border border-slate-200 rounded-2xl p-6">
          <form class="space-y-4" @submit.prevent>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-[10px] font-bold uppercase tracking-wider text-slate-600 mb-1.5">First Name</label>
                <input type="text" class="w-full bg-white border border-slate-200 rounded-lg px-3 py-2 text-xs focus:outline-none focus:border-teal-500" />
              </div>
              <div>
                <label class="block text-[10px] font-bold uppercase tracking-wider text-slate-600 mb-1.5">Email</label>
                <input type="email" class="w-full bg-white border border-slate-200 rounded-lg px-3 py-2 text-xs focus:outline-none focus:border-teal-500" />
              </div>
            </div>
            <div>
              <label class="block text-[10px] font-bold uppercase tracking-wider text-slate-600 mb-1.5">Hospital / Organization</label>
              <input type="text" class="w-full bg-white border border-slate-200 rounded-lg px-3 py-2 text-xs focus:outline-none focus:border-teal-500" />
            </div>
            <div>
              <label class="block text-[10px] font-bold uppercase tracking-wider text-slate-600 mb-1.5">Message</label>
              <textarea rows="4" class="w-full bg-white border border-slate-200 rounded-lg p-3 text-xs focus:outline-none focus:border-teal-500"></textarea>
            </div>
            <button type="submit" class="flex items-center justify-center gap-2 w-full py-2.5 bg-teal-600 hover:bg-teal-700 text-white rounded-lg text-xs font-semibold uppercase tracking-wider">
              Send Message
              <Send class="w-3.5 h-3.5" />
            </button>
          </form>
        </div>
      </div>

    </div>
  </div>
</template>
