<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AdminStatCard from '@features/admin/components/shared/AdminStatCard.vue'

// Chart.js imports
import {
  Chart as ChartJS, Title, Tooltip, Legend,
  BarElement, CategoryScale, LinearScale,
  LineElement, PointElement, ArcElement
} from 'chart.js'
import { Bar, Doughnut } from 'vue-chartjs'

ChartJS.register(
  CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend,
  LineElement, PointElement, ArcElement
)

interface RevCard {
  label: string
  value: string
  sub: string
  delta: string
  deltaUp: boolean
  icon: string
}

interface CostRow {
  category: string
  amount: number
  pct: number
}

interface MonthRow {
  month: string
  revenue: number
  cogs: number
  gross: number
}

const revCards = ref<RevCard[]>([])
const costRows = ref<CostRow[]>([])
const loading = ref(true)
const period = ref<'day' | 'week' | 'month' | 'year'>('month')

const rawData = ref({
  day: [] as MonthRow[],
  week: [] as MonthRow[],
  month: [] as MonthRow[],
  year: [] as MonthRow[],
})

const monthRows = computed(() => rawData.value[period.value] || [])

onMounted(() => {
  setTimeout(() => {
    revCards.value = [
      { label: 'Ingresos Brutos', value: '$58,400', sub: 'Abril 2024',      delta: '+18%', deltaUp: true, icon: 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z' },
      { label: 'Ingresos Netos',  value: '$51,230', sub: 'Tras descuentos', delta: '+14%', deltaUp: true, icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2' },
      { label: 'Ticket Promedio', value: '$170.80', sub: '342 órdenes',     delta: '+6%',  deltaUp: true, icon: 'M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z' },
      { label: 'Devoluciones',    value: '$1,840',  sub: '11 órdenes',      delta: '-3%',  deltaUp: true, icon: 'M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4' },
    ]

    costRows.value = [
      { category: 'Costo de Mercancía',     amount: 23360, pct: 40 },
      { category: 'Envios y Logística',     amount: 5840,  pct: 10 },
      { category: 'Descuentos Aplicados',   amount: 3504,  pct: 6  },
      { category: 'Comisiones de Pago',     amount: 1752,  pct: 3  },
      { category: 'Cambios y Devoluciones', amount: 1840,  pct: 3  },
    ]

    rawData.value = {
      day: [
        { month: '12 Abr', revenue: 1200, cogs: 480,  gross: 720 },
        { month: '13 Abr', revenue: 1500, cogs: 600,  gross: 900 },
        { month: '14 Abr', revenue: 1100, cogs: 440,  gross: 660 },
        { month: '15 Abr', revenue: 2100, cogs: 840,  gross: 1260 },
        { month: '16 Abr', revenue: 2800, cogs: 1120, gross: 1680 },
        { month: '17 Abr', revenue: 3200, cogs: 1280, gross: 1920 },
        { month: 'Hoy',    revenue: 1800, cogs: 720,  gross: 1080 },
      ],
      week: [
        { month: 'W1 Abr', revenue: 12500, cogs: 5000, gross: 7500 },
        { month: 'W2 Abr', revenue: 14200, cogs: 5680, gross: 8520 },
        { month: 'W3 Abr', revenue: 15300, cogs: 6120, gross: 9180 },
        { month: 'W4 Abr', revenue: 16400, cogs: 6560, gross: 9840 },
      ],
      month: [
        { month: 'Nov 2023', revenue: 31200, cogs: 12480, gross: 18720 },
        { month: 'Dec 2023', revenue: 48900, cogs: 19560, gross: 29340 },
        { month: 'Jan 2024', revenue: 27500, cogs: 11000, gross: 16500 },
        { month: 'Feb 2024', revenue: 33800, cogs: 13520, gross: 20280 },
        { month: 'Mar 2024', revenue: 49400, cogs: 19760, gross: 29640 },
        { month: 'Abr 2024', revenue: 58400, cogs: 23360, gross: 35040 },
      ],
      year: [
        { month: '2021',     revenue: 250000, cogs: 100000, gross: 150000 },
        { month: '2022',     revenue: 380000, cogs: 152000, gross: 228000 },
        { month: '2023',     revenue: 494000, cogs: 197600, gross: 296400 },
        { month: '2024 YTD', revenue: 169100, cogs: 67640,  gross: 101460 },
      ],
    }

    loading.value = false
  }, 600)
})

function grossMargin(row: MonthRow) {
  if (row.revenue === 0) return '0.0'
  return ((row.gross / row.revenue) * 100).toFixed(1)
}

// Chart.js Data & Options
const mainChartData = computed(() => ({
  labels: monthRows.value.map(r => r.month),
  datasets: [
    {
      type: 'line' as const,
      label: 'Margen (%)',
      data: monthRows.value.map(r => {
        if (r.revenue === 0) return 0
        return Number(((r.gross / r.revenue) * 100).toFixed(1))
      }),
      borderColor: '#222222', // Obsidian-like
      backgroundColor: '#222222',
      yAxisID: 'y1',
      tension: 0.4,
      borderWidth: 2,
      pointRadius: 3,
    },
    {
      type: 'bar' as const,
      label: 'Utilidad Bruta',
      data: monthRows.value.map(r => r.gross),
      backgroundColor: '#C9A84C', // var(--admin-amber)
      borderRadius: { topLeft: 4, topRight: 4, bottomLeft: 0, bottomRight: 0 },
      yAxisID: 'y',
      stack: 'stack0',
    },
    {
      type: 'bar' as const,
      label: 'COGS',
      data: monthRows.value.map(r => r.cogs),
      backgroundColor: 'rgba(0,0,0,0.06)',
      borderRadius: { topLeft: 0, topRight: 0, bottomLeft: 4, bottomRight: 4 },
      yAxisID: 'y',
      stack: 'stack0',
    }
  ]
}))

const mainChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: { mode: 'index' as const, intersect: false },
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: 'rgba(0,0,0,0.85)',
      padding: 10,
      cornerRadius: 8,
      callbacks: {
        label: (ctx: any) => {
          if (ctx.datasetIndex === 0) return ` ${ctx.dataset.label}: ${ctx.raw}%`
          return ` ${ctx.dataset.label}: $${ctx.raw.toLocaleString()}`
        }
      }
    }
  },
  scales: {
    x: { grid: { display: false }, stacked: true },
    y: { 
      stacked: true, 
      border: { display: false },
      ticks: { callback: (val: any) => '$' + val / 1000 + 'k' }
    },
    y1: {
      position: 'right' as const,
      grid: { display: false },
      ticks: { callback: (val: any) => val + '%' },
      min: 0, max: 100
    }
  }
}

