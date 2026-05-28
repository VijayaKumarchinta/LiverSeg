<template>
  <div class="ct-viewer">

    <div class="viewer-header">
      <div>
        <h2>Clinical CT Viewer</h2>
        <p>Liver Segmentation Overlay</p>
      </div>

      <div class="viewer-controls">
        <button @click="zoomIn" title="Zoom In">+</button>
        <button @click="zoomOut" title="Zoom Out">−</button>
        <button @click="resetView" title="Reset View">Reset</button>
      </div>
    </div>

    <div class="scan-container" @wheel.prevent="handleScroll">

      <!-- No scan state -->
      <div v-if="!hasScan" class="no-scan-placeholder">
        <div class="no-scan-icon">🩻</div>
        <div class="no-scan-title">No CT Scan Uploaded</div>
        <div class="no-scan-sub">Upload a .nii, .nii.gz, or .dcm file to view the CT scan here.</div>
      </div>

      <!-- Real scan from backend API -->
      <template v-else>
        <img
          :src="scanUrl"
          class="ct-scan"
          :style="{ transform: `scale(${zoomLevel})`, filter: ctFilter }"
          alt="CT Scan"
          @error="onImageError"
        />

        <img
          v-if="showMask && maskUrl"
          :src="maskUrl"
          class="segmentation-mask"
          :style="{ opacity: normalizedOpacity }"
          alt="Liver Segmentation Mask"
        />

        <div class="crosshair horizontal"></div>
        <div class="crosshair vertical"></div>

        <div class="scan-metadata">
          <span>Slice {{ currentSliceIndex }}/{{ patient?.slices?.length || 20 }}</span>
          <span>WL: {{ wl }}</span>
          <span>WW: {{ ww }}</span>
          <span v-if="patient?.id">{{ patient.id }}</span>
        </div>

        <!-- Image load error -->
        <div v-if="imageError" class="image-error-overlay">
          <div>⚠ Failed to load scan image</div>
          <div class="image-error-url">{{ scanUrl }}</div>
        </div>

        <!-- Zoom indicator -->
        <div v-if="zoomLevel !== 1" class="zoom-indicator">{{ Math.round(zoomLevel * 100) }}%</div>
      </template>

    </div>

    <div class="mask-controls" v-if="hasScan">

      <label>Mask Opacity</label>

      <input
        type="range"
        min="0"
        max="1"
        step="0.05"
        v-model.number="localOpacity"
      />

      <button @click="showMask = !showMask">
        {{ showMask ? 'Hide Mask' : 'Show Mask' }}
      </button>

    </div>

  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  // Patient object from API — contains ctScanUrl, liverMaskUrl, etc.
  patient: {
    type: Object,
    default: null
  },
  // Slice index for display metadata
  currentSlice: {
    type: Number,
    default: 11
  },
  // Window Width (Hounsfield Units) for contrast filter
  ww: {
    type: Number,
    default: 400
  },
  // Window Level (Hounsfield Units) for brightness filter
  wl: {
    type: Number,
    default: 40
  },
  // Mask opacity 0–100 (percentage from parent controls)
  maskOpacity: {
    type: Number,
    default: 65
  }
})

const emit = defineEmits(['update:currentSlice'])

// Internal state
const showMask = ref(true)
const zoomLevel = ref(1)
const localOpacity = ref(props.maskOpacity / 100)
const imageError = ref(false)

// Sync local opacity from parent prop
watch(() => props.maskOpacity, (val) => {
  localOpacity.value = val / 100
})

// Derived values
const currentSliceIndex = computed(() => props.currentSlice + 1)

const hasScan = computed(() => !!props.patient?.ctScanUrl)

const scanUrl = computed(() => {
  if (!props.patient?.ctScanUrl) return null;
  const baseUrl = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/api\/?$/, '');
  return `${baseUrl}/api/patients/${props.patient.id}/slice/?index=${props.currentSlice}&type=ct&ww=${props.ww}&wl=${props.wl}`;
})

const maskUrl = computed(() => {
  if (!props.patient?.liverMaskUrl) return null;
  const baseUrl = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/api\/?$/, '');
  return `${baseUrl}/api/patients/${props.patient.id}/slice/?index=${props.currentSlice}&type=mask`;
})

// Normalize opacity: parent sends 0-100, we display as 0-1
const normalizedOpacity = computed(() => localOpacity.value)

