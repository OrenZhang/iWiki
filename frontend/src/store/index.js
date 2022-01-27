import { createStore } from 'vuex'
import { getUserInfoAPI } from '../api/modules/user'
import { getConfAPI } from '../api/modules/common'

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
            },
            footerInfo: {
                'copyright': '',
                'showFooter': false,
                'siteStartup': ''
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
        },
        setFooterInfo (state, payload) {
            state.footerInfo = payload
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
            getUserInfoAPI().then(res => {
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
        },
        getFooterInfo ({ commit }) {
            getConfAPI('footer_info').then(res => {
                if (res.result) {
                    commit('setFooterInfo', res.data)
                }
            })
        }
    }
})

export default store
