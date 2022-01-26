import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import i18n from './locale'

import ElementPlus from 'element-plus'
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
import createHighlightLinesPlugin from '@kangc/v-md-editor/lib/plugins/highlight-lines/index'
import '@kangc/v-md-editor/lib/plugins/highlight-lines/highlight-lines.css'
import createCopyCodePlugin from '@kangc/v-md-editor/lib/plugins/copy-code/index'
import '@kangc/v-md-editor/lib/plugins/copy-code/copy-code.css'
import markdownItSub from 'markdown-it-sub'
import markdownItSup from 'markdown-it-sup'
import enUS from '@kangc/v-md-editor/lib/lang/en-US'
import zhCN from '@kangc/v-md-editor/lib/lang/zh-CN'

VueMarkdownEditor.use(vuepressTheme, {
    Prism,
    extend(md){
        md.set().use(markdownItSub)
        md.set().use(markdownItSup)
    },
    codeHighlightExtensionMap: {
        vue: 'html',
        shell: 'bash',
        sh: 'bash',
        'c++': 'cpp'
    },
})
VueMarkdownEditor.use(createEmojiPlugin())
VueMarkdownEditor.use(createKatexPlugin())
VueMarkdownEditor.use(createMermaidPlugin())
VueMarkdownEditor.use(createTodoListPlugin())
VueMarkdownEditor.use(createLineNumbertPlugin())
VueMarkdownEditor.use(createAlignPlugin())
VueMarkdownEditor.use(createHighlightLinesPlugin())
VueMarkdownEditor.use(createCopyCodePlugin())
const userLocale = localStorage.getItem('locale')
if (userLocale === 'en') {
    VueMarkdownEditor.lang.use('en-US', enUS)
} else {
    VueMarkdownEditor.lang.use('zh-CN', zhCN)
}

const app = createApp(App)
app.use(i18n)
app.use(store)
app.use(router)
app.use(VueMarkdownEditor)
app.use(ElementPlus)
app.mount('#app')