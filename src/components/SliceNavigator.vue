<script setup>
import { ChevronLeft, ChevronRight } from 'lucide-vue-next'

const props = defineProps({
  modelValue: {
    type: Number,
    required: true
  },
  max: {
    type: Number,
    default: 20
  }
})

const emit = defineEmits(['update:modelValue'])

const decrement = () => {
  if (props.modelValue > 0) {
    emit('update:modelValue', props.modelValue - 1)
  }
}

const increment = () => {
  if (props.modelValue < props.max - 1) {
    emit('update:modelValue', props.modelValue + 1)
  }
}

const onSliderInput = (event) => {
  emit('update:modelValue', parseInt(event.target.value, 10))
}
</script>

<template>

<div class="slice-nav">

  <button @click="prevSlice">◀</button>

  <div class="slider-section">

    <input
      type="range"
      :max="maxSlices"
      v-model="currentSlice"
    />

    <div class="slice-info">
      Slice {{ currentSlice }} / {{ maxSlices }}
    </div>

  </div>

  <button @click="nextSlice">▶</button>

</div>

</template>

<style scoped>
input[type="range"]::-webkit-slider-thumb {
  appearance: none;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #0d9488;
  cursor: pointer;
  transition: transform 0.1s ease, background-color 0.1s ease;
}

input[type="range"]::-webkit-slider-thumb:hover {
  transform: scale(1.2);
  background: #0f766e;
}
</style>
