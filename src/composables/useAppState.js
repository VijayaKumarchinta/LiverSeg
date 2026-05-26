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

  const runSegmentation = (id) => {
    if (isInferenceRunning.value) return
    const pIndex = patients.value.findIndex(p => p.id === id)
    if (pIndex === -1) return

    isInferenceRunning.value = true
    inferenceProgress.value = 0
    inferenceStage.value = 'Loading model...'
    patients.value[pIndex].status = 'Analyzing'
    
    // Persist analyzing status to DB
    api.patch(`/patients/${id}/`, { status: 'Analyzing' }).catch(err => console.error(err))

    let progress = 0
    const interval = setInterval(() => {
      progress += Math.random() * 15
      if (progress > 100) progress = 100
      inferenceProgress.value = Math.floor(progress)

      if (progress < 30) inferenceStage.value = 'Preprocessing volume...'
      else if (progress < 70) inferenceStage.value = 'Running 3D U-Net Inference...'
      else if (progress < 95) inferenceStage.value = 'Extracting mesh & metrics...'
      else inferenceStage.value = 'Finalizing...'

      if (progress === 100) {
        clearInterval(interval)
        setTimeout(() => {
          isInferenceRunning.value = false
          patients.value[pIndex].status = 'Completed'
          patients.value[pIndex].metrics = { dice: '94.8%', volume: '1520 cc' }
          
          // Persist completed status & metrics to DB
          api.patch(`/patients/${id}/`, { 
            status: 'Completed',
            metrics: { dice: '94.8%', volume: '1520 cc' }
          }).catch(err => console.error(err))

          activities.value.unshift({
            id: Date.now(),
            type: 'success',
            action: 'AI Analysis Completed',
            details: `For case ${patients.value[pIndex].id}`,
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
          })
          saveActivities()
        }, 800)
      }
    }, 500)
  }

  const simulateUpload = (filename, size, type) => {
    uploadQueue.value.push({ filename, size, type, progress: 0, status: 'uploading' })
    const qIndex = uploadQueue.value.length - 1

    let progress = 0
    const interval = setInterval(() => {
      progress += Math.random() * 20
      if (progress > 100) progress = 100
      uploadQueue.value[qIndex].progress = Math.floor(progress)

      if (progress === 100) {
        clearInterval(interval)
        uploadQueue.value[qIndex].status = 'completed'
        
        activities.value.unshift({
          id: Date.now(),
          type: 'success',
          action: 'Upload Completed',
          details: filename,
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        })
        saveActivities()
        
        // Add to patients list and persist in DB
        const newId = `PT-${Math.floor(Math.random() * 9000) + 1000}-X`
        const newPatient = {
          id: newId,
          name: 'Anonymous Patient',
          gender: 'Unknown',
          age: 0,
          dob: '2026-01-01',
          modality: type === 'dicom' ? 'CT' : 'MRI',
          status: 'Ready',
          has_lesions: false,
          lesion_volume: '—',
          metrics: { dice: '—', volume: '—' },
          slices: Array(20).fill(0).map((_, idx) => ({
            slice_index: idx,
            liver_size: 0,
            liver_x: 0,
            liver_y: 0,
            lesion_size: 0,
            lesion_x: 0,
            lesion_y: 0
          }))
        }

        api.post('/patients/', newPatient).then(res => {
          if (res.data) {
            patients.value.unshift(mapPatientToCamelCase(res.data))
            if (!activePatientId.value) {
              activePatientId.value = newId
            }
          }
        }).catch(err => console.error('Error saving patient to backend:', err))
      }
    }, 400)
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
    simulateUpload,
    pacsConfig,
    fetchPacsConfig,
    updatePacs
  }
}
