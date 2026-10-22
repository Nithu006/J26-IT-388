import { defineConfig } from 'vite';
export default defineConfig({
  server: { host: '127.0.0.1', port: 5173, strictPort: true },
  test: { environment: 'jsdom', setupFiles: ['./src/tests/setup.js'],
    include: ['src/tests/**/*.test.{js,jsx}'] }
});
