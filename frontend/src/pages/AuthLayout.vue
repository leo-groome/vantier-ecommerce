<template>
  <div class="min-h-screen flex">
    <!-- Left panel — brand -->
    <div
      class="hidden lg:flex lg:w-[55%] flex-col justify-between p-12 relative overflow-hidden"
      style="background: var(--color-obsidian);"
    >
      <!-- Background texture / gradient overlay -->
      <div class="absolute inset-0 pointer-events-none">
        <div
          class="absolute inset-0 opacity-[0.06]"
          style="background-image: repeating-linear-gradient(45deg, #fff 0, #fff 1px, transparent 0, transparent 50%); background-size: 24px 24px;"
        />
        <div
          class="absolute bottom-0 left-0 w-[600px] h-[600px] rounded-full opacity-[0.08]"
          style="background: radial-gradient(circle, #C9A84C 0%, transparent 70%); transform: translate(-30%, 30%);"
        />
      </div>

      <!-- Top wordmark -->
      <div class="relative z-10">
        <p
          class="text-[0.65rem] font-bold uppercase tracking-[0.35em]"
          style="color: #C9A84C;"
        >
          Vantier
        </p>
      </div>

      <!-- Center copy -->
      <div class="relative z-10 space-y-5">
        <div
          class="w-10 h-px"
          style="background: var(--color-gold);"
        />
        <h1
          class="text-[2.8rem] font-bold leading-[1.1] tracking-tight"
          style="color: #fff;"
        >
          Panel<br />Administrativo
        </h1>
        <p
          class="text-[0.82rem] leading-relaxed max-w-xs"
          style="color: rgba(255,255,255,0.4);"
        >
          Gestión de inventario, órdenes y envíos para Vantier Luxury.
        </p>
      </div>

      <!-- Bottom badge -->
      <div class="relative z-10">
        <p
          class="text-[0.6rem] uppercase tracking-widest"
          style="color: rgba(255,255,255,0.2);"
        >
          Acceso restringido · Solo personal autorizado
        </p>
      </div>
    </div>

    <!-- Right panel — form slot -->
    <div
      class="flex-1 flex items-center justify-center px-6 py-12"
      style="background: #fafaf9;"
    >
      <div class="w-full max-w-sm">
        <!-- Mobile wordmark (hidden on lg) -->
        <p
          class="lg:hidden text-center text-[0.65rem] font-bold uppercase tracking-[0.35em] mb-8"
          style="color: var(--color-obsidian);"
        >
          Vantier
        </p>
        <RouterView />
      </div>
    </div>
  </div>
</template>
