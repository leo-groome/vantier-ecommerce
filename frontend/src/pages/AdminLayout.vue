<template>
  <div class="min-h-screen flex">
    <aside class="w-56 border-r px-4 py-6 flex flex-col gap-2">
      <p class="text-xs font-bold uppercase tracking-widest mb-4">Admin</p>
      <RouterLink to="/admin/dashboard">Dashboard</RouterLink>
      <RouterLink to="/admin/inventory">Inventario</RouterLink>
      <RouterLink to="/admin/orders">Órdenes</RouterLink>
      <RouterLink to="/admin/purchases">Compras</RouterLink>
      <RouterLink to="/admin/discounts">Descuentos</RouterLink>
      <RouterLink to="/admin/finances">Finanzas</RouterLink>
      <RouterLink to="/admin/users">Usuarios</RouterLink>
    </aside>
    <main class="flex-1 p-6">
      <RouterView />
    </main>
  </div>
</template>
