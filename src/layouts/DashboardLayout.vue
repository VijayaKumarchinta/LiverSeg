<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useAppState } from '../composables/useAppState'
import {
  LayoutDashboard, Upload, ScanLine, FileText, Users,
  Brain, Settings, Shield, LogOut, ChevronLeft, ChevronRight,
  Bell, Activity, Server, Search, Cpu, ChevronDown,
  AlertCircle, CheckCircle2, Wifi
} from 'lucide-vue-next'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const isSidebarCollapsed = ref(false)
const showNotifications = ref(false)
const showUserDropdown = ref(false)
const mouseX = ref(0)
const mouseY = ref(0)
const containerRef = ref(null)

const handleMouseMove = (e) => {
  mouseX.value = e.clientX
  mouseY.value = e.clientY
}

const toggleSidebar = () => { isSidebarCollapsed.value = !isSidebarCollapsed.value }

const handleLogout = () => {
  auth.logout()
  router.push('/login')
}

const menuItems = [
  { name: 'Dashboard',    path: '/app',            icon: LayoutDashboard, exact: true },
  { name: 'Upload Scan',  path: '/app/upload',     icon: Upload },
  { name: 'AI Analysis',  path: '/app/analysis',   icon: ScanLine },
  { name: 'Patients',     path: '/app/patients',   icon: Users },
  { name: 'Reports',      path: '/app/reports',    icon: FileText },
  { name: 'Research',     path: '/app/research',   icon: Brain },
  { name: 'Settings',     path: '/app/settings',   icon: Settings },
  { name: 'Admin',        path: '/app/admin',      icon: Shield },
]

const filteredMenuItems = computed(() => {
  const role = auth.userRole
  return menuItems.filter(item => {
    // Admin route only for admin
    if (item.name === 'Admin' && role !== 'admin') return false
    // Research route only for researcher
    if (item.name === 'Research' && role !== 'researcher') return false
    // Upload Scan route only for radiologist and technician
    if (item.name === 'Upload Scan' && role !== 'radiologist' && role !== 'technician') return false
    // AI Analysis route only for radiologist
    if (item.name === 'AI Analysis' && role !== 'radiologist') return false
    return true
  })
})

const isActive = (item) => {
  if (item.exact) return route.path === item.path
  return route.path.startsWith(item.path)
}

const roleColors = {
  radiologist: 'bg-teal-50 text-teal-700 border-teal-200',
  admin: 'bg-purple-50 text-purple-700 border-purple-200',
  researcher: 'bg-blue-50 text-blue-700 border-blue-200',
  clinician: 'bg-emerald-50 text-emerald-700 border-emerald-200',
  technician: 'bg-amber-50 text-amber-700 border-amber-200',
}

const roleLabel = {
  radiologist: 'Radiologist',
  admin: 'Hospital Admin',
  researcher: 'AI Researcher',
  clinician: 'Clinician',
  technician: 'Technician',
}

const notifications = ref([
  { id: 1, title: 'AI Model Updated', desc: 'Encoder weights optimized (Dice +0.3%)', time: '5m', read: false, type: 'success' },
  { id: 2, title: 'PACS Ingest Complete', desc: '32 slices imported for PT-8831-C', time: '22m', read: false, type: 'info' },
  { id: 3, title: 'Segmentation Queued', desc: 'PT-5542-K awaiting GPU slot', time: '1h', read: true, type: 'warning' },
])

const unreadCount = ref(notifications.value.filter(n => !n.read).length)

const { fetchPatients, fetchActivities } = useAppState()

const closeDropdowns = (e) => {
  if (!e.target.closest('.notif-zone')) showNotifications.value = false
  if (!e.target.closest('.user-zone')) showUserDropdown.value = false
}

onMounted(() => {
  document.addEventListener('click', closeDropdowns)
  if (auth.isAuthenticated) {
    fetchPatients()
    fetchActivities()
  }
})
onUnmounted(() => document.removeEventListener('click', closeDropdowns))
</script>

