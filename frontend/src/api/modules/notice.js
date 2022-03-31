import http from '../index'

export const getNoticeCommonAPI = (page, size) => new Promise(
    (resolve, reject) => {
        http.get(
            '/notice/common/?page=' + page +'&size=' + size
        ).then(res => resolve(res), err => reject(err))
    }
)

export const readNoticeAPI = (id) => new Promise(
    (resolve, reject) => {
        http.post(
            '/notice/common/' + id +'/read/'
        ).then(res => resolve(res), err => reject(err))
    }
)

export const readAllNoticeAPI = () => new Promise(
    (resolve, reject) => {
        http.post(
            '/notice/common/read_all/'
        ).then(res => resolve(res), err => reject(err))
    }
)

