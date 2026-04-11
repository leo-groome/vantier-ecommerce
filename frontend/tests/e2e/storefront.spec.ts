import { test, expect } from '@playwright/test'

test('homepage redirects to /products', async ({ page }) => {
  await page.goto('/')
  await expect(page).toHaveURL('/products')
})

test('products page renders heading', async ({ page }) => {
  await page.goto('/products')
  await expect(page.getByRole('heading', { name: 'Colección' })).toBeVisible()
})

test('cart page renders heading', async ({ page }) => {
  await page.goto('/cart')
  await expect(page.getByRole('heading', { name: 'Carrito' })).toBeVisible()
})
