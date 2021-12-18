import { createStore } from 'vuex'
import http from '../api'

const store = createStore({
    state () {
        return {
            mainLoading: true,
            showLogin: false,
            showEditUser: false,
            showVersion: false,
            user: {
                uid: '',
                username: '',
                avatar: '',
                date_joined: '',
                property: {},
                auth: false
            }
        }
    },
    mutations: {
        setMainLoading (state, payload) {
            state.mainLoading = payload
        },
        setUser (state, payload) {
            state.user = payload
        },
        setEditUser (state, payload) {
            state.showEditUser = payload
        },
        setLogin (state, payload) {
            state.showLogin = payload
        },
        setVersion (state, payload) {
            state.showVersion = payload
        }
    },
    actions: {
        setMainLoading ({ commit }, payload) {
            if (payload) {
                commit('setMainLoading', true)
            } else {
                setTimeout(() => {
                    commit('setMainLoading', status)
                }, 600)
            }
        },
        getUserInfo ({ commit, dispatch }) {
            dispatch('setMainLoading', true)
            http.get(
                '/account/user_info/'
            ).then(res => {
                if (res.result) {
                    commit('setUser', {
                        uid: res.data.uid,
                        username: res.data.username,
                        avatar: res.data.avatar,
                        property: res.data.property,
                        date_joined: res.data.date_joined,
                        auth: true
                    })
                } else {
                    commit('setUser', {
                        uid: res.data.uid,
                        username: res.data.username,
                        avatar: res.data.avatar,
                        property: res.data.property,
                        date_joined: res.data.date_joined,
                        auth: false
                    })
                }
            }).finally(() => {
                dispatch('setMainLoading', false)
            })
        }
    }
})

export default store
