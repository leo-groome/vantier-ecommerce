import { test, expect } from '@playwright/test'

test('checkout redirects to login when unauthenticated', async ({ page }) => {
  await page.goto('/checkout')
  await expect(page).toHaveURL(/\/auth\/login/)
})

test('admin redirects to login when unauthenticated', async ({ page }) => {
  await page.goto('/admin/dashboard')
  await expect(page).toHaveURL(/\/auth\/login/)
})
