import React from 'react'
import { Composition } from 'remotion'
import { HeroIntro } from './compositions/HeroIntro'
import { ProductReveal } from './compositions/ProductReveal'

export const Root: React.FC = () => {
  return (
    <>
      <Composition
        id="HeroIntro"
        component={HeroIntro}
        durationInFrames={300}   // 10s @ 30fps
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="ProductReveal"
        component={ProductReveal}
        durationInFrames={540}   // 18s @ 30fps
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  )
}
