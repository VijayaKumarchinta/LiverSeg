<template>
  <div class="ct-viewer">

    <div class="viewer-header">
      <div>
        <h2>Clinical CT Viewer</h2>
        <p>Liver Segmentation Overlay</p>
      </div>

      <div class="viewer-controls">
        <button @click="zoomIn">+</button>
        <button @click="zoomOut">−</button>
        <button @click="resetView">Reset</button>
      </div>
    </div>

    <div class="scan-container">

      <img
        :src="currentSlice"
        class="ct-scan"
      />

      <img
        v-if="showMask"
        :src="currentMask"
        class="segmentation-mask"
        :style="{ opacity: maskOpacity }"
      />

      <div class="crosshair horizontal"></div>
      <div class="crosshair vertical"></div>

      <div class="scan-metadata">
        <span>Slice {{ currentSliceIndex }}/20</span>
        <span>WL: 40</span>
        <span>WW: 400</span>
      </div>

    </div>

    <div class="mask-controls">

      <label>Mask Opacity</label>

      <input
        type="range"
        min="0"
        max="1"
        step="0.1"
        v-model="maskOpacity"
      />

      <button @click="toggleMask">
        {{ showMask ? 'Hide Mask' : 'Show Mask' }}
      </button>

    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import ctSlice from '../assets/medical/ct-slice.png'
import liverMask from '../assets/medical/liver-mask.png'

const currentSlice = ref(ctSlice)
const currentMask = ref(liverMask)

const currentSliceIndex = ref(11)

const maskOpacity = ref(0.5)
const showMask = ref(true)

const zoomIn = () => {
  console.log('Zoom In')
}

const zoomOut = () => {
  console.log('Zoom Out')
}

const resetView = () => {
  console.log('Reset View')
}

const toggleMask = () => {
  showMask.value = !showMask.value
}
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
  margin-bottom: 18px;
}

.viewer-header h2 {
  color: #183b56;
  margin: 0;
}

.viewer-header p {
  color: #6b7d89;
  margin-top: 4px;
}

.viewer-controls {
  display: flex;
  gap: 10px;
}

.viewer-controls button {
  background: white;
  border: 1px solid #dbe5ec;
  border-radius: 10px;
  padding: 10px 14px;
  cursor: pointer;
}

.scan-container {
  position: relative;
  width: 100%;
  aspect-ratio: 1 / 1;
  background: black;
  overflow: hidden;
  border-radius: 16px;
}

.ct-scan {
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: contrast(1.1);
}

.segmentation-mask {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  mix-blend-mode: screen;
}

.crosshair {
  position: absolute;
  background: rgba(255,255,255,0.2);
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
  gap: 18px;
  background: rgba(0,0,0,0.5);
  color: white;
  padding: 8px 14px;
  border-radius: 10px;
  font-size: 13px;
}

.mask-controls {
  margin-top: 18px;
  display: flex;
  align-items: center;
  gap: 14px;
}

.mask-controls input {
  flex: 1;
}

.mask-controls button {
  background: #0f766e;
  color: white;
  border: none;
  padding: 10px 14px;
  border-radius: 10px;
}

</style>