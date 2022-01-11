import http from '../index'

export const getUserInfoAPI = () => {
    return new Promise((resolve, reject) => {
        http.get(
            '/account/user_info/'
        ).then(res => resolve(res), err => reject(err))
    })
}

export const getExactUserInfoAPI = (searchUser) => {
    return new Promise((resolve, reject) => {
        http.get(
            '/account/user_info/' + searchUser + '/'
        ).then(res => resolve(res), err => reject(err))
    })
}

export const isManagerAPI = () => {
    return new Promise((resolve, reject) => {
        http.get(
            '/account/user_info/is_manager/'
        ).then(res => resolve(res), err => reject(err))
    })
}

export const signOutAPI = () => {
    return new Promise((resolve, reject) => {
        http.get(
            '/account/sign_out/'
        ).then(res => resolve(res), err => reject(err))
    })
}

export const checkSuperAdminAPI = () => {
    return new Promise((resolve, reject) => {
        http.get(
            '/account/user_info/is_superuser/'
        ).then(res => resolve(res), err => reject(err))
    })
}

export const searchUserAPI = (keyword) => {
    return new Promise((resolve, reject) => {
        http.post(
            '/account/search/search_user/',
            {
                searchKey: keyword
            }
        ).then(res => resolve(res), err => reject(err))
    })
}

export const loginCheckAPI = () => {
    return new Promise((resolve, reject) => {
        http.get(
            '/account/login_check/'
        ).then(res => resolve(res), err => reject(err))
    })
}

export const loadActiveUserAPI = () => {
    return new Promise((resolve, reject) => {
        http.get(
            '/account/user_info/active_user/'
        ).then(res => resolve(res), err => reject(err))
    })
}

export const repassAPI = (username, password, code, phone) => {
    return new Promise((resolve, reject) => {
        http.post(
            '/account/user_info/re_pass/',
            { username, password, code, phone }
        ).then(res => resolve(res), err => reject(err))
    })
}

export const signInAPI = (data) => {
    return new Promise((resolve, reject) => {
        http.post(
            '/account/sign_in/',
            data
        ).then(res => resolve(res), err => reject(err))
    })
}

export const checkUserNameAPI = (username) => {
    return new Promise((resolve, reject) => {
        http.post(
            '/account/search/check_username/',
            {
                username: username
            }
        ).then(res => resolve(res), err => reject(err))
    })
}

export const signUpAPI = (data) => {
    return new Promise((resolve, reject) => {
        http.post(
            '/account/sign_up/',
            data
        ).then(res => resolve(res), err => reject(err))
    })
}
