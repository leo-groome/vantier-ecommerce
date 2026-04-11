import React from 'react'
import {
  AbsoluteFill,
  Sequence,
  useCurrentFrame,
  interpolate,
  Easing,
} from 'remotion'

/**
 * ProductReveal — 18s (540 frames @ 30fps), 3 scenes × 180f each
 *
 * Each scene: product line name fades in from bottom, holds, fades out.
 * Intended as a product-line showcase for the home hero area.
 */

interface SceneProps {
  label: string
  subtitle: string
  bgColor: string
  textColor: string
}

const Scene: React.FC<SceneProps & { localFrame: number; totalFrames: number }> = ({
  label,
  subtitle,
  bgColor,
  textColor,
  localFrame,
  totalFrames,
}) => {
  const fadeIn  = interpolate(localFrame, [0, 40], [0, 1], { extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic) })
  const slideY  = interpolate(localFrame, [0, 40], [20, 0], { extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic) })
  const fadeOut = interpolate(localFrame, [totalFrames - 30, totalFrames], [1, 0], { extrapolateLeft: 'clamp', easing: Easing.in(Easing.cubic) })
  const opacity = Math.min(fadeIn, fadeOut)

  return (
    <AbsoluteFill
      style={{
        backgroundColor: bgColor,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 16,
        fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif',
      }}
    >
      <div
        style={{
          fontSize: 56,
          fontWeight: 700,
          letterSpacing: '0.18em',
          textTransform: 'uppercase',
          color: textColor,
          opacity,
          transform: `translateY(${slideY}px)`,
        }}
      >
        {label}
      </div>
      <div
        style={{
          fontSize: 18,
          fontWeight: 300,
          letterSpacing: '0.08em',
          color: textColor,
          opacity: opacity * 0.7,
          transform: `translateY(${slideY * 1.4}px)`,
          fontFamily: '"Playfair Display", Georgia, serif',
          fontStyle: 'italic',
        }}
      >
        {subtitle}
      </div>
    </AbsoluteFill>
  )
}

const SCENES: SceneProps[] = [
  { label: 'Polo Atelier',  subtitle: 'Crafted for the discerning.',     bgColor: 'oklch(97% 0.003 90)',   textColor: 'oklch(8% 0.005 250)' },
  { label: 'Signature',     subtitle: 'Understated. Unforgettable.',     bgColor: 'oklch(22% 0.045 260)',  textColor: 'oklch(97% 0.003 90)' },
  { label: 'Essential',     subtitle: 'The foundation of your wardrobe.',bgColor: 'oklch(88% 0.018 80)',   textColor: 'oklch(8% 0.005 250)' },
]

const FRAMES_PER_SCENE = 180

export const ProductReveal: React.FC = () => {
  const frame = useCurrentFrame()

  return (
    <AbsoluteFill>
      {SCENES.map((scene, i) => {
        const start = i * FRAMES_PER_SCENE
        const localFrame = frame - start
        if (localFrame < 0 || localFrame >= FRAMES_PER_SCENE) return null
        return (
          <Scene
            key={scene.label}
            {...scene}
            localFrame={localFrame}
            totalFrames={FRAMES_PER_SCENE}
          />
        )
      })}
    </AbsoluteFill>
  )
}
