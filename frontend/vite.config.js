import { defineConfig } from 'vite'
import react, { reactCompilerPreset } from '@vitejs/plugin-react'
import babel from '@rolldown/plugin-babel'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    tailwindcss(),
    react(),
    babel({ presets: [reactCompilerPreset()] })
  ],
  server: {
    // Usa a porta da env PORT quando definida (ex.: painéis de preview);
    // sem ela, mantém a padrão 5173.
    port: Number(process.env.PORT) || 5173,
    proxy: {
      // Backend FinKAN (FastAPI/uvicorn). Em dev o frontend usa caminhos
      // relativos (/api/...) e o proxy evita CORS; em produção configure
      // VITE_API_BASE_URL apontando para a API.
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
