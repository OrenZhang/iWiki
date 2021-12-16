import axios from 'axios'
import globalContext from '../context'
import store from '../store'

const http = axios

http.defaults.timeout = 10000
http.defaults.baseURL = globalContext.backEndUrl
http.defaults.withCredentials = true

http.interceptors.response.use(res => {
    res = res.data
    return res
}, err => {
    err = err.response
    if (err.status === 401) {
        store.commit('setLogin', true)
    }
    return Promise.reject(err)
})

export default http
