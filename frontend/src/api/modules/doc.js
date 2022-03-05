import http from '../index'

export const getDocCommonAPI = (docId) => {
    return new Promise((resolve, reject) => {
        http.get(
            '/doc/common/' + docId + '/'
        ).then(res => resolve(res), err => reject(err))
    })
}

export const loadDocPublicAPI = (size, page) => {
    return new Promise((resolve, reject) => {
        http.get(
            '/doc/public/?size=' + size + '&page=' + page
        ).then(res => resolve(res), err => reject(err))
    })
}

export const loadUserDocPublicAPI = (username, page) => {
    return new Promise((resolve, reject) => {
        http.get(
            '/doc/public/user_doc/?username=' + username + '&page=' + page
        ).then(res => resolve(res), err => reject(err))
    })
}

export const searchDocAPI = (keywords, page, size) => {
    return new Promise((resolve, reject) => {
        http.post(
            '/doc/search/?page=' + page + '&size=' + size,
            {
                searchKey: keywords
            }
        ).then(res => resolve(res), err => reject(err))
    })
}

export const createOrUpdateDocAPI = (url, method, data) => {
    return new Promise((resolve, reject) => {
        http({ url, method, data }).then(res => resolve(res), err => reject(err))
    })
}

export const loadDocDataManageAPI = (docId) => {
    return new Promise((resolve, reject) => {
        http.get(
            '/doc/manage/' + docId + '/'
        ).then(res => resolve(res), err => reject(err))
    })
}

export const listDocManageAPI = (page, keyword) => {
    return new Promise((resolve, reject) => {
        http.get(
            '/doc/manage/?page=' + page + '&searchKey=' + keyword
        ).then(res => resolve(res), err => reject(err))
    })
}

export const loadDocCollaboratorAPI = (docId) => {
    return new Promise((resolve, reject) => {
        http.get(
            '/doc/manage/' + docId + '/list_collaborator/'
        ).then(res => resolve(res), err => reject(err))
    })
}

export const removeDocCollaboratorAPI = (docId, uid) => {
    return new Promise((resolve, reject) => {
        http.post(
            '/doc/manage/' + docId + '/remove_collaborator/',
            { uid }
        ).then(res => resolve(res), err => reject(err))
    })
}

export const addDocCollaboratorAPI = (docId, uid) => {
    return new Promise((resolve, reject) => {
        http.post(
            '/doc/manage/' + docId + '/add_collaborator/',
            { uid }
        ).then(res => resolve(res), err => reject(err))
    })
}

export const checkDocEditingAPI = (docId) => {
    return new Promise((resolve, reject) => {
        http.get(
            '/doc/manage/' + docId + '/edit_status/'
        ).then(res => resolve(res), err => reject(err))
    })
}

export const loadRepoDocAPI = (repoId, keyword, page) => {
    return new Promise((resolve, reject) => {
        http.get(
            '/doc/common/?repo_id=' + repoId + '&searchKey=' + keyword + '&page=' + page
        ).then(res => resolve(res), err => reject(err))
    })
}

export const loadDocChartDataAPI = () => {
    return new Promise((resolve, reject) => {
        http.get(
            '/doc/public/recent_chart/'
        ).then(res => resolve(res), err => reject(err))
    })
}

export const loadHotRepoAPI = () => {
    return new Promise((resolve, reject) => {
        http.get(
            '/repo/public/hot_repo/'
        ).then(res => resolve(res), err => reject(err))
    })
}

export const loadRecentDocAPI = () => {
    return new Promise((resolve, reject) => {
        http.get(
            '/doc/public/recent/'
        ).then(res => resolve(res), err => reject(err))
    })
}

export const loadDocByRepoAdminAPI = (repoId, page, size, keyword) => {
    return new Promise((resolve, reject) => {
        http.get(
            '/repo/manage/' + repoId + '/load_doc/?page=' + page + '&size=' + size + '&searchKey=' + keyword
        ).then(res => resolve(res), err => reject(err))
    })
}

export const deleteDocAdminAPI = (repoId, docID) => {
    return new Promise((resolve, reject) => {
        http({
            url: '/repo/manage/' + repoId + '/delete_doc/',
            method: 'DELETE',
            data: { docID }
        }).then(res => resolve(res), err => reject(err))
    })
}

export const changeDocStatusAdminAPI = (docId, data) => {
    return new Promise((resolve, reject) => {
        http.patch(
            '/doc/manage/' + docId + '/',
            data
        ).then(res => resolve(res), err => reject(err))
    })
}

export const unPinDocAdminAPI = (repoId, docId) => {
    return new Promise((resolve, reject) => {
        http.post(
            '/repo/manage/' + repoId + '/unpin_doc/',
            {
                doc_id: docId
            }
        ).then(res => resolve(res), err => reject(err))
    })
}

export const pinDocAdminAPI = (repoId, data) => {
    return new Promise((resolve, reject) => {
        http.post(
            '/repo/manage/' + repoId + '/pin_doc/',
            data
        ).then(res => resolve(res), err => reject(err))
    })
}

export const deleteDocAPI = (docId) => {
    return new Promise((resolve, reject) => {
        http.delete(
            '/doc/manage/' + docId + '/'
        ).then(res => resolve(res), err => reject(err))
    })
}

export const checkDocCollaboratorAPI = (docId) => {
    return new Promise((resolve, reject) => {
        http.get(
            '/doc/common/' + docId + '/is_collaborator/'
        ).then(res => resolve(res), err => reject(err))
    })
}

export const loadPinDocAPI = (repoId) => {
    return new Promise((resolve, reject) => {
        http.get(
            '/doc/common/load_pin_doc/?repo_id=' + repoId
        ).then(res => resolve(res), err => reject(err))
    })
}
