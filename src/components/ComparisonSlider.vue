<template>
  <div class="comparison-wrapper">

    <img :src="beforeImage" class="base-image" />

    <div
      class="overlay-container"
      :style="{ width: sliderPosition + '%' }"
    >
      <img :src="afterImage" class="overlay-image" />
    </div>

    <input
      type="range"
      min="0"
      max="100"
      v-model="sliderPosition"
      class="slider"
    />

  </div>
</template>

<script setup>
import { ref } from 'vue'

const sliderPosition = ref(50)

defineProps({
  beforeImage: String,
  afterImage: String
})
</script>

<style scoped>

.comparison-wrapper {
  position: relative;
  overflow: hidden;
  border-radius: 18px;
}

.base-image,
.overlay-image {
  width: 100%;
  display: block;
}

.overlay-container {
  position: absolute;
  top: 0;
  left: 0;
  overflow: hidden;
  height: 100%;
}

.slider {
  width: 100%;
  margin-top: 10px;
}

</style>