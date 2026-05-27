<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  modelValue: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['update:modelValue'])

const sliderRef = ref(null)
const isDragging = ref(false)

const startDrag = (event) => {
  event.preventDefault()
  isDragging.value = true
  document.addEventListener('mousemove', onDrag)
  document.addEventListener('mouseup', stopDrag)
  document.addEventListener('touchmove', onDrag, { passive: false })
  document.addEventListener('touchend', stopDrag)
}

const onDrag = (event) => {
  if (!isDragging.value || !sliderRef.value) return
  
  // Prevent default scroll on touch
  if (event.cancelable) event.preventDefault()
  
  const container = sliderRef.value.parentElement
  if (!container) return
  
  const rect = container.getBoundingClientRect()
  const clientX = event.touches ? event.touches[0].clientX : event.clientX
  
  // Calculate relative X position as a percentage
  let percentage = ((clientX - rect.left) / rect.width) * 100
  percentage = Math.max(0, Math.min(100, percentage))
  
  emit('update:modelValue', percentage)
}

const stopDrag = () => {
  if (isDragging.value) {
    isDragging.value = false
    document.removeEventListener('mousemove', onDrag)
    document.removeEventListener('mouseup', stopDrag)
    document.removeEventListener('touchmove', onDrag)
    document.removeEventListener('touchend', stopDrag)
  }
}

onUnmounted(() => {
  stopDrag()
})
</script>

<template>
  <div 
    ref="sliderRef"
    class="absolute top-0 bottom-0 z-20 w-1 -ml-0.5 cursor-ew-resize select-none pointer-events-auto"
    :style="{ left: `${modelValue}%` }"
    @mousedown="startDrag"
    @touchstart="startDrag"
  >
    <!-- Divider Line -->
    <div class="h-full w-full bg-teal-500 shadow-[0_0_8px_rgba(20,184,166,0.8)] relative">
      <!-- Drag Handle -->
      <div 
        class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-8 h-8 rounded-full bg-slate-900 border-2 border-teal-500 shadow-[0_0_12px_rgba(20,184,166,0.6)] flex items-center justify-center transition-transform hover:scale-110 active:scale-95"
        :class="{ 'scale-110 ring-4 ring-teal-500/20': isDragging }"
      >
        <!-- Custom icon: two small triangles pointing left and right -->
        <svg class="w-4 h-4 text-teal-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M8 7l-5 5 5 5M16 7l5 5-5 5" />
        </svg>
      </div>
      
      <!-- Scan Labels on either side of the slider -->
      <div class="absolute top-3 right-4 bg-black/60 border border-slate-700/50 text-slate-350 text-[9px] font-bold font-mono px-2 py-0.5 rounded pointer-events-none uppercase tracking-wider">
        Original
      </div>
      <div class="absolute top-3 left-4 bg-black/60 border border-teal-800/50 text-teal-400 text-[9px] font-bold font-mono px-2 py-0.5 rounded pointer-events-none uppercase tracking-wider">
        AI Mask
      </div>
    </div>
  </div>
</template>
