import { Config } from '@remotion/cli/config'

Config.setVideoImageFormat('jpeg')
Config.setCodec('h264')
Config.setWidth(1920)
Config.setHeight(1080)
Config.setFps(30)
Config.setPixelFormat('yuv420p')
// Overridable per-composition via CLI flags
