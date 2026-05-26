<script setup>
import Navbar from '../components/common/Navbar.vue'
import FooterSection from '../components/common/FooterSection.vue'
</script>

<template>
  <div class="relative min-h-screen bg-slate-50 text-slate-900 overflow-x-hidden font-sans flex flex-col justify-between">
    <!-- Navbar -->
    <Navbar />
    
    <!-- Routed content with layout wrapper padding -->
    <main class="flex-1 pt-14 relative z-10">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Footer -->
    <FooterSection />
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
