import {config} from 'dotenv'
import {resolve} from 'path'

config({path: resolve(__dirname, ".env")})

export const VITE_API_KEY = process.env.VITE_API_KEY