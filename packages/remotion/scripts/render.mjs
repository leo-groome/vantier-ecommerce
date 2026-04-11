#!/usr/bin/env node
/**
 * render.mjs — offline pre-render script for Vantier Remotion compositions
 *
 * Usage:
 *   node scripts/render.mjs hero-intro
 *   node scripts/render.mjs product-reveal
 *
 * Output lands in ../../frontend/public/video/ so Vue can serve them.
 *
 * Requires:
 *   - @remotion/bundler and @remotion/renderer installed in this package
 *   - Run from packages/remotion/ directory or via npm script
 */

import path from 'path'
import { fileURLToPath } from 'url'
import { bundle } from '@remotion/bundler'
import { renderMedia, selectComposition } from '@remotion/renderer'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

const COMPOSITIONS = {
  'hero-intro':     { id: 'HeroIntro',     out: 'hero-intro.mp4' },
  'product-reveal': { id: 'ProductReveal', out: 'product-reveal.mp4' },
}

const key = process.argv[2]
if (!key || !COMPOSITIONS[key]) {
  console.error(`Usage: node scripts/render.mjs <${Object.keys(COMPOSITIONS).join(' | ')}>`)
  process.exit(1)
}

const { id, out } = COMPOSITIONS[key]
const entryPoint = path.join(__dirname, '..', 'src', 'index.ts')
const outputDir  = path.join(__dirname, '..', '..', '..', 'frontend', 'public', 'video')

console.log(`Bundling…`)
const bundleLocation = await bundle({
  entryPoint,
  webpackOverride: (config) => config,
})

console.log(`Selecting composition: ${id}`)
const composition = await selectComposition({
  serveUrl: bundleLocation,
  id,
})

const outputLocation = path.join(outputDir, out)
console.log(`Rendering → ${outputLocation}`)
await renderMedia({
  composition,
  serveUrl: bundleLocation,
  codec: 'h264',
  outputLocation,
})

console.log(`Done: ${out}`)
