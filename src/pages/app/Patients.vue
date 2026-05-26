<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAppState } from '../../composables/useAppState'
import {
  Search, FolderOpen, ArrowRight, CheckCircle2, Loader2,
  Clock, AlertTriangle, ScanLine, Calendar, User, Filter
} from 'lucide-vue-next'

const router = useRouter()
const { patients, selectPatient } = useAppState()

const searchVal = ref('')
const activeFilter = ref('all')

const filters = ['all', 'Completed', 'Analyzing', 'Ready']

const filteredPatients = computed(() => {
  let list = patients.value
  if (searchVal.value) {
    const q = searchVal.value.toLowerCase()
    list = list.filter(p => p.name.toLowerCase().includes(q) || p.id.toLowerCase().includes(q) || p.modality.toLowerCase().includes(q))
  }
  if (activeFilter.value !== 'all') list = list.filter(p => p.status === activeFilter.value)
  return list
})

const statusClass = (status) => ({
  Completed: 'badge-completed',
  Analyzing: 'badge-analyzing',
  Ready:     'badge-pending',
}[status] || 'badge-pending')

const statusIcon = (status) => ({ Completed: CheckCircle2, Analyzing: Loader2, Ready: Clock }[status] || Clock)

const handleOpenWorkspace = (p) => {
  selectPatient(p.id)
  router.push('/app/analysis')
}
</script>

<template>
  <div class="space-y-5 animate-fade-in-up">

    <!-- Header -->
    <div class="frosted-glass-panel p-4 flex flex-wrap items-center justify-between gap-4">
      <div>
        <div class="section-title">Patient Management</div>
        <h2 class="text-sm font-black text-slate-800 mt-0.5">PACS Patient Records Directory</h2>
        <p class="text-[10px] text-slate-500 font-medium mt-0.5">{{ patients.length }} cases in local PACS cache · Real-time sync active</p>
      </div>

      <div class="flex items-center gap-3">
        <!-- Search -->
        <div class="relative">
          <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-400" />
          <input
            v-model="searchVal"
            type="text"
            placeholder="Search by name, MRN, or modality..."
            class="clinical-input pl-9 pr-4 py-2 text-xs w-64"
          />
        </div>

        <!-- Filter tabs -->
        <div class="flex items-center bg-slate-100/70 rounded-lg p-0.5 border border-slate-200/60">
          <button
            v-for="f in filters" :key="f"
            @click="activeFilter = f"
            :class="[
              'px-2.5 py-1 rounded-md text-[9px] font-bold transition-all capitalize',
              activeFilter === f ? 'bg-white text-teal-700 shadow-sm border border-slate-200/60' : 'text-slate-500 hover:text-slate-700'
            ]"
          >{{ f }}</button>
        </div>
      </div>
    </div>

    <!-- Results count -->
    <div class="text-[10px] text-slate-400 font-semibold">
      Showing {{ filteredPatients.length }} of {{ patients.length }} cases
    </div>

    <!-- Patient Cards Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
      <div
        v-for="p in filteredPatients"
        :key="p.id"
        class="frosted-glass-panel p-5 flex flex-col justify-between group"
      >
        <!-- Card Top -->
        <div class="space-y-4">
          <div class="flex items-start justify-between">
            <div class="min-w-0 flex-1">
              <h3 class="text-sm font-black text-slate-800 truncate group-hover:text-teal-700 transition-colors">{{ p.name }}</h3>
              <div class="font-mono text-[9px] text-slate-400 font-bold mt-0.5">{{ p.id }}</div>
            </div>
            <span :class="['inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[8px] font-bold ml-2 flex-shrink-0', statusClass(p.status)]">
              <component :is="statusIcon(p.status)" :class="['w-2.5 h-2.5', p.status==='Analyzing'?'animate-spin':'']" />
              {{ p.status }}
            </span>
          </div>

          <!-- Details grid -->
          <div class="grid grid-cols-2 gap-x-4 gap-y-2.5 text-[10px] font-medium">
            <div>
              <div class="section-title mb-0.5">Age / Sex</div>
              <div class="font-bold text-slate-700">{{ p.age }}y · {{ p.gender }}</div>
            </div>
            <div>
              <div class="section-title mb-0.5">Date of Birth</div>
              <div class="font-bold text-slate-700">{{ p.dob }}</div>
            </div>
            <div class="col-span-2">
              <div class="section-title mb-0.5">Modality</div>
              <div class="font-bold text-slate-700">{{ p.modality }}</div>
            </div>
            <div class="col-span-2">
              <div class="section-title mb-0.5">Scan Date</div>
              <div class="font-bold text-slate-700">{{ p.scanDate }}</div>
            </div>
          </div>

          <!-- Metrics (if completed) -->
          <div v-if="p.status === 'Completed'" class="grid grid-cols-3 gap-2">
            <div class="text-center bg-teal-50/60 border border-teal-100/60 rounded-lg p-1.5">
              <div class="text-[8px] font-bold text-teal-600 uppercase">Dice</div>
              <div class="text-xs font-black text-teal-700">{{ p.metrics.dice }}</div>
            </div>
            <div class="text-center bg-slate-50/60 border border-slate-200/40 rounded-lg p-1.5">
              <div class="text-[8px] font-bold text-slate-400 uppercase">Volume</div>
              <div class="text-[10px] font-black text-slate-700">{{ p.metrics.volume }}</div>
            </div>
            <div class="text-center rounded-lg p-1.5" :class="p.hasLesions ? 'bg-rose-50/60 border border-rose-100/60' : 'bg-slate-50/60 border border-slate-200/40'">
              <div class="text-[8px] font-bold uppercase" :class="p.hasLesions ? 'text-rose-500' : 'text-slate-400'">Lesion</div>
              <div class="text-[10px] font-black" :class="p.hasLesions ? 'text-rose-600' : 'text-slate-500'">{{ p.lesionVolume }}</div>
            </div>
          </div>
        </div>

        <!-- Card Footer -->
        <div class="mt-4 pt-4 border-t border-slate-200/50 flex items-center justify-between">
          <div class="text-[9px] text-slate-400 font-semibold">
            <span v-if="p.hasLesions" class="text-rose-500 font-bold">⚠ Lesion detected</span>
            <span v-else-if="p.status === 'Completed'" class="text-teal-600 font-bold">✓ Normal findings</span>
            <span v-else>Awaiting analysis</span>
          </div>
          <button
            @click="handleOpenWorkspace(p)"
            class="clinical-btn-primary flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-[9px] font-bold active-shrink"
          >
            Workspace <ArrowRight class="w-3 h-3" />
          </button>
        </div>
      </div>

      <!-- Empty state -->
      <div v-if="filteredPatients.length === 0" class="col-span-full frosted-glass-panel p-12 text-center">
        <FolderOpen class="w-8 h-8 text-slate-300 mx-auto mb-3" />
        <div class="text-sm font-bold text-slate-500">No patients match your search</div>
        <div class="text-xs text-slate-400 font-medium mt-1">Try a different filter or search term</div>
      </div>
    </div>
  </div>
</template>
