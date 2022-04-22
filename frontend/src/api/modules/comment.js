import http from '../index'

export const loadCommentAPI = (docId, size, page) => {
    return new Promise((resolve, reject) => {
        http.get(
            '/doc/comments/?doc_id=' + docId + '&size=' + size + '&page=' + page
        ).then(res => resolve(res), err => reject(err))
    })
}

export const createCommentAPI = (doc_id, reply_to, content) => {
    return new Promise((resolve, reject) => {
        http.post(
            '/doc/comment/',
            { doc_id, reply_to, content }
        ).then(res => resolve(res), err => reject(err))
    })
}

export const updateCommentAPI = (id, text) => {
    return new Promise((resolve, reject) => {
        http.patch(
            '/doc/comment/' + id + '/',
            {
                content: text
            }
        ).then(res => resolve(res), err => reject(err))
    })
}

export const deleteCommentAPI = (id) => {
    return new Promise((resolve, reject) => {
        http.delete(
            '/doc/comment/' + id + '/'
        ).then(res => resolve(res), err => reject(err))
    })
}

export const loadUserCommentAPI = (page, size, searchKey) => {
    return new Promise((resolve, reject) => {
        http.get(
            '/doc/comment/all/?page=' + page + '&size=' + size + '&search_key=' + searchKey
        ).then(res => resolve(res), err => reject(err))
    })
}
