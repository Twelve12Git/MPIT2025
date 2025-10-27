import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
    const env: Record<string, string> = loadEnv(mode, process.cwd(), 'VITE_');

    const PORT: number = parseInt(env.VITE_PORT ?? 5173);
    const HOST: string | undefined = env.VITE_HOST ?? 'localhost';

    return {
        plugins: [react()],
        base: "",
        server: {
            port: PORT,
            host: HOST
        }
    }
})
