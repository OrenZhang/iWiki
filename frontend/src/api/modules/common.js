import http from '../index'

export const changeLangAPI = (langCode) => {
    return new Promise((resolve, reject) => {
        http.post(
            '/i18n/',
            {
                language: langCode
            }
        ).then(res => resolve(res), err => reject(err))
    })
}

export const getConfAPI = (key) => {
    return new Promise((resolve, reject) => {
        http.post(
            '/conf/common/',
            {
                cKey: key
            }
        ).then(res => resolve(res), err => reject(err))
    })
}

export const uploadFileAPI = (url, data) => {
    return new Promise((resolve, reject) => {
        http({
            url: url,
            method: 'POST',
            headers: { 'Content-Type':'multipart/form-data' },
            data: data
        }).then(res => resolve(res), err => reject(err))
    })
}

export const sendRepassCodeAPI = (username, phone) => {
    return new Promise((resolve, reject) => {
        http.post(
            '/sms/send/repass_code/',
            { username, phone }
        ).then(res => resolve(res), err => reject(err))
    })
}

export const sendRegistryCodeAPI = (phone) => {
    return new Promise((resolve, reject) => {
        http.post(
            '/sms/send/register_code/',
            {
                phone: phone
            }
        ).then(res => resolve(res), err => reject(err))
    })
}

export const loadVersionDataAPI = (vid) => {
    return new Promise((resolve, reject) => {
        http.get(
            '/version/log/' + vid + '/'
        ).then(res => resolve(res), err => reject(err))
    })
}

export const listVersionAPI = () => {
    return new Promise((resolve, reject) => {
        http.get(
            '/version/log/'
        ).then(res => resolve(res), err => reject(err))
    })
}
