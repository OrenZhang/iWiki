import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import prismjs from 'vite-plugin-prismjs'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'

export default defineConfig({
    plugins: [
        vue(),
        prismjs({
            languages: [
                'bash',
                'c', 'cpp', 'css', 'csv',
                'django', 'docker',
                'go',
                'ini',
                'java', 'javascript', 'js', 'json',
                'latex', 'lua',
                'markdown', 'matlab',
                'php', 'python',
                'sql',
                'vim',
                'yaml'
            ],
        }),
        AutoImport({
            resolvers: [ElementPlusResolver()],
        }),
        Components({
            resolvers: [ElementPlusResolver()],
        }),
    ],
    base: '/',
    publicDir: 'public',
    server: {
        host: 'dev.wiki.incv.net',
        port: 8080
    },
    css: {
        preprocessorOptions:
            {
                scss:
                    {
                        charset: false // 禁用 Charset 提醒
                    }
            }
    },
    build: {
        rollupOptions: {
            output: {
                manualChunks (id) {
                    if (id.includes('node_modules/element-plus')) {
                        return 'element-plus'
                    }
                    if (id.includes('node_modules/echarts')) {
                        return 'echarts'
                    }
                }
            }
        },
        chunkSizeWarningLimit: 2000
    }
})
