<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface RevCard {
  label: string
  value: string
  sub: string
  delta: string
  deltaUp: boolean
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
const monthRows = ref<MonthRow[]>([])
const loading = ref(true)
const period = ref<'week' | 'month' | 'quarter'>('month')

onMounted(() => {
  setTimeout(() => {
    revCards.value = [
      { label: 'Gross Revenue',    value: '$58,400', sub: 'April 2024',      delta: '+18%', deltaUp: true  },
      { label: 'Net Revenue',      value: '$51,230', sub: 'After discounts', delta: '+14%', deltaUp: true  },
      { label: 'Avg Order Value',  value: '$170.80', sub: '342 orders',      delta: '+6%',  deltaUp: true  },
      { label: 'Refunds / Exch.',  value: '$1,840',  sub: '11 orders',       delta: '-3%',  deltaUp: true  },
    ]

    costRows.value = [
      { category: 'Cost of Goods (COGS)',  amount: 23360, pct: 40 },
      { category: 'Shipping & Fulfillment', amount: 5840,  pct: 10 },
      { category: 'Discounts Applied',      amount: 3504,  pct: 6  },
      { category: 'Payment Processing',     amount: 1752,  pct: 3  },
      { category: 'Returns & Exchanges',    amount: 1840,  pct: 3  },
    ]

    monthRows.value = [
      { month: 'Nov 2023', revenue: 31200, cogs: 12480, gross: 18720 },
      { month: 'Dec 2023', revenue: 48900, cogs: 19560, gross: 29340 },
      { month: 'Jan 2024', revenue: 27500, cogs: 11000, gross: 16500 },
      { month: 'Feb 2024', revenue: 33800, cogs: 13520, gross: 20280 },
      { month: 'Mar 2024', revenue: 49400, cogs: 19760, gross: 29640 },
      { month: 'Apr 2024', revenue: 58400, cogs: 23360, gross: 35040 },
    ]

    loading.value = false
  }, 400)
})

function grossMargin(row: MonthRow) {
  return ((row.gross / row.revenue) * 100).toFixed(1)
}

const maxRevenue = 60000
</script>

<template>
  <div class="space-y-8">
    <!-- Header -->
    <div class="flex items-end justify-between gap-4">
      <div>
        <p class="text-xs uppercase tracking-widest text-[color:var(--color-border-strong)]">Financial Overview</p>
        <h1 class="mt-1 text-2xl font-semibold uppercase tracking-wider text-[color:var(--color-obsidian)]">Financials</h1>
      </div>
      <!-- Period selector -->
      <div class="flex gap-1 border border-[color:var(--color-border)] rounded-[var(--radius-md)] p-0.5 bg-[color:var(--color-warm-beige)]">
        <button
          v-for="p in ['week', 'month', 'quarter']"
          :key="p"
          class="px-3 py-1.5 text-xs uppercase tracking-widest rounded-[var(--radius-sm)] transition-colors duration-[var(--duration-fast)]"
          :class="period === p
            ? 'bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)]'
            : 'text-[color:var(--color-border-strong)] hover:text-[color:var(--color-obsidian)]'"
          @click="period = p as any"
        >{{ p }}</button>
      </div>
    </div>

    <!-- Skeleton -->
    <div v-if="loading" class="space-y-4">
      <div class="grid grid-cols-2 xl:grid-cols-4 gap-4">
        <div v-for="i in 4" :key="i" class="h-28 rounded-[var(--radius-md)] bg-[color:var(--color-warm-beige-dk)] animate-pulse" />
      </div>
    </div>

    <template v-else>
      <!-- Revenue cards -->
      <div class="grid grid-cols-2 xl:grid-cols-4 gap-4">
        <div
          v-for="card in revCards"
          :key="card.label"
          class="bg-[color:var(--color-ivory)] border border-[color:var(--color-border)] rounded-[var(--radius-md)] p-5 flex flex-col gap-3"
        >
          <p class="text-xs uppercase tracking-widest text-[color:var(--color-border-strong)]">{{ card.label }}</p>
          <div class="flex items-end justify-between gap-2">
            <div>
              <p class="text-3xl font-semibold tracking-tight text-[color:var(--color-obsidian)]">{{ card.value }}</p>
              <p class="mt-0.5 text-xs text-[color:var(--color-border-strong)]">{{ card.sub }}</p>
            </div>
            <span
              class="text-xs font-medium px-2 py-0.5 rounded-full flex-shrink-0"
              :class="card.deltaUp ? 'bg-emerald-50 text-emerald-700' : 'bg-red-50 text-red-600'"
            >{{ card.delta }}</span>
          </div>
        </div>
      </div>

      <!-- Revenue bar chart -->
      <div class="bg-[color:var(--color-ivory)] border border-[color:var(--color-border)] rounded-[var(--radius-md)] p-6">
        <p class="text-xs uppercase tracking-widest font-semibold text-[color:var(--color-obsidian)] mb-6">Monthly Revenue vs. COGS</p>
        <div class="space-y-3">
          <div v-for="row in monthRows" :key="row.month" class="grid grid-cols-[80px_1fr_80px] items-center gap-3">
            <p class="text-xs text-[color:var(--color-border-strong)] text-right">{{ row.month }}</p>
            <div class="relative h-6 bg-[color:var(--color-warm-beige)] rounded-sm overflow-hidden">
              <!-- Revenue bar -->
              <div
                class="absolute inset-y-0 left-0 bg-[color:var(--color-obsidian)] opacity-20 rounded-sm transition-[width] duration-[var(--duration-slow)]"
                :style="{ width: `${(row.revenue / maxRevenue) * 100}%` }"
              />
              <!-- Gross bar -->
              <div
                class="absolute inset-y-0 left-0 bg-[color:var(--color-obsidian)] rounded-sm transition-[width] duration-[var(--duration-slow)]"
                :style="{ width: `${(row.gross / maxRevenue) * 100}%` }"
              />
            </div>
            <p class="text-xs font-medium text-[color:var(--color-obsidian)]">${{ (row.gross / 1000).toFixed(1) }}k</p>
          </div>
        </div>
        <div class="flex items-center gap-4 mt-4 pt-4 border-t border-[color:var(--color-border)]">
          <div class="flex items-center gap-1.5 text-xs text-[color:var(--color-border-strong)]">
            <span class="w-3 h-2 bg-[color:var(--color-obsidian)] opacity-20 rounded-sm" /> Revenue
          </div>
          <div class="flex items-center gap-1.5 text-xs text-[color:var(--color-border-strong)]">
            <span class="w-3 h-2 bg-[color:var(--color-obsidian)] rounded-sm" /> Gross Profit
          </div>
        </div>
      </div>

      <!-- Cost breakdown + Monthly table side by side -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Cost breakdown -->
        <div class="bg-[color:var(--color-ivory)] border border-[color:var(--color-border)] rounded-[var(--radius-md)] p-6">
          <p class="text-xs uppercase tracking-widest font-semibold text-[color:var(--color-obsidian)] mb-4">Cost Breakdown — April 2024</p>
          <div class="space-y-3">
            <div v-for="row in costRows" :key="row.category" class="space-y-1.5">
              <div class="flex justify-between text-sm">
                <span class="text-[color:var(--color-obsidian)]">{{ row.category }}</span>
                <span class="font-medium text-[color:var(--color-obsidian)]">${{ row.amount.toLocaleString() }}</span>
              </div>
              <div class="h-1.5 bg-[color:var(--color-warm-beige)] rounded-full overflow-hidden">
                <div
                  class="h-full bg-[color:var(--color-obsidian)] rounded-full transition-[width] duration-[var(--duration-slow)]"
                  :style="{ width: `${row.pct}%` }"
                />
              </div>
              <p class="text-xs text-[color:var(--color-border-strong)] text-right">{{ row.pct }}% of revenue</p>
            </div>
          </div>
        </div>

        <!-- Monthly P&L table -->
        <div class="bg-[color:var(--color-ivory)] border border-[color:var(--color-border)] rounded-[var(--radius-md)] overflow-hidden">
          <div class="px-6 py-4 border-b border-[color:var(--color-border)]">
            <p class="text-xs uppercase tracking-widest font-semibold text-[color:var(--color-obsidian)]">Monthly P&L Summary</p>
          </div>
          <table class="w-full text-sm">
            <thead>
              <tr class="bg-[color:var(--color-warm-beige)] text-xs uppercase tracking-widest text-[color:var(--color-border-strong)]">
                <th class="px-5 py-2.5 text-left font-medium">Month</th>
                <th class="px-5 py-2.5 text-right font-medium">Revenue</th>
                <th class="px-5 py-2.5 text-right font-medium">COGS</th>
                <th class="px-5 py-2.5 text-right font-medium">Gross</th>
                <th class="px-5 py-2.5 text-right font-medium">Margin</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-[color:var(--color-border)]">
              <tr
                v-for="row in monthRows"
                :key="row.month"
                class="hover:bg-[color:var(--color-warm-beige)] transition-colors duration-[var(--duration-fast)]"
              >
                <td class="px-5 py-3 text-[color:var(--color-obsidian)]">{{ row.month }}</td>
                <td class="px-5 py-3 text-right text-[color:var(--color-border-strong)]">${{ row.revenue.toLocaleString() }}</td>
                <td class="px-5 py-3 text-right text-red-500">-${{ row.cogs.toLocaleString() }}</td>
                <td class="px-5 py-3 text-right font-medium text-[color:var(--color-obsidian)]">${{ row.gross.toLocaleString() }}</td>
                <td class="px-5 py-3 text-right">
                  <span class="text-xs font-medium text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full">{{ grossMargin(row) }}%</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>
  </div>
</template>
