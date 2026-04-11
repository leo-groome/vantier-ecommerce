import React from 'react'
import {
  AbsoluteFill,
  Sequence,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Easing,
} from 'remotion'

/**
 * HeroIntro — 10s (300 frames @ 30fps)
 *
 * Scene 1 (0–90f):   Brand name fades in with letter-spacing expand
 * Scene 2 (90–210f): Tagline "Silent Luxury." slides up and fades in
 * Scene 3 (210–300f): Both elements settle, subtle parallax hold
 */
export const HeroIntro: React.FC = () => {
  const frame = useCurrentFrame()
  const { fps } = useVideoConfig()

  // Brand name — letter-spacing expand + opacity
  const brandOpacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: 'clamp' })
  const brandLetterSpacing = interpolate(frame, [0, 60], [0.02, 0.25], {
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  })

  // Tagline — translate up + opacity, delayed to frame 90
  const taglineOpacity = interpolate(frame, [90, 140], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  })
  const taglineY = interpolate(frame, [90, 140], [24, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  })

  return (
    <AbsoluteFill
      style={{
        backgroundColor: 'oklch(97% 0.003 90)', // --color-ivory
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 32,
        fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif',
      }}
    >
      {/* Brand name */}
      <div
        style={{
          fontSize: 80,
          fontWeight: 700,
          letterSpacing: `${brandLetterSpacing}em`,
          textTransform: 'uppercase',
          color: 'oklch(8% 0.005 250)', // --color-obsidian
          opacity: brandOpacity,
        }}
      >
        VANTIER
      </div>

      {/* Tagline */}
      <div
        style={{
          fontSize: 24,
          fontWeight: 300,
          letterSpacing: '0.12em',
          color: 'oklch(8% 0.005 250)',
          opacity: taglineOpacity,
          transform: `translateY(${taglineY}px)`,
          fontFamily: '"Playfair Display", Georgia, serif',
          fontStyle: 'italic',
        }}
      >
        Silent Luxury.
      </div>
    </AbsoluteFill>
  )
}
