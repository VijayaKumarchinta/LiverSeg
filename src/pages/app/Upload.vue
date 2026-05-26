<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAppState } from '../../composables/useAppState'
import {
  UploadCloud, FileText, CheckCircle2, Loader2, AlertCircle,
  X, ShieldCheck, ChevronRight, File, Database, Zap
} from 'lucide-vue-next'

const router = useRouter()
const { uploadQueue, simulateUpload, patients } = useAppState()

const isDragging = ref(false)
const patientName = ref('')
const patientDob = ref('')
const patientGender = ref('Male')
const modality = ref('CT Abdomen (Portal Venous)')

const handleDragOver = (e) => { e.preventDefault(); isDragging.value = true }
const handleDragLeave = () => { isDragging.value = false }
const handleDrop = (e) => { e.preventDefault(); isDragging.value = false; processFiles(e.dataTransfer.files) }
const handleFileSelect = (e) => processFiles(e.target.files)

const processFiles = (files) => {
  for (const file of files) {
    const ext = file.name.split('.').pop().toLowerCase()
    let type = 'unknown'
    if (ext === 'dcm') type = 'dicom'
    else if (ext === 'nii' || file.name.endsWith('.nii.gz')) type = 'nifti'
    else if (ext === 'pdf') type = 'pdf'
    if (type === 'unknown') { alert(`Format .${ext} not supported.`); continue }
    simulateUpload(file.name, (file.size / 1048576).toFixed(1) + ' MB', type)
  }
}

const validationChecks = computed(() => [
  { label: '(0010,0010) PatientName',    pass: true  },
  { label: '(0010,0020) PatientID',      pass: true  },
  { label: '(0008,0060) Modality',       pass: true  },
  { label: '(0018,0050) SliceThickness', pass: true  },
  { label: '(0028,0030) PixelSpacing',   pass: true  },
  { label: '(0008,0022) AcquisitionDate',pass: true  },
])

const pipelineSteps = [
  { step: 'DICOM Header Parse',     status: 'done',    desc: 'Tag validation complete' },
  { step: 'Isotropic Resampling',   status: 'done',    desc: '1mm³ voxel normalization' },
  { step: 'HU Windowing',           status: 'done',    desc: 'Window [-100, 400] HU' },
  { step: 'AI Segmentation Queue',  status: 'pending', desc: 'Awaiting GPU slot' },
  { step: 'Post-processing',        status: 'pending', desc: 'Morphological cleaning' },
  { step: 'PACS Export',            status: 'pending', desc: 'DICOM SR generation' },
]

const completedUploads = computed(() => uploadQueue.value.filter(u => u.status === 'completed'))
const activeUploads = computed(() => uploadQueue.value.filter(u => u.status === 'uploading'))

const typeIcon = (type) => ({ dicom: '🔬', nifti: '🧠', pdf: '📄' }[type] || '📁')
const typeLabel = (type) => ({ dicom: 'DICOM', nifti: 'NIfTI', pdf: 'PDF' }[type] || type)
</script>

