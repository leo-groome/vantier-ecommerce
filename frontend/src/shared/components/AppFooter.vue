<script setup lang="ts">
const newsletterUrl = 'https://lasilentluxury.substack.com/'
</script>

<template>
  <footer class="bg-[color:var(--color-obsidian)] text-[color:var(--color-ivory)]">
    <!-- Gold top rule -->
    <div class="w-full h-px bg-[color:var(--color-amber-accent)]" />

    <!-- Main grid -->
    <div class="max-w-[var(--container-max)] mx-auto px-[var(--spacing-container)] py-16 grid grid-cols-1 md:grid-cols-3 gap-12 md:gap-8">

      <!-- Left: Brand -->
      <div class="flex flex-col gap-4">
        <img
          src="/Logos y tipografia/LOGOTIPO BLANCO VANTIER.svg"
          alt="Vantier"
          class="h-6 w-auto mb-2"
        />
        <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] opacity-40 leading-relaxed">
          Los Angeles — México
        </p>
        <p class="text-[length:var(--text-micro)] opacity-30 leading-relaxed max-w-[220px] mt-2">
          Silent luxury. Crafted for those who move with purpose.
        </p>
      </div>

      <!-- Center: Collection links -->
      <div class="flex flex-col gap-4">
        <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-display)] opacity-40">The Collection</p>
        <nav class="flex flex-col gap-3" aria-label="Collection navigation">
          <RouterLink
            v-for="item in [
              { label: 'Polo Atelier', to: '/shop?line=polo-atelier' },
              { label: 'Signature', to: '/shop?line=signature' },
              { label: 'Essential', to: '/shop?line=essential' },
              { label: 'All Products', to: '/shop' },
            ]"
            :key="item.to"
            :to="item.to"
            class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] opacity-60 hover:opacity-100 transition-opacity duration-[var(--duration-fast)] w-fit"
          >
            {{ item.label }}
          </RouterLink>
        </nav>
      </div>

      <!-- Right: Newsletter + social -->
      <div class="flex flex-col gap-6">
        <div>
          <p class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-display)] opacity-40 mb-4">Stay in the know</p>
          <a
            :href="newsletterUrl"
            target="_blank"
            rel="noopener noreferrer"
            data-newsletter-cta
            class="inline-flex items-center gap-2 border border-[color:var(--color-ivory)]/30 px-5 py-2.5 text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] text-[color:var(--color-ivory)] hover:border-[color:var(--color-amber-accent)] hover:text-[color:var(--color-amber-accent)] transition-colors duration-[var(--duration-normal)]"
          >
            Unirme al círculo
            <svg class="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M5 12h14M12 5l7 7-7 7" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </a>
        </div>

        <!-- Social -->
        <div class="flex flex-col gap-3">
          <!-- Instagram -->
          <div class="flex items-center gap-3">
            <a
              href="https://www.instagram.com/vantier_worldwide?igsh=MW1hZWFtaXpsOXk5Zw%3D%3D&utm_source=qr"
              target="_blank"
              rel="noopener noreferrer"
              class="opacity-40 hover:opacity-100 transition-opacity duration-[var(--duration-fast)]"
              aria-label="Instagram"
            >
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <rect x="2" y="2" width="20" height="20" rx="5" ry="5"/>
                <circle cx="12" cy="12" r="4"/>
                <circle cx="17.5" cy="6.5" r="0.5" fill="currentColor"/>
              </svg>
            </a>
            <span class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] opacity-30">@vantier_worldwide</span>
          </div>
          <!-- LinkedIn -->
          <div class="flex items-center gap-3">
            <a
              href="https://linkedin.com/in/vantier-silent-luxury-3993823b1"
              target="_blank"
              rel="noopener noreferrer"
              class="opacity-40 hover:opacity-100 transition-opacity duration-[var(--duration-fast)]"
              aria-label="LinkedIn"
            >
              <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <rect x="2" y="2" width="20" height="20" rx="4" ry="4"/>
                <path d="M8 11v5M8 8v.01M12 16v-5M12 11a3 3 0 0 1 6 0v5M18 16v-5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </a>
            <span class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] opacity-30">Vantier Silent Luxury</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom bar -->
    <div class="border-t border-[color:var(--color-ivory)]/8">
      <div class="max-w-[var(--container-max)] mx-auto px-[var(--spacing-container)] py-5 flex flex-col sm:flex-row items-center justify-between gap-3">
        <p class="text-[length:var(--text-micro)] opacity-25 uppercase tracking-[var(--tracking-label)]">
          © 2025 Vantier LLC
        </p>
        <nav class="flex items-center gap-6" aria-label="Legal navigation">
          <RouterLink
            v-for="item in [
              { label: 'Privacy', to: '/privacy' },
              { label: 'Shipping', to: '/shipping' },
              { label: 'Exchange Policy', to: '/exchange' },
            ]"
            :key="item.to"
            :to="item.to"
            class="text-[length:var(--text-micro)] uppercase tracking-[var(--tracking-label)] opacity-25 hover:opacity-60 transition-opacity duration-[var(--duration-fast)]"
          >
            {{ item.label }}
          </RouterLink>
        </nav>
      </div>
    </div>
  </footer>
</template>
