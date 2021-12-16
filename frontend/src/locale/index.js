import { createI18n } from 'vue-i18n'
import zh from './zh-hans'
import en from './en'

const i18n = createI18n({
    locale: sessionStorage.getItem('locale') === 'en' ? 'en' : 'zh',
    fallbackLocale: 'zh',
    messages: {
        zh,
        en
    }
})

export default i18n