<template>
  <div class="space-y-5 animate-fade-in-up">

    <!-- Header -->
    <div class="frosted-glass-panel p-4 flex flex-wrap items-center justify-between gap-4">
      <div>
        <div class="section-title">Imaging Ingest</div>
        <h2 class="text-sm font-black text-slate-800 mt-0.5">Upload & Preprocessing Workspace</h2>
        <p class="text-[10px] text-slate-500 font-medium mt-0.5">Upload DICOM, NIfTI, or PDF imaging files for AI processing</p>
      </div>
      <button @click="router.push('/app/analysis')" class="clinical-btn-secondary flex items-center gap-2 px-3 py-2 rounded-xl text-xs font-bold active-shrink">
        Open Analysis Workspace <ChevronRight class="w-3.5 h-3.5" />
      </button>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-5">

      <!-- LEFT: Upload + Patient Metadata -->
      <div class="lg:col-span-4 space-y-4">

        <!-- Drop Zone -->
        <div class="frosted-glass-panel p-5 space-y-4">
          <div class="section-title flex items-center gap-1.5"><UploadCloud class="w-3.5 h-3.5" /> Upload Files</div>

          <div
            @dragover="handleDragOver" @dragleave="handleDragLeave" @drop="handleDrop"
            :class="[
              'border-2 border-dashed rounded-xl p-8 flex flex-col items-center justify-center gap-3 text-center transition-all cursor-pointer',
              isDragging ? 'border-teal-400 bg-teal-50/40 scale-[1.01]' : 'border-slate-200 bg-white/30 hover:border-teal-300 hover:bg-teal-50/20'
            ]"
          >
            <input id="file-upload" type="file" class="hidden" multiple accept=".dcm,.nii,.nii.gz,.pdf" @change="handleFileSelect" />
            <label for="file-upload" class="cursor-pointer">
              <div class="w-12 h-12 rounded-full bg-teal-50 border border-teal-100 flex items-center justify-center mx-auto mb-2">
                <UploadCloud class="w-5 h-5 text-teal-600" />
              </div>
              <div class="text-xs font-bold text-slate-700">Drag & drop imaging files</div>
              <div class="text-[10px] text-slate-400 font-medium mt-1">or <span class="text-teal-600 font-bold">click to browse</span></div>
              <div class="text-[9px] text-slate-400 font-bold mt-2 bg-slate-50 border border-slate-200/60 px-3 py-1 rounded-full">
                DICOM (.dcm) · NIfTI (.nii/.nii.gz) · PDF
              </div>
            </label>
          </div>

          <!-- Quick test buttons -->
          <div class="flex gap-2">
            <button @click="simulateUpload('CT_Liver_Portal.nii.gz','48.2 MB','nifti')"
              class="clinical-btn-secondary flex-1 py-1.5 rounded-lg text-[9px] font-bold active-shrink">+ NIfTI</button>
            <button @click="simulateUpload('CT_ABDOMEN_CASE.dcm','84.1 MB','dicom')"
              class="clinical-btn-secondary flex-1 py-1.5 rounded-lg text-[9px] font-bold active-shrink">+ DICOM</button>
            <button @click="simulateUpload('Radiology_Report.pdf','2.4 MB','pdf')"
              class="clinical-btn-secondary flex-1 py-1.5 rounded-lg text-[9px] font-bold active-shrink">+ PDF</button>
          </div>

          <!-- Active uploads -->
          <div v-if="activeUploads.length > 0" class="space-y-2">
            <div class="section-title">Uploading</div>
            <div v-for="u in activeUploads" :key="u.id" class="p-2.5 bg-sky-50/60 border border-sky-100 rounded-xl">
              <div class="flex items-center justify-between mb-1.5">
                <span class="text-[10px] font-bold text-slate-700 truncate">{{ u.name }}</span>
                <span class="text-[9px] font-bold text-sky-600 flex-shrink-0 ml-2">{{ u.progress }}%</span>
              </div>
              <div class="progress-track h-1.5">
                <div class="progress-fill" :style="`width:${u.progress}%`"></div>
              </div>
            </div>
          </div>

          <!-- Completed uploads -->
          <div v-if="completedUploads.length > 0" class="space-y-1.5">
            <div class="section-title">Completed Queue</div>
            <div v-for="u in completedUploads.slice(-4)" :key="u.id"
              class="flex items-center gap-2 p-2 bg-white/50 border border-slate-100/70 rounded-lg"
            >
              <CheckCircle2 class="w-3.5 h-3.5 text-teal-500 flex-shrink-0" />
              <span class="text-[9px] font-semibold text-slate-700 truncate">{{ u.name }}</span>
              <span class="ml-auto text-[8px] font-bold text-slate-400 flex-shrink-0">{{ typeLabel(u.type) }}</span>
            </div>
          </div>
        </div>

        <!-- Patient Assignment -->
        <div class="frosted-glass-panel p-5 space-y-3">
          <div class="section-title flex items-center gap-1.5"><Database class="w-3.5 h-3.5" /> Patient Assignment</div>
          <div class="space-y-2.5">
            <div>
              <label class="section-title block mb-1">Patient Name</label>
              <input v-model="patientName" type="text" placeholder="Full name" class="clinical-input w-full px-3 py-2 text-xs" />
            </div>
            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="section-title block mb-1">Date of Birth</label>
                <input v-model="patientDob" type="date" class="clinical-input w-full px-3 py-2 text-xs" />
              </div>
              <div>
                <label class="section-title block mb-1">Sex</label>
                <select v-model="patientGender" class="clinical-input w-full px-3 py-2 text-xs">
                  <option>Male</option><option>Female</option><option>Other</option>
                </select>
              </div>
            </div>
            <div>
              <label class="section-title block mb-1">Modality</label>
              <select v-model="modality" class="clinical-input w-full px-3 py-2 text-xs">
                <option>CT Abdomen (Portal Venous)</option>
                <option>CT Abdomen (Contrast)</option>
                <option>CT Abdomen (Non-contrast)</option>
                <option>MRI Abdomen</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- CENTER + RIGHT: Validation + Pipeline -->
      <div class="lg:col-span-8 space-y-4">

        <!-- DICOM Validation -->
        <div class="frosted-glass-panel p-5 space-y-3">
          <div class="flex items-center justify-between">
            <div>
              <div class="section-title flex items-center gap-1.5"><ShieldCheck class="w-3.5 h-3.5 text-teal-600" /> DICOM Tag Validation</div>
              <h3 class="text-xs font-black text-slate-800 mt-0.5">Mandatory Tag Compliance Check</h3>
            </div>
            <span class="text-[9px] font-bold text-teal-600 bg-teal-50 border border-teal-100 px-2 py-1 rounded-lg">6 / 6 PASS</span>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
            <div v-for="c in validationChecks" :key="c.label"
              class="flex items-center justify-between py-2 px-3 bg-white/60 border border-slate-100/70 rounded-xl"
            >
              <span class="text-[9px] font-mono font-semibold text-slate-600">{{ c.label }}</span>
              <span :class="['text-[8px] font-black', c.pass ? 'text-teal-600' : 'text-rose-600']">{{ c.pass ? 'PASS' : 'FAIL' }}</span>
            </div>
          </div>
        </div>

        <!-- Preprocessing Pipeline -->
        <div class="frosted-glass-panel p-5 space-y-3">
          <div>
            <div class="section-title flex items-center gap-1.5"><Zap class="w-3.5 h-3.5 text-amber-500" /> Preprocessing Pipeline</div>
            <h3 class="text-xs font-black text-slate-800 mt-0.5">CT Volume Processing Steps</h3>
          </div>

          <div class="space-y-2">
            <div
              v-for="(step, i) in pipelineSteps"
              :key="step.step"
              class="flex items-center gap-3 p-3 rounded-xl border transition-colors"
              :class="step.status === 'done' ? 'bg-teal-50/40 border-teal-100/60' : 'bg-slate-50/40 border-slate-200/40'"
            >
              <div :class="['w-6 h-6 rounded-full flex items-center justify-center text-[9px] font-black flex-shrink-0', step.status === 'done' ? 'bg-teal-500 text-white' : 'bg-slate-200 text-slate-500']">
                <CheckCircle2 v-if="step.status === 'done'" class="w-3.5 h-3.5" />
                <span v-else>{{ i + 1 }}</span>
              </div>
              <div class="min-w-0">
                <div class="text-[10px] font-bold text-slate-800">{{ step.step }}</div>
                <div class="text-[9px] text-slate-500 font-medium">{{ step.desc }}</div>
              </div>
              <span :class="['ml-auto text-[8px] font-bold flex-shrink-0', step.status === 'done' ? 'text-teal-600' : 'text-slate-400']">
                {{ step.status === 'done' ? 'Done' : 'Pending' }}
              </span>
            </div>
          </div>
        </div>

        <!-- Recently Added Patients -->
        <div class="frosted-glass-panel overflow-hidden">
          <div class="px-5 py-3.5 border-b border-slate-200/50 bg-white/30 flex items-center justify-between">
            <div>
              <div class="section-title">Queue</div>
              <h3 class="text-xs font-black text-slate-800 mt-0.5">Recently Uploaded Cases</h3>
            </div>
          </div>
          <table class="w-full clinical-table">
            <thead>
              <tr>
                <th>Patient</th>
                <th>Modality</th>
                <th>Uploaded</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="p in patients.slice(-4).reverse()" :key="p.id">
                <td>
                  <div class="text-[10px] font-bold text-slate-800">{{ p.name }}</div>
                  <div class="text-[8px] font-mono text-slate-400">{{ p.id }}</div>
                </td>
                <td class="text-[10px] text-slate-600">{{ p.modality.replace('CT Abdomen ', '') }}</td>
                <td class="text-[9px] font-mono text-slate-500">{{ p.scanDate?.substring(0,10) }}</td>
                <td>
                  <span :class="['inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[8px] font-bold', p.status === 'Completed' ? 'badge-completed' : p.status === 'Analyzing' ? 'badge-analyzing' : 'badge-pending']">
                    {{ p.status }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>