const donutChartData = computed(() => ({
  labels: costRows.value.map(r => r.category),
  datasets: [{
    data: costRows.value.map(r => r.amount),
    backgroundColor: [
      '#C9A84C', // var(--admin-amber)
      '#222222', // var(--admin-obsidian wrapper)
      '#666666',
      '#aaaaaa',
      '#dddddd',
    ],
    borderWidth: 3,
    borderColor: '#ffffff',
    hoverOffset: 4
  }]
}))

const donutOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: 'rgba(0,0,0,0.85)',
      padding: 10,
      cornerRadius: 8,
      callbacks: {
        label: (ctx: any) => {
          const val = ctx.raw
          const total = ctx.dataset.data.reduce((a: number, b: number) => a + b, 0)
          const pct = ((val / total) * 100).toFixed(1)
          return ` $${val.toLocaleString()} (${pct}%)`
        }
      }
    }
  },
  cutout: '75%'
}
</script>

<template>
  <div class="space-y-6">
    <!-- Filters -->
    <div class="flex justify-end">
      <!-- Period selector -->
      <div class="flex gap-1 border rounded-lg p-1 bg-white" style="border-color: rgba(0,0,0,0.08);">
        <button
          v-for="p in [
            { id: 'day', label: 'día' },
            { id: 'week', label: 'semana' },
            { id: 'month', label: 'mes' },
            { id: 'year', label: 'año' }
          ]"
          :key="p.id"
          class="px-3 py-1 text-[0.65rem] font-bold uppercase tracking-widest rounded-md transition-all"
          :style="period === p.id
            ? { background: 'var(--admin-amber)', color: 'white' }
            : { color: 'var(--admin-text-secondary)' }"
          @click="period = p.id as any"
        >{{ p.label }}</button>
      </div>
    </div>

    <!-- Skeleton -->
    <div v-if="loading" class="grid grid-cols-2 xl:grid-cols-4 gap-4">
      <div v-for="i in 4" :key="i" class="h-28 rounded-xl animate-pulse" style="background: rgba(0,0,0,0.06);" />
    </div>

    <template v-else>
      <!-- Revenue cards -->
      <div class="grid grid-cols-2 xl:grid-cols-4 gap-4">
        <AdminStatCard
          v-for="card in revCards"
          :key="card.label"
          :label="card.label"
          :value="card.value"
          :sub="card.sub"
          :delta="card.delta"
          :delta-up="card.deltaUp"
          :icon="card.icon"
        />
      </div>

      <!-- Main Chart Card (Chart.js Bar+Line) -->
      <div class="bg-white rounded-xl p-6" style="box-shadow: var(--admin-card-shadow);">
        <div class="flex items-center justify-between mb-6">
          <p class="text-[0.72rem] font-semibold uppercase tracking-wider" style="color: var(--admin-text-primary);">Ingresos vs Costo (COGS)</p>
          <div class="flex items-center gap-4">
            <div class="flex items-center gap-1.5 text-[0.6rem] font-bold uppercase tracking-widest text-gray-500">
              <span class="w-2.5 h-2.5 bg-black/[0.06] rounded-sm" /> COGS
            </div>
            <div class="flex items-center gap-1.5 text-[0.6rem] font-bold uppercase tracking-widest text-gray-500">
              <span class="w-2.5 h-2.5 rounded-sm" style="background: var(--admin-amber);" /> Utilidad
            </div>
            <div class="flex items-center gap-1.5 text-[0.6rem] font-bold uppercase tracking-widest text-gray-500">
              <span class="w-2.5 h-0.5 bg-[#222] rounded-full" /> Margen %
            </div>
          </div>
        </div>
        
        <div class="w-full h-[280px]">
          <Bar :data="mainChartData" :options="mainChartOptions" />
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-5 gap-6">
        <!-- Cost breakdown (Doughnut) -->
        <div class="lg:col-span-2 bg-white rounded-xl p-6 flex flex-col" style="box-shadow: var(--admin-card-shadow);">
          <p class="text-[0.72rem] font-semibold uppercase tracking-wider mb-6" style="color: var(--admin-text-primary);">Desglose de Costos</p>
          
          <div class="relative flex-1 flex flex-col justify-center min-h-[220px]">
             <!-- Chart -->
             <div class="absolute inset-0 flex justify-center items-center">
               <Doughnut :data="donutChartData" :options="donutOptions" />
             </div>
             <!-- Center Text -->
             <div class="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
               <span class="text-[0.65rem] font-bold uppercase tracking-widest text-gray-400">Total Fijos</span>
               <span class="text-[1.1rem] font-bold" style="color: var(--admin-text-primary);">$34k</span>
             </div>
          </div>

          <div class="mt-6 pt-4 border-t space-y-2.5" style="border-color: var(--admin-border);">
             <div v-for="(row, i) in costRows.slice(0, 3)" :key="row.category" class="flex justify-between text-[0.75rem]">
               <div class="flex items-center gap-2">
                 <span class="w-2 h-2 rounded-full" :style="{ background: donutChartData.datasets[0].backgroundColor[i] }" />
                 <span style="color: var(--admin-text-secondary);">{{ row.category }}</span>
               </div>
               <span class="font-bold" style="color: var(--admin-text-primary);">${{ row.amount.toLocaleString() }}</span>
             </div>
          </div>
        </div>

        <!-- Monthly P&L table -->
        <div class="lg:col-span-3 bg-white rounded-xl overflow-hidden flex flex-col" style="box-shadow: var(--admin-card-shadow);">
          <div class="px-6 py-4 border-b" style="border-color: var(--admin-border);">
            <p class="text-[0.72rem] font-semibold uppercase tracking-wider" style="color: var(--admin-text-primary);">Resumen Mensual P&L</p>
          </div>
          <div class="overflow-x-auto flex-1">
            <table class="w-full">
              <thead>
                <tr style="background: var(--admin-bg);">
                  <th class="px-5 py-3 text-left font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Mes</th>
                  <th class="px-5 py-3 text-right font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Ingreso</th>
                  <th class="px-5 py-3 text-right font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">COGS</th>
                  <th class="px-5 py-3 text-right font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Bruto</th>
                  <th class="px-5 py-3 text-right font-semibold uppercase tracking-wider" style="font-size: 0.62rem; color: var(--admin-text-secondary);">Margen</th>
                </tr>
              </thead>
              <tbody class="divide-y" style="border-color: var(--admin-border);">
                <tr
                  v-for="row in monthRows.slice().reverse()"
                  :key="row.month"
                  class="hover:bg-black/[0.01] transition-colors"
                >
                  <td class="px-5 py-3.5 text-[0.78rem] font-medium" style="color: var(--admin-text-primary);">{{ row.month }}</td>
                  <td class="px-5 py-3.5 text-right text-[0.78rem]" style="color: var(--admin-text-secondary);">${{ row.revenue.toLocaleString() }}</td>
                  <td class="px-5 py-3.5 text-right text-[0.78rem] text-red-500/80">-${{ row.cogs.toLocaleString() }}</td>
                  <td class="px-5 py-3.5 text-right font-bold text-[0.78rem]" style="color: var(--admin-text-primary);">${{ row.gross.toLocaleString() }}</td>
                  <td class="px-5 py-3.5 text-right">
                    <span
                      class="text-[0.68rem] font-bold px-2 py-0.5 rounded-full inline-block min-w-[3.5rem] text-center"
                      style="background: var(--status-ok-bg); color: var(--status-ok-text);"
                    >{{ grossMargin(row) }}%</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>
