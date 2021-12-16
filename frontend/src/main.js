import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import http from './api'
import store from './store'
import VueAxios from 'vue-axios'
import i18n from './locale'

import 'element-plus/dist/index.css'

import VueMarkdownEditor from '@kangc/v-md-editor'
import '@kangc/v-md-editor/lib/style/base-editor.css'
import vuepressTheme from '@kangc/v-md-editor/lib/theme/vuepress.js'
import '@kangc/v-md-editor/lib/theme/style/vuepress.css'
import Prism from 'prismjs'
import createEmojiPlugin from '@kangc/v-md-editor/lib/plugins/emoji/index'
import '@kangc/v-md-editor/lib/plugins/emoji/emoji.css'
import createKatexPlugin from '@kangc/v-md-editor/lib/plugins/katex/cdn'
import createMermaidPlugin from '@kangc/v-md-editor/lib/plugins/mermaid/cdn'
import '@kangc/v-md-editor/lib/plugins/mermaid/mermaid.css'
import createTodoListPlugin from '@kangc/v-md-editor/lib/plugins/todo-list/index'
import '@kangc/v-md-editor/lib/plugins/todo-list/todo-list.css'
import createLineNumbertPlugin from '@kangc/v-md-editor/lib/plugins/line-number/index'
import createAlignPlugin from '@kangc/v-md-editor/lib/plugins/align'
import markdownItSub from 'markdown-it-sub'
import markdownItSup from 'markdown-it-sup'
import enUS from '@kangc/v-md-editor/lib/lang/en-US'
import zhCN from '@kangc/v-md-editor/lib/lang/zh-CN'

VueMarkdownEditor.use(vuepressTheme, {
    Prism,
    extend(md){
        md.set().use(markdownItSub)
        md.set().use(markdownItSup)
    }
})
VueMarkdownEditor.use(createEmojiPlugin())
VueMarkdownEditor.use(createKatexPlugin())
VueMarkdownEditor.use(createMermaidPlugin())
VueMarkdownEditor.use(createTodoListPlugin())
VueMarkdownEditor.use(createLineNumbertPlugin())
VueMarkdownEditor.use(createAlignPlugin())
const userLocale = sessionStorage.getItem('locale')
if (userLocale === 'en') {
    VueMarkdownEditor.lang.use('en-US', enUS)
} else {
    VueMarkdownEditor.lang.use('zh-CN', zhCN)
}


const app = createApp(App)
app.use(router)
app.use(store)
app.use(i18n)
app.use(VueAxios, http)
app.use(VueMarkdownEditor)
app.mount('#app')