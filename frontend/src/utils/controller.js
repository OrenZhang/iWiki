import i18n from '../locale'

export function setTitle (title) {
    if (title) {
        document.title = title + ' - ' + i18n.global.t('wikiRepo')
    } else {
        document.title = i18n.global.t('wikiRepo')
    }
}