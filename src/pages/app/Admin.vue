<script setup>
import { ref, onMounted } from 'vue'
import { 
  Users, Server, Activity, CheckCircle
} from 'lucide-vue-next'
import api from '../../api'

const adminUsers = ref([])
const adminLogs = ref([])

onMounted(async () => {
  try {
    const usersRes = await api.get('/users/')

    if (usersRes.data) {
      adminUsers.value = usersRes.data.map(u => ({
        id: u.id,
        name: `${u.first_name} ${u.last_name}`.trim() || u.username,
        role: u.role,
        status: u.status === 'active' ? 'Active' : 'Inactive'
      }))

      // Aggregate activities from all users
      const allLogs = []
      usersRes.data.forEach(u => {
        if (u.activities && Array.isArray(u.activities)) {
          u.activities.forEach(log => {
            allLogs.push({
              time: log.time,
              user: `${u.first_name} ${u.last_name}`.trim() || u.username,
              action: log.action + (log.details ? ` (${log.details})` : ''),
              status: log.type === 'success' ? 'SUCCESS' : 'INFO'
            })
          })
        }
      })
      adminLogs.value = allLogs
    }
  } catch (error) {
    console.error('Error fetching admin data:', error)
  }
})
</script>

<template>
  <div class="space-y-6 animate-fade-in">
    
    <!-- Top KPIs -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="frosted-glass-panel p-4 flex items-center justify-between">
        <div class="space-y-1">
          <div class="text-[9px] font-bold uppercase tracking-wider text-slate-400">Total Users Active</div>
          <div class="text-xl font-extrabold text-slate-900">14 Doctors</div>
          <div class="text-[10px] text-slate-500 font-bold">5 Roles Configured</div>
        </div>
        <div class="w-9 h-9 rounded-lg bg-purple-50 text-purple-700 flex items-center justify-center shadow-sm">
          <Users class="w-4.5 h-4.5" />
        </div>
      </div>

      <div class="frosted-glass-panel p-4 flex items-center justify-between">
        <div class="space-y-1">
          <div class="text-[9px] font-bold uppercase tracking-wider text-slate-400">Platform Network Load</div>
          <div class="text-xl font-extrabold text-slate-900">421.5 Mbps</div>
          <div class="text-[10px] text-emerald-600 font-bold flex items-center gap-0.5">
            <CheckCircle class="w-3 h-3" /> PACS routing stable
          </div>
        </div>
        <div class="w-9 h-9 rounded-lg bg-purple-50 text-purple-700 flex items-center justify-center shadow-sm">
          <Server class="w-4.5 h-4.5" />
        </div>
      </div>

      <div class="frosted-glass-panel p-4 flex items-center justify-between">
        <div class="space-y-1">
          <div class="text-[9px] font-bold uppercase tracking-wider text-slate-400">AI GPU Utilisation</div>
          <div class="text-xl font-extrabold text-slate-900">48.2% Average</div>
          <div class="text-[10px] text-slate-500 font-bold">Running model inference</div>
        </div>
        <div class="w-9 h-9 rounded-lg bg-purple-50 text-purple-700 flex items-center justify-center shadow-sm">
          <Activity class="w-4.5 h-4.5" />
        </div>
      </div>

      <div class="frosted-glass-panel p-4 flex items-center justify-between">
        <div class="space-y-1">
          <div class="text-[9px] font-bold uppercase tracking-wider text-slate-400">Compliance Audit status</div>
          <div class="text-xl font-extrabold text-slate-900">100% Verified</div>
          <div class="text-[10px] text-slate-500 font-bold">HIPAA Compliant trace log</div>
        </div>
        <div class="w-9 h-9 rounded-lg bg-purple-50 text-purple-700 flex items-center justify-center shadow-sm">
          <CheckCircle class="w-4.5 h-4.5" />
        </div>
      </div>
    </div>

    <!-- Admin Details Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
      
      <!-- Left: Users & Logs -->
      <div class="lg:col-span-8 space-y-6">
        
        <!-- Users table -->
        <div class="frosted-glass-panel overflow-hidden !p-0">
          <div class="px-5 py-3 border-b border-slate-200/50 bg-white/40">
            <h3 class="font-extrabold text-slate-800 text-xs tracking-tight uppercase">Hospital User Access Management</h3>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse text-xs">
              <thead>
                <tr class="bg-slate-50/50 border-b border-slate-200/50 text-slate-500 font-bold">
                  <th class="px-5 py-2.5 font-bold text-[9px] uppercase tracking-wider">User Account</th>
                  <th class="px-5 py-2.5 font-bold text-[9px] uppercase tracking-wider">Role Assigned</th>
                  <th class="px-5 py-2.5 font-bold text-[9px] uppercase tracking-wider">Status</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100/50 text-slate-700 font-semibold">
                <tr v-for="user in adminUsers" :key="user.id" class="hover:bg-white/40 transition-colors">
                  <td class="px-5 py-3 font-bold text-slate-800">{{ user.name }}</td>
                  <td class="px-5 py-3 font-mono text-[10px] text-slate-500 font-bold">{{ user.role }}</td>
                  <td class="px-5 py-3">
                    <span :class="user.status === 'Active' ? 'bg-emerald-50 text-emerald-700 border-emerald-100' : 'bg-slate-100 text-slate-500 border-slate-200'" class="px-2 py-0.5 rounded text-[9px] font-bold border">
                      {{ user.status }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Audit log console -->
        <div class="frosted-glass-panel p-5 space-y-4">
          <h3 class="font-extrabold text-slate-800 text-xs tracking-tight uppercase border-b border-slate-200/50 pb-2.5">Real-time Compliance Audit Trail</h3>
          <div class="space-y-2.5">
            <div v-for="log in adminLogs" :key="log.time" class="flex items-center justify-between text-xs p-2.5 bg-white/40 border border-slate-200/50 rounded-xl hover:border-slate-300 transition-colors">
              <div class="flex items-center gap-3">
                <span class="font-mono text-[10px] text-slate-400 font-bold">{{ log.time }}</span>
                <span class="font-extrabold text-slate-800">{{ log.user }}</span>
                <span class="text-slate-500 font-semibold">&mdash; {{ log.action }}</span>
              </div>
              <span :class="log.status === 'SUCCESS' ? 'text-emerald-600' : 'text-amber-500'" class="text-[9.5px] font-bold font-mono">{{ log.status }}</span>
            </div>
          </div>
        </div>

      </div>

      <!-- Right: Server health checks -->
      <div class="lg:col-span-4 space-y-6">
        <div class="frosted-glass-panel p-5 space-y-4">
          <h3 class="font-extrabold text-slate-800 text-xs tracking-tight uppercase border-b border-slate-200/50 pb-2.5">PACS &amp; Service Health</h3>
          
          <div class="space-y-3.5">
            <div class="flex justify-between items-center text-xs">
              <span class="font-bold text-slate-700">DICOM PACS Router</span>
              <span class="px-2.5 py-0.5 rounded bg-emerald-50 text-emerald-800 font-bold text-[9px] border border-emerald-100">ONLINE</span>
            </div>
            <div class="flex justify-between items-center text-xs">
              <span class="font-bold text-slate-700">AI Inference Server</span>
              <span class="px-2.5 py-0.5 rounded bg-emerald-50 text-emerald-800 font-bold text-[9px] border border-emerald-100">ONLINE</span>
            </div>
            <div class="flex justify-between items-center text-xs">
              <span class="font-bold text-slate-700">PostgreSQL Database</span>
              <span class="px-2.5 py-0.5 rounded bg-emerald-50 text-emerald-800 font-bold text-[9px] border border-emerald-100">STABLE</span>
            </div>
            <div class="flex justify-between items-center text-xs">
              <span class="font-bold text-slate-700">Storage Allocation</span>
              <span class="font-mono font-bold text-slate-500">1.2 TB / 4.0 TB free</span>
            </div>
          </div>

          <!-- Health visual tracker representation -->
          <div class="pt-4 border-t border-slate-200/50 text-center">
            <div class="text-[10px] text-slate-400 font-bold uppercase tracking-wider mb-2">Host Node Latency</div>
            <div class="flex gap-1 justify-center items-end h-8">
              <div class="w-2.5 bg-purple-400 rounded-t h-3"></div>
              <div class="w-2.5 bg-purple-400 rounded-t h-4"></div>
              <div class="w-2.5 bg-purple-400 rounded-t h-3.5"></div>
              <div class="w-2.5 bg-purple-400 rounded-t h-5"></div>
              <div class="w-2.5 bg-purple-500 rounded-t h-6 animate-pulse"></div>
            </div>
            <div class="text-[9px] font-mono text-slate-400 mt-2 font-bold">12ms average node latency</div>
          </div>

        </div>
      </div>

    </div>

  </div>
</template>
