import {defineConfig} from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
    plugins: [react()],
    server: {
        proxy: {
            '/browse': 'http://127.0.0.1:5000',
            '/vocabulary': 'http://127.0.0.1:5000',
            '/facet': 'http://127.0.0.1:5000',
            '/user-info': 'http://127.0.0.1:5000',
            '/login': 'http://127.0.0.1:5000',
            '/logout': 'http://127.0.0.1:5000',
            '/review': 'http://127.0.0.1:5000',
            '/thumb': 'http://127.0.0.1:5000',
        }
    }
});
