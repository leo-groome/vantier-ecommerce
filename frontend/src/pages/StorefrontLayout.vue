<template>
  <div class="min-h-screen flex flex-col">
    <header class="border-b px-6 py-4 flex items-center justify-between">
      <RouterLink to="/" class="text-xl font-semibold tracking-widest uppercase">Vantier</RouterLink>
      <nav class="flex gap-6 text-sm">
        <RouterLink to="/products">Colección</RouterLink>
        <RouterLink to="/cart">Carrito</RouterLink>
        <RouterLink to="/account">Cuenta</RouterLink>
      </nav>
    </header>
    <main class="flex-1">
      <RouterView />
    </main>
    <footer class="border-t px-6 py-4 text-center text-xs text-gray-500">
      © {{ new Date().getFullYear() }} Vantier
    </footer>
  </div>
</template>
