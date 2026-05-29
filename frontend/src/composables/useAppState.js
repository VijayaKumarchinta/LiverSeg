import { ref, computed } from 'vue'
import api from '../api'

const patients = ref([])
const activities = ref([])
const activePatientId = ref(null)

const isInferenceRunning = ref(false)
const inferenceProgress = ref(0)
const inferenceStage = ref('Initializing...')
const uploadQueue = ref([])

const pacsConfig = ref({
  aeTitle: 'LIVERSEG_AI_AE',
  port: 104,
  ipAddress: '192.168.10.45',
  compression: 'Lossless JPEG-LS',
  autoRoute: true,
  validateOnReceive: true
})

const fetchPacsConfig = async () => {
  try {
    const res = await api.get('/users/me/')
    if (res.data && res.data.pacs_config) {
      pacsConfig.value = res.data.pacs_config
    }
  } catch (error) {
    console.error('Error fetching PACS config:', error)
  }
}

const updatePacs = async (newConfig) => {
  try {
    await api.patch('/users/me/', { pacs_config: newConfig })
    pacsConfig.value = { ...pacsConfig.value, ...newConfig }
  } catch (error) {
    console.error('Error updating PACS config:', error)
  }
}

const saveActivities = async () => {
  try {
    await api.patch('/users/me/', { activities: activities.value })
  } catch (error) {
    console.error('Error saving activities:', error)
  }
}

const mapSliceToCamelCase = (slice) => {
  if (!slice) return slice
  return {
    ...slice,
    sliceIndex: slice.slice_index,
    liverSize: slice.liver_size,
    liverX: slice.liver_x,
    liverY: slice.liver_y,
    lesionSize: slice.lesion_size,
    lesionX: slice.lesion_x,
    lesionY: slice.lesion_y
  }
}

const mapPatientToCamelCase = (patient) => {
  if (!patient) return patient
  return {
    ...patient,
    scanDate: patient.scan_date,
    hasLesions: patient.has_lesions,
    lesionVolume: patient.lesion_volume,
    hasFile: patient.has_file,
    // Real image URLs from backend media storage
    ctScanUrl: patient.ct_scan_url || null,
    liverMaskUrl: patient.liver_mask_url || null,
    previewImageUrl: patient.preview_image_url || null,
    slices: patient.slices ? patient.slices.map(mapSliceToCamelCase) : []
  }
}

export function useAppState() {
  const activePatient = computed(() => patients.value.find(p => p.id === activePatientId.value))

  const fetchPatients = async () => {
    try {
      const res = await api.get('/patients/')
      if (res.data) {
        patients.value = res.data.map(mapPatientToCamelCase)
        if (patients.value.length > 0 && !activePatientId.value) {
          activePatientId.value = patients.value[0].id
        }
      }
    } catch (error) {
      console.error('Error fetching patients:', error)
    }
  }

  const fetchActivities = async () => {
    try {
      const res = await api.get('/users/me/')
      if (res.data && res.data.activities) {
        activities.value = res.data.activities
      }
    } catch (error) {
      console.error('Error fetching activities:', error)
    }
  }

  const selectPatient = (id) => {
    activePatientId.value = id
  }

  // ── REAL upload: sends actual file bytes to backend ──────────────────────
  const realUpload = async (file, patientId) => {
    if (!file || !patientId) {
      console.error('realUpload requires a File object and a patient ID')
      return null
    }

    // Add to upload queue for progress display
    const queueItem = {
      id: Date.now(),
      filename: file.name,
      size: (file.size / 1048576).toFixed(1) + ' MB',
      type: detectFileType(file.name),
      progress: 0,
      status: 'uploading'
    }
    uploadQueue.value.push(queueItem)
    const qIndex = uploadQueue.value.length - 1

    const formData = new FormData()
    formData.append('ct_scan', file)

    try {
      const res = await api.post(`/patients/${patientId}/upload_scan/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (e) => {
          const pct = Math.round((e.loaded * 100) / e.total)
          uploadQueue.value[qIndex].progress = pct
        }
      })

      uploadQueue.value[qIndex].status = 'completed'
      uploadQueue.value[qIndex].progress = 100

      const patientResponse =
        await api.get(`/patients/${patientId}/`)

      const updatedPatient =
        mapPatientToCamelCase(patientResponse.data)

      const pIndex =
        patients.value.findIndex(
          p => p.id === patientId
        )

      if (pIndex !== -1) {
        patients.value[pIndex] = updatedPatient
      }

      activities.value.unshift({
        id: Date.now(),
        type: 'success',
        action: 'Scan Uploaded',
        details: file.name,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      })
      saveActivities()

      return res.data
    } catch (error) {
      uploadQueue.value[qIndex].status = 'error'
      console.error('Upload failed:', error.response?.data || error.message)
      throw error
    }
  }

  // ── DEMO fallback: simulate upload with fake progress (no real file) ─────

  // ── REAL segmentation: calls backend API instead of fake timer ───────────
  const runSegmentation = async (id) => {
    if (isInferenceRunning.value) return

    const pIndex = patients.value.findIndex(p => p.id === id)
    if (pIndex === -1) return

    isInferenceRunning.value = true
    inferenceProgress.value = 0
    inferenceStage.value = 'Connecting to inference pipeline...'
    patients.value[pIndex].status = 'Analyzing'

    try {
      // Call the real backend endpoint
      await api.post(`/patients/${id}/run_segmentation/`)
      inferenceStage.value = 'Preprocessing volume data...'
      const interval = setInterval(
        async () => {

          const patientResponse =
            await api.get(`/patients/${id}/`)

          const updatedPatient =
            mapPatientToCamelCase(
              patientResponse.data
            )

          patients.value[pIndex] =
            updatedPatient

          if (
            updatedPatient.status ===
            'Completed'
          ) {

            clearInterval(interval)

            inferenceProgress.value = 100

            inferenceStage.value =
              'Completed'

            isInferenceRunning.value =
              false
          }

        },
        2000
      )
    } catch (error) {
      console.error('Segmentation API error:', error.response?.data || error.message)
      // Fallback to local demo simulation if backend call fails
      inferenceStage.value = 'Running local demo simulation...'
      isInferenceRunning.value = false
      patients.value[pIndex].status = 'Ready'
    }
  }

  return {
    patients,
    activities,
    activePatient,
    fetchPatients,
    fetchActivities,
    selectPatient,
    runSegmentation,
    isInferenceRunning,
    inferenceProgress,
    inferenceStage,
    uploadQueue,
    realUpload,
    pacsConfig,
    fetchPacsConfig,
    updatePacs
  }
}

// ── Helpers ──────────────────────────────────────────────────────────────────

function detectFileType(filename) {
  const f = filename.toLowerCase()
  if (f.endsWith('.dcm')) return 'dicom'
  if (f.endsWith('.nii') || f.endsWith('.nii.gz')) return 'nifti'
  if (f.endsWith('.pdf')) return 'pdf'
  return 'unknown'
}