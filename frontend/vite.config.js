/*
 * MIT License
 *
 * Copyright (c) 2021 Oren Zhang
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import prismjs from 'vite-plugin-prismjs';

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
        'yaml',
      ],
    }),
  ],
  base: '/',
  publicDir: 'public',
  server: {
    host: 'dev.wiki.incv.net',
    port: 8080,
  },
  css: {
    preprocessorOptions:
            {
              scss:
                    {
                      charset: false, // 禁用 Charset 提醒
                    },
            },
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules/element-plus')) {
            return 'element-plus';
          }
          if (id.includes('node_modules/echarts')) {
            return 'echarts';
          }
        },
      },
    },
    chunkSizeWarningLimit: 2000,
  },
});
