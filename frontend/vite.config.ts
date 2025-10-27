import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // Проксируем все запросы с префиксом /reports на backend
      '/reports': {
        target: 'http://localhost:3000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/reports/, '/reports'), // сохраняем путь, можно упростить
      },
      // Если есть другие пути API — можно добавить аналогично
    },
  },
})
