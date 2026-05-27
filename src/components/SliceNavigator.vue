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
  <div class="space-y-3 pt-3 border-t border-slate-200/60 dark:border-slate-800/60">
    <div class="flex justify-between items-center text-xs">
      <span class="font-bold text-slate-700 dark:text-slate-300">Axial Slice Navigator</span>
      <span class="font-mono text-slate-500 dark:text-slate-400 font-bold bg-slate-50 dark:bg-slate-900 border dark:border-slate-800 px-2 py-0.5 rounded">
        Slice {{ modelValue + 1 }} / {{ max }}
      </span>
    </div>
    
    <div class="flex items-center gap-4">
      <button 
        @click="decrement" 
        :disabled="modelValue === 0"
        class="p-1.5 rounded-lg border border-slate-200 dark:border-slate-700 hover:border-teal-500 dark:hover:border-teal-400 disabled:opacity-30 disabled:hover:border-slate-200 dark:disabled:hover:border-slate-700 transition-colors"
        title="Previous Slice (Left Arrow)"
      >
        <ChevronLeft class="w-4 h-4 text-slate-600 dark:text-slate-400" />
      </button>
      
      <div class="flex-1 relative flex items-center">
        <input 
          :value="modelValue"
          @input="onSliderInput"
          type="range" 
          min="0" 
          :max="max - 1" 
          step="1"
          class="w-full accent-teal-600 cursor-pointer bg-slate-100 dark:bg-slate-800 h-1.5 rounded-full appearance-none outline-none focus:ring-1 focus:ring-teal-500/20"
        />
      </div>
      
      <button 
        @click="increment" 
        :disabled="modelValue === props.max - 1"
        class="p-1.5 rounded-lg border border-slate-200 dark:border-slate-700 hover:border-teal-500 dark:hover:border-teal-400 disabled:opacity-30 disabled:hover:border-slate-200 dark:disabled:hover:border-slate-700 transition-colors"
        title="Next Slice (Right Arrow)"
      >
        <ChevronRight class="w-4 h-4 text-slate-600 dark:text-slate-400" />
      </button>
    </div>
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
