import http from '../index'

export const changeRepoTypeAPI = (repoId, value) => {
    return new Promise((resolve, reject) => {
        http.patch(
            '/repo/manage/' + repoId + '/',
            {
                r_type: value
            }
        ).then(res => resolve(res), err => reject(err))
    })
}

export const loadManageRepoAPI = () => {
    return new Promise((resolve, reject) => {
        http.get(
            '/repo/manage/load_repo/'
        ).then(res => resolve(res), err => reject(err))
    })
}

export const checkOwnerAPI = (repoId) => {
    return new Promise((resolve, reject) => {
        http.get(
            '/repo/manage/' + repoId + '/is_owner/'
        ).then(res => resolve(res), err => reject(err))
    })
}

export const deleteRepoAPI = (repoId) => {
    return new Promise((resolve, reject) => {
        http.delete(
            '/repo/manage/' + repoId + '/'
        ).then(res => resolve(res), err => reject(err))
    })
}

export const loadRepoAPI = (page = 0, searchKey = '') => {
    const url = page? '/repo/common/?page=' + page + '&searchKey=' + searchKey : '/repo/common/'
    return new Promise((resolve, reject) => {
        http.get(
            url
        ).then(res => resolve(res), err => reject(err))
    })
}

export const loadRepoDetailAPI = (repoId) => {
    return new Promise((resolve, reject) => {
        http.get(
            '/repo/common/' + repoId + '/'
        ).then(res => resolve(res), err => reject(err))
    })
}

export const loadRepoWithUserAPI = (page, keyword) => {
    return new Promise((resolve, reject) => {
        http.get(
            '/repo/common/with_user/?page=' + page + '&searchKey=' + keyword
        ).then(res => resolve(res), err => reject(err))
    })
}

export const createRepoAPI = (data) => {
    return new Promise((resolve, reject) => {
        http.post(
            '/repo/manage/',
            data
        ).then(res => resolve(res), err => reject(err))
    })
}

export const applyForRepoAPI = (repoId) => {
    return new Promise((resolve, reject) => {
        http.post(
            '/repo/common/' + repoId + '/apply/'
        ).then(res => resolve(res), err => reject(err))
    })
}

export const applyByDocAPI = (doc_id) => {
    return new Promise((resolve, reject) => {
        http.post(
            '/repo/common/apply_by_doc/',
            { doc_id }
        ).then(res => resolve(res), err => reject(err))
    })
}

export const exitRepoAPI = (repoId) => {
    return new Promise((resolve, reject) => {
        http.post(
            '/repo/common/' + repoId + '/exit/'
        ).then(res => resolve(res), err => reject(err))
    })
}

export const loadRepoUserAdminAPI = (repoId, page, size, keyword) => {
    return new Promise((resolve, reject) => {
        http.get(
            '/repo/manage/' + repoId + '/load_user/?page=' + page + '&size=' + size + '&searchKey=' + keyword
        ).then(res => resolve(res), err => reject(err))
    })
}

export const removeRepoUserAdminAPI = (repoId, uid) => {
    return new Promise((resolve, reject) => {
        http.post(
            '/repo/manage/' + repoId + '/remove_user/',
            { uid }
        ).then(res => resolve(res), err => reject(err))
    })
}

export const dealRepoUserApplyAdminAPI = (repoId, status, uid) => {
    return new Promise((resolve, reject) => {
        http.post(
            '/repo/manage/' + repoId + '/deal_apply/',
            { status, uid }
        ).then(res => resolve(res), err => reject(err))
    })
}

export const changeRepoUserTypeAdminAPI = (repoId, uid, uType) => {
    return new Promise((resolve, reject) => {
        http.post(
            '/repo/manage/' + repoId + '/change_u_type/',
            { uid, uType }
        ).then(res => resolve(res), err => reject(err))
    })
}