// CSS filter is no longer heavily simulating HU because the backend now handles WW/WL via API!
// But we can leave a slight contrast boost for the PNGs
const ctFilter = computed(() => {
  return `contrast(1.0) brightness(1.0)`
})

// Controls
const zoomIn = () => { zoomLevel.value = Math.min(zoomLevel.value + 0.25, 4) }
const zoomOut = () => { zoomLevel.value = Math.max(zoomLevel.value - 0.25, 0.5) }
const resetView = () => { zoomLevel.value = 1; imageError.value = false }

const handleScroll = (e) => {
  // Medical standard: scroll wheel changes slice
  if (e.deltaY < 0) {
    if (props.currentSlice > 0) {
      emit('update:currentSlice', props.currentSlice - 1)
    }
  } else {
    const maxSlices = props.patient?.slices?.length || 20
    if (props.currentSlice < maxSlices - 1) {
      emit('update:currentSlice', props.currentSlice + 1)
    }
  }
}

const onImageError = () => {
  imageError.value = true
}

// Reset error state when patient changes
watch(() => props.patient?.id, () => {
  imageError.value = false
  zoomLevel.value = 1
})
</script>

<style scoped>

.ct-viewer {
  background: white;
  border-radius: 20px;
  padding: 20px;
  border: 1px solid #e5edf2;
}

.viewer-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 18px;
}

.viewer-header h2 {
  color: #183b56;
  margin: 0;
  font-size: 14px;
  font-weight: 900;
}

.viewer-header p {
  color: #6b7d89;
  margin-top: 4px;
  font-size: 11px;
}

.viewer-controls {
  display: flex;
  gap: 8px;
}

.viewer-controls button {
  background: white;
  border: 1px solid #dbe5ec;
  border-radius: 10px;
  padding: 8px 12px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 700;
  color: #475569;
  transition: all 0.15s;
}

.viewer-controls button:hover {
  border-color: #0f766e;
  color: #0f766e;
  background: #f0fdfa;
}

.scan-container {
  position: relative;
  width: 100%;
  aspect-ratio: 1 / 1;
  background: #050508;
  overflow: hidden;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ── No scan placeholder ── */
.no-scan-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  color: #475569;
  text-align: center;
  padding: 32px;
}

.no-scan-icon {
  font-size: 48px;
  opacity: 0.3;
}

.no-scan-title {
  font-size: 13px;
  font-weight: 700;
  color: #64748b;
}

.no-scan-sub {
  font-size: 11px;
  color: #94a3b8;
  max-width: 220px;
  line-height: 1.5;
}

/* ── Real scan image ── */
.ct-scan {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.2s ease;
}

.segmentation-mask {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  mix-blend-mode: screen;
  object-fit: cover;
  pointer-events: none;
}

.crosshair {
  position: absolute;
  background: rgba(255, 255, 255, 0.15);
  pointer-events: none;
}

.horizontal {
  width: 100%;
  height: 1px;
  top: 50%;
}

.vertical {
  height: 100%;
  width: 1px;
  left: 50%;
}

.scan-metadata {
  position: absolute;
  bottom: 14px;
  left: 14px;
  display: flex;
  gap: 14px;
  background: rgba(0, 0, 0, 0.55);
  color: white;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 10px;
  font-family: monospace;
  pointer-events: none;
}

.zoom-indicator {
  position: absolute;
  top: 14px;
  right: 14px;
  background: rgba(0, 0, 0, 0.55);
  color: #14b8a6;
  font-size: 10px;
  font-family: monospace;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 6px;
  pointer-events: none;
}

.image-error-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #f87171;
  font-size: 11px;
  font-weight: 700;
  text-align: center;
  padding: 16px;
}

.image-error-url {
  font-size: 9px;
  color: #94a3b8;
  font-family: monospace;
  word-break: break-all;
  max-width: 280px;
}

/* ── Mask Controls ── */
.mask-controls {
  margin-top: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.mask-controls label {
  font-size: 11px;
  font-weight: 700;
  color: #475569;
  white-space: nowrap;
}

.mask-controls input {
  flex: 1;
  accent-color: #0f766e;
}

.mask-controls button {
  background: #0f766e;
  color: white;
  border: none;
  padding: 9px 14px;
  border-radius: 10px;
  font-size: 11px;
  font-weight: 700;
  cursor: pointer;
  white-space: nowrap;
  transition: background 0.15s;
}

.mask-controls button:hover {
  background: #0d6560;
}

</style>