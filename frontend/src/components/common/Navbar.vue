<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { Activity, Menu, X, ArrowRight } from 'lucide-vue-next'

const isScrolled = ref(false)
const mobileMenuOpen = ref(false)
const route = useRoute()

const handleScroll = () => {
  isScrolled.value = window.scrollY > 10
}

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

const closeMobileMenu = () => {
  mobileMenuOpen.value = false
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  handleScroll()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

const navLinks = [
  { name: 'Home', path: '/' },
  { name: 'Platform', path: '/platform' },
  { name: 'Research', path: '/research' },
  { name: 'About', path: '/about' },
  { name: 'Contact', path: '/contact' }
]
</script>

<template>
  <nav 
    :class="[
      'fixed left-1/2 -translate-x-1/2 z-50 transition-all duration-300 w-[95%] max-w-7xl rounded-2xl border',
      isScrolled 
        ? 'top-3 bg-white/75 border-slate-200/60 shadow-md py-2 backdrop-blur-md' 
        : 'top-4 bg-white/55 border-slate-200/40 shadow-sm py-2.5 backdrop-blur-md'
    ]"
  >
    <div class="w-full px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-14">
        <!-- Logo -->
        <router-link to="/" class="flex items-center gap-2.5 group">
          <div class="relative flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-tr from-teal-500 to-sky-600 text-white shadow-sm group-hover:scale-105 transition-transform duration-300">
            <Activity class="w-5.5 h-5.5" />
          </div>
          <div class="flex flex-col">
            <span class="text-base font-bold tracking-tight text-slate-900 leading-none">
              LiverSeg<span class="text-teal-600 bg-gradient-to-r from-teal-600 to-sky-600 bg-clip-text text-transparent">AI</span>
            </span>
            <span class="text-[9px] uppercase tracking-widest font-bold text-slate-400 mt-1">Radiology Suite</span>
          </div>
        </router-link>

        <!-- Desktop Navigation Links -->
        <div class="hidden md:flex items-center gap-1">
          <router-link 
            v-for="link in navLinks" 
            :key="link.name" 
            :to="link.path"
            :class="[
              'px-3.5 py-2 text-sm font-semibold rounded-lg transition-all duration-200 active-shrink',
              route.path === link.path 
                ? 'text-teal-600 bg-teal-50/50' 
                : 'text-slate-600 hover:text-slate-950 hover:bg-slate-50'
            ]"
          >
            {{ link.name }}
          </router-link>
          
          <div class="h-5 w-px bg-slate-200 mx-3"></div>

          <router-link 
            to="/app" 
            class="flex items-center gap-1.5 px-4 py-2 text-xs font-semibold uppercase tracking-wider rounded-lg clinical-btn-primary active-shrink"
          >
            Launch Workspace
            <ArrowRight class="w-3.5 h-3.5" />
          </router-link>
        </div>

        <!-- Mobile Menu Toggle -->
        <div class="md:hidden">
          <button 
            @click="toggleMobileMenu" 
            class="p-2 rounded-lg text-slate-600 hover:bg-slate-100 transition-colors"
            aria-label="Toggle menu"
          >
            <Menu v-if="!mobileMenuOpen" class="w-6 h-6" />
            <X v-else class="w-6 h-6" />
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Navigation Drawer -->
    <div 
      v-show="mobileMenuOpen" 
      class="md:hidden border-t border-slate-200/60 mt-2 bg-white/95 backdrop-blur-xl transition-all duration-300 rounded-b-2xl overflow-hidden"
    >
      <div class="px-4 pt-2 pb-6 space-y-1">
        <router-link 
          v-for="link in navLinks" 
          :key="link.name" 
          :to="link.path" 
          @click="closeMobileMenu"
          :class="[
            'block px-4 py-2.5 text-base font-semibold rounded-lg transition-all',
            route.path === link.path 
              ? 'text-teal-600 bg-teal-50' 
              : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
          ]"
        >
          {{ link.name }}
        </router-link>
        <div class="pt-4 border-t border-slate-100 px-4 flex flex-col gap-3">
          <router-link 
            to="/login"
            @click="closeMobileMenu"
            class="block text-center py-2.5 text-sm font-semibold text-slate-700 hover:text-slate-900 bg-slate-50 rounded-lg active-shrink"
          >
            Sign In
          </router-link>
          
          <router-link 
            to="/app" 
            @click="closeMobileMenu"
            class="flex items-center justify-center gap-2 w-full px-5 py-3 text-sm font-semibold uppercase tracking-wider rounded-lg clinical-btn-primary active-shrink"
          >
            Launch Workspace
            <ArrowRight class="w-4 h-4" />
          </router-link>
        </div>
      </div>
    </div>
  </nav>
</template>
