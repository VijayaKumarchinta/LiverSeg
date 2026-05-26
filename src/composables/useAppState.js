import { ref, computed } from 'vue'

const patients = ref([])

const activities = ref([])

const activePatientId = ref(null)

const isInferenceRunning = ref(false)
const inferenceProgress = ref(0)
const inferenceStage = ref('Initializing...')
const uploadQueue = ref([])

export function useAppState() {
  const activePatient = computed(() => patients.value.find(p => p.id === activePatientId.value))

  const fetchPatients = async () => {
    try {
      const token = localStorage.getItem('token')
      const res = await fetch('http://localhost:8000/api/patients/', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      if (res.ok) {
        patients.value = await res.json()
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
      const token = localStorage.getItem('token')
      const res = await fetch('http://localhost:8000/api/activities/', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      if (res.ok) {
        activities.value = await res.json()
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
          activities.value.unshift({
            id: Date.now(),
            type: 'success',
            action: 'AI Analysis Completed',
            details: `For case ${patients.value[pIndex].id}`,
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
          })
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
        
        // Add to patients list
        const newId = `PT-${Math.floor(Math.random() * 9000) + 1000}-X`
        patients.value.unshift({
          id: newId,
          name: 'Anonymous Patient',
          gender: 'Unknown',
          age: 0,
          modality: type === 'dicom' ? 'CT' : 'MRI',
          scanDate: new Date().toISOString().split('T')[0],
          status: 'Ready',
          hasLesions: false,
          lesionVolume: '—',
          metrics: { dice: '—', volume: '—' },
          slices: Array(20).fill(0).map(() => ({ liverX: 0, liverY: 0, lesionSize: 0 }))
        })
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
    simulateUpload
  }
}
