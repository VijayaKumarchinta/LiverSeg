<script setup>
import { ref, computed } from 'vue'
import { useAppState } from '../../composables/useAppState'
import { FileText, Printer, Search, CheckCircle2, Download, Shield, BarChart3 } from 'lucide-vue-next'

const { patients } = useAppState()
const activeReportId = ref('PT-2094-A')
const searchVal = ref('')

const completedReports = computed(() =>
  patients.value.filter(p => p.status === 'Completed' &&
    (p.name.toLowerCase().includes(searchVal.value.toLowerCase()) || p.id.toLowerCase().includes(searchVal.value.toLowerCase())))
)

const activeReport = computed(() =>
  patients.value.find(p => p.id === activeReportId.value) || completedReports.value[0]
)

const handlePrint = () => window.print()
</script>

<template>
  <div class="space-y-5 animate-fade-in-up">

    <!-- Header -->
    <div class="frosted-glass-panel p-4 flex items-center justify-between gap-4">
      <div>
        <div class="section-title">Radiology Reporting</div>
        <h2 class="text-sm font-black text-slate-800 mt-0.5">Structured Diagnostic Reports</h2>
        <p class="text-[10px] text-slate-500 font-medium mt-0.5">{{ completedReports.length }} signed reports · EHR and PACS integrated</p>
      </div>
      <div class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-teal-50 border border-teal-100">
        <Shield class="w-3 h-3 text-teal-600" />
        <span class="text-[9px] font-bold text-teal-700">HIPAA Verified</span>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-5">

      <!-- LEFT: Report List -->
      <div class="lg:col-span-4 frosted-glass-panel p-4 space-y-3">
        <div>
          <div class="section-title mb-2">Report Queue</div>
          <div class="relative">
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-400" />
            <input v-model="searchVal" type="text" placeholder="Search signed reports..." class="clinical-input w-full pl-9 pr-3 py-2 text-xs" />
          </div>
        </div>

        <div class="space-y-1.5 max-h-[520px] overflow-y-auto clinical-scrollbar">
          <div
            v-for="rep in completedReports" :key="rep.id"
            @click="activeReportId = rep.id"
            :class="[
              'p-3 rounded-xl border cursor-pointer transition-all',
              activeReportId === rep.id
                ? 'bg-teal-50/70 border-teal-200 shadow-sm'
                : 'border-slate-100/70 hover:bg-white/50 hover:border-slate-200'
            ]"
          >
            <div class="flex items-start justify-between gap-2">
              <div class="min-w-0">
                <div class="text-[10px] font-black text-slate-800 truncate">{{ rep.name }}</div>
                <div class="font-mono text-[8px] text-slate-400 font-bold mt-0.5">{{ rep.id }}</div>
              </div>
              <CheckCircle2 class="w-3.5 h-3.5 text-teal-500 flex-shrink-0 mt-0.5" />
            </div>
            <div class="flex items-center justify-between mt-2 text-[9px] font-bold">
              <span class="text-slate-400">{{ rep.scanDate.substring(0,10) }}</span>
              <span class="text-teal-600">{{ rep.metrics.dice }}</span>
            </div>
            <div class="mt-1.5 flex items-center gap-1.5">
              <span v-if="rep.hasLesions" class="text-[8px] font-bold text-rose-500 bg-rose-50 border border-rose-100 px-1.5 py-0.5 rounded-full">Lesion</span>
              <span class="text-[8px] font-bold text-slate-500 bg-slate-100 px-1.5 py-0.5 rounded-full">{{ rep.metrics.volume }}</span>
            </div>
          </div>

          <div v-if="completedReports.length === 0" class="py-8 text-center">
            <FileText class="w-6 h-6 text-slate-300 mx-auto mb-2" />
            <div class="text-xs text-slate-400 font-medium">No reports found</div>
          </div>
        </div>
      </div>

      <!-- RIGHT: Report Sheet -->
      <div class="lg:col-span-8 frosted-glass-panel p-6 space-y-6" id="report-sheet">
        <div v-if="activeReport">

          <!-- Sheet Header -->
          <div class="flex items-start justify-between pb-5 border-b border-slate-200/60">
            <div class="space-y-1">
              <div class="section-title text-teal-600">Clinical Diagnosis Report · LiversegAI</div>
              <h2 class="text-lg font-black text-slate-900">Hepatic Volumetric Segmentation Report</h2>
              <div class="text-[10px] text-slate-400 font-bold font-mono">Document ID: SR-{{ activeReport.id }} · DICOM SR Standard</div>
            </div>
            <div class="flex items-center gap-2 no-print">
              <button @click="handlePrint" class="clinical-btn-secondary flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-bold active-shrink">
                <Download class="w-3.5 h-3.5" /> Export PDF
              </button>
            </div>
          </div>

          <!-- Demographics -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 py-4 border-b border-slate-200/50">
            <div v-for="(val, label) in {
              'Patient Name': activeReport.name,
              'Case Reference': activeReport.id,
              'Demographics': activeReport.gender + ', ' + activeReport.age + 'y',
              'Acquisition Date': activeReport.scanDate
            }" :key="label">
              <div class="section-title mb-1">{{ label }}</div>
              <div class="text-xs font-bold text-slate-800">{{ val }}</div>
            </div>
          </div>

          <!-- Quantitative Metrics -->
          <div class="space-y-3">
            <div class="section-title">1. Quantitative AI Segmentation Metrics</div>
            <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
              <div v-for="(val, label) in {
                'Liver Volume': activeReport.metrics.volume,
                'Dice Score': activeReport.metrics.dice,
                'IoU Score': activeReport.metrics.iou,
                'Precision': activeReport.metrics.precision,
                'Recall': activeReport.metrics.recall,
                'AI Confidence': activeReport.metrics.confidence,
              }" :key="label"
                class="bg-white/60 border border-slate-200/60 p-3 rounded-xl shadow-sm"
              >
                <div class="section-title mb-1">{{ label }}</div>
                <div class="text-sm font-black text-slate-800" :class="label === 'Dice Score' ? 'text-teal-600' : ''">{{ val }}</div>
              </div>
            </div>

            <!-- Lesion Card -->
            <div :class="['p-3 rounded-xl border', activeReport.hasLesions ? 'bg-rose-50/60 border-rose-100' : 'bg-slate-50/60 border-slate-200/40']">
              <div class="section-title mb-1" :class="activeReport.hasLesions ? 'text-rose-600' : ''">Lesion Volume</div>
              <div class="text-lg font-black" :class="activeReport.hasLesions ? 'text-rose-700' : 'text-slate-600'">
                {{ activeReport.lesionVolume }}
              </div>
              <div class="text-[9px] font-medium mt-1" :class="activeReport.hasLesions ? 'text-rose-500' : 'text-slate-400'">
                {{ activeReport.hasLesions ? 'Focal lesion detected — correlate clinically' : 'No significant focal lesions' }}
              </div>
            </div>
          </div>

          <!-- Clinical Findings -->
          <div class="space-y-2 pt-4 border-t border-slate-200/50">
            <div class="section-title">2. Radiologist Diagnostic Findings</div>
            <div class="bg-white/60 border border-slate-200/60 p-4 rounded-xl text-xs text-slate-600 font-medium leading-relaxed">
              {{ activeReport.findings }}
            </div>
          </div>

          <!-- Signature -->
          <div class="pt-4 border-t border-slate-200/50 flex items-end justify-between">
            <div class="space-y-1">
              <div class="section-title">Authorized Radiologist Signature</div>
              <div class="font-serif italic text-base font-bold text-slate-800">
                {{ activeReport.signature || 'Pending Radiologist Signature' }}
              </div>
              <div class="text-[9px] text-slate-400 font-medium">Electronically validated · HSM digital certificate · HIPAA audit trail</div>
            </div>
            <div class="flex items-center gap-1.5 bg-teal-50 border border-teal-100 px-3 py-2 rounded-xl">
              <CheckCircle2 class="w-4 h-4 text-teal-600" />
              <div>
                <div class="text-[9px] font-black text-teal-700">HIPAA Verified</div>
                <div class="text-[8px] text-teal-600 font-medium">Audit trail active</div>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="py-20 text-center">
          <FileText class="w-8 h-8 text-slate-300 mx-auto mb-3" />
          <div class="text-sm font-bold text-slate-500">No report selected</div>
          <div class="text-xs text-slate-400 font-medium mt-1">Select a signed report from the list</div>
        </div>
      </div>
    </div>
  </div>
</template>
