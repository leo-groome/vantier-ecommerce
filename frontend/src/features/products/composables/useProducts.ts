import { useProductsStore } from '../store'

export function useProducts() {
  const store = useProductsStore()
  return { store }
}