<template>
  <div
    class="flex h-screen overflow-hidden clinical-workspace font-sans"
    @mousemove="handleMouseMove"
  >
    <!-- Cursor glow -->
    <div
      class="workspace-glow pointer-events-none"
      :style="{ '--mouse-x': mouseX + 'px', '--mouse-y': mouseY + 'px' }"
    />

    <!-- ════════════════════════════════════════
         LEFT SIDEBAR
    ════════════════════════════════════════ -->
    <aside
      :class="[
        'glass-sidebar flex flex-col z-30 flex-shrink-0 transition-all duration-300 relative',
        isSidebarCollapsed ? 'w-16' : 'w-60'
      ]"
    >
      <!-- Logo -->
      <div class="flex items-center justify-between h-14 px-3 border-b border-slate-200/50 flex-shrink-0">
        <router-link to="/app" class="flex items-center gap-2.5 min-w-0">
          <div class="flex-shrink-0 w-8 h-8 rounded-lg bg-gradient-to-br from-teal-500 to-sky-600 flex items-center justify-center shadow-sm">
            <Activity class="w-4 h-4 text-white" />
          </div>
          <transition name="fade">
            <span v-if="!isSidebarCollapsed" class="font-black text-slate-800 text-sm tracking-tight whitespace-nowrap">
              LiverSeg<span class="bg-gradient-to-r from-teal-600 to-sky-500 bg-clip-text text-transparent">AI</span>
            </span>
          </transition>
        </router-link>
        <button
          @click="toggleSidebar"
          class="hidden md:flex p-1 rounded-md text-slate-400 hover:text-slate-600 hover:bg-slate-100/70 transition-colors flex-shrink-0"
        >
          <ChevronLeft v-if="!isSidebarCollapsed" class="w-3.5 h-3.5" />
          <ChevronRight v-else class="w-3.5 h-3.5" />
        </button>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 py-2 overflow-y-auto clinical-scrollbar">
        <div class="px-2 space-y-0.5">
          <router-link
            v-for="item in filteredMenuItems"
            :key="item.name"
            :to="item.path"
            :class="[
              'nav-item flex items-center gap-3 px-3 py-2.5 text-xs font-semibold transition-all duration-150 group',
              isActive(item) ? 'nav-item-active' : 'text-slate-500 hover:text-slate-800'
            ]"
            :data-tip="isSidebarCollapsed ? item.name : ''"
            :class2="isSidebarCollapsed ? 'tooltip' : ''"
          >
            <component
              :is="item.icon"
              :class="['w-4 h-4 flex-shrink-0 transition-colors', isActive(item) ? 'text-teal-600' : 'text-slate-400 group-hover:text-slate-600']"
            />
            <transition name="fade">
              <span v-if="!isSidebarCollapsed" class="whitespace-nowrap truncate">{{ item.name }}</span>
            </transition>
            <transition name="fade">
              <span v-if="!isSidebarCollapsed && item.name === 'Admin' && auth.userRole !== 'admin'" class="ml-auto text-[8px] font-bold bg-slate-100 text-slate-400 px-1.5 py-0.5 rounded-full">Admin</span>
            </transition>
          </router-link>
        </div>
      </nav>

      <!-- AI Engine Status -->
      <div v-if="!isSidebarCollapsed" class="px-3 py-2 border-t border-slate-200/40 flex-shrink-0">
        <div class="flex items-center gap-2 px-2.5 py-2 rounded-lg bg-teal-50/60 border border-teal-100/60">
          <div class="relative flex-shrink-0">
            <div class="w-2 h-2 rounded-full bg-teal-500"></div>
            <div class="w-2 h-2 rounded-full bg-teal-500 absolute inset-0 animate-ping opacity-60"></div>
          </div>
          <div class="min-w-0">
            <div class="text-[9px] font-bold text-teal-700 uppercase tracking-wide">AI Engine</div>
            <div class="text-[8px] text-teal-600 font-semibold">MONAI v1.4 · Online</div>
          </div>
        </div>
      </div>

      <!-- User section -->
      <div class="px-2 py-2 border-t border-slate-200/40 flex-shrink-0">
        <button
          @click="handleLogout"
          :class="[
            'flex items-center gap-3 w-full px-3 py-2 rounded-lg text-xs font-semibold text-rose-500 hover:bg-rose-50 hover:text-rose-600 transition-colors',
            isSidebarCollapsed ? 'justify-center' : ''
          ]"
        >
          <LogOut class="w-4 h-4 flex-shrink-0" />
          <span v-if="!isSidebarCollapsed">Sign Out</span>
        </button>
      </div>
    </aside>

    <!-- ════════════════════════════════════════
         RIGHT CONTENT AREA
    ════════════════════════════════════════ -->
    <div class="flex-1 flex flex-col min-w-0 overflow-hidden">

      <!-- ── TOP HEADER ── -->
      <header class="glass-header h-14 flex items-center justify-between px-5 z-20 flex-shrink-0">

        <!-- Left: Page title + breadcrumb -->
        <div class="flex items-center gap-3 min-w-0">
          <div class="min-w-0">
            <h1 class="text-[11px] font-black text-slate-800 uppercase tracking-widest truncate">
              {{ route.meta?.title || 'Clinical Workstation' }}
            </h1>
            <div class="text-[9px] text-slate-400 font-semibold">
              LiversegAI v2.5 · Radiology Suite · <span class="text-teal-600">PACS_NODE_4</span>
            </div>
          </div>
        </div>

        <!-- Right: Controls -->
        <div class="flex items-center gap-3 flex-shrink-0">

          <!-- PACS Node Status -->
          <div class="hidden lg:flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-slate-50 border border-slate-200/60">
            <Wifi class="w-3 h-3 text-teal-500" />
            <span class="text-[9px] font-bold text-slate-600">PACS: <span class="text-teal-600">LIVERSEG_AI_AE</span></span>
          </div>

          <!-- GPU Status -->
          <div class="hidden lg:flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-slate-50 border border-slate-200/60">
            <Cpu class="w-3 h-3 text-sky-500" />
            <span class="text-[9px] font-bold text-slate-600">GPU: <span class="text-sky-600">48% · T4</span></span>
          </div>

          <!-- Notifications -->
          <div class="relative notif-zone">
            <button
              @click.stop="showNotifications = !showNotifications; showUserDropdown = false"
              class="relative p-2 text-slate-400 hover:text-slate-700 hover:bg-slate-100/70 rounded-lg transition-colors"
            >
              <Bell class="w-4 h-4" />
              <span v-if="unreadCount > 0" class="absolute top-1 right-1 w-2 h-2 bg-rose-500 rounded-full"></span>
            </button>

            <transition name="slide-up">
              <div
                v-if="showNotifications"
                class="absolute right-0 top-full mt-2 w-72 frosted-glass-panel p-3 z-50 shadow-xl"
              >
                <div class="flex items-center justify-between mb-2.5 pb-2 border-b border-slate-200/50">
                  <span class="text-xs font-bold text-slate-800">System Alerts</span>
                  <span class="text-[9px] bg-rose-50 text-rose-600 font-bold px-1.5 py-0.5 rounded-full border border-rose-100">{{ unreadCount }} New</span>
                </div>
                <div class="space-y-1.5">
                  <div
                    v-for="n in notifications"
                    :key="n.id"
                    class="p-2.5 rounded-lg border transition-colors"
                    :class="n.read ? 'bg-white/40 border-slate-100/60' : 'bg-teal-50/40 border-teal-100/60'"
                  >
                    <div class="flex items-start gap-2">
                       <CheckCircle2 v-if="n.type==='success'" class="w-3 h-3 text-teal-500 mt-0.5 flex-shrink-0" />
                      <AlertCircle v-else-if="n.type==='warning'" class="w-3 h-3 text-amber-500 mt-0.5 flex-shrink-0" />
                      <Server v-else class="w-3 h-3 text-sky-500 mt-0.5 flex-shrink-0" />
                      <div class="min-w-0">
                        <div class="text-[10px] font-bold text-slate-800">{{ n.title }}</div>
                        <div class="text-[9px] text-slate-500 font-medium mt-0.5">{{ n.desc }}</div>
                      </div>
                      <span class="text-[8px] text-slate-400 font-bold flex-shrink-0">{{ n.time }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </transition>
          </div>

          <!-- User Profile -->
          <div class="relative user-zone">
            <button
              @click.stop="showUserDropdown = !showUserDropdown; showNotifications = false"
              class="flex items-center gap-2 pl-1 pr-2 py-1 rounded-lg hover:bg-slate-100/70 transition-colors border border-transparent hover:border-slate-200/60"
            >
              <div class="w-7 h-7 rounded-full bg-gradient-to-br from-teal-500 to-sky-600 flex items-center justify-center text-white font-black text-[10px] flex-shrink-0">
                {{ auth.userInitials }}
              </div>
              <div class="hidden md:block text-left">
                <div class="text-[10px] font-bold text-slate-800 leading-tight">{{ auth.userName }}</div>
                <div class="text-[8px] font-semibold leading-tight" :class="roleColors[auth.userRole]?.split(' ')[1] || 'text-teal-600'">
                  {{ roleLabel[auth.userRole] || auth.userRole }}
                </div>
              </div>
              <ChevronDown class="w-3 h-3 text-slate-400" />
            </button>

            <transition name="slide-up">
              <div
                v-if="showUserDropdown"
                class="absolute right-0 top-full mt-2 w-52 frosted-glass-panel p-1.5 z-50 shadow-xl"
              >
                <div class="px-3 py-2.5 border-b border-slate-200/50 mb-1">
                  <div class="text-[10px] font-bold text-slate-800">{{ auth.userName }}</div>
                  <div class="text-[9px] text-slate-500 font-medium truncate">@{{ auth.userUsername }}</div>
                  <span class="inline-flex mt-1.5 text-[8px] font-bold px-2 py-0.5 rounded-full border" :class="roleColors[auth.userRole] || 'bg-teal-50 text-teal-700 border-teal-200'">
                    {{ roleLabel[auth.userRole] || auth.userRole }}
                  </span>
                </div>
                <router-link to="/app/settings" @click="showUserDropdown=false" class="flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-semibold text-slate-600 hover:bg-slate-50 transition-colors">
                  <Settings class="w-3.5 h-3.5 text-slate-400" /> Settings
                </router-link>

                <button @click="handleLogout" class="flex items-center gap-2 w-full px-3 py-2 rounded-lg text-xs font-semibold text-rose-600 hover:bg-rose-50 transition-colors">
                  <LogOut class="w-3.5 h-3.5" /> Sign Out
                </button>
              </div>
            </transition>
          </div>
        </div>
      </header>

      <!-- ── MAIN WORKSPACE ── -->
      <main
        ref="containerRef"
        class="flex-1 overflow-y-auto workspace-bg clinical-scrollbar relative"
      >
        <div class="relative z-10 p-5">
          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </div>
      </main>
    </div>
  </div>
</template>
