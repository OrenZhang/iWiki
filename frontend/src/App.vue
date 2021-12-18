<template>
    <el-config-provider :locale="locale">
        <div v-if="!screenCheck" class="small-screen">
            <span style="letter-spacing: 20px">iWik</span>i
        </div>
        <div v-loading="mainLoading" v-if="screenCheck" class="app-container">
            <Login v-show="showLogin" />
            <EditUserInfo v-show="showEditUser" />
            <el-header class="app-header" height="61px">
                <div class="el-menu-demo">
                    <div class="menu">
                        <router-link to="/" class="header-menu-home">
                            <img src="https://www.oren.ink/metapic/iwiki.png" alt="logo.jpg" style="width: 32px; height: 32px; margin: 0 10px 0 0;">
                            <h2 class="header-menu-home-title">
                                iWiki
                            </h2>
                        </router-link>
                        <el-menu :default-active="activeIndex" :router="true" mode="horizontal" :ellipsis="false">
                            <el-menu-item v-for="item in menu" v-show="!item.disabled" :key="item.index" :route="item.route" :index="item.index">
                                {{ item.name }}
                            </el-menu-item>
                        </el-menu>
                    </div>
                    <div class="right-bar">
                        <el-link :underline="false" type="warning" class="locale" @click="toggleLang">
                            <i class="fad fa-globe" />
                            <span>{{ curLocaleName }}</span>
                        </el-link>
                        <div class="user-login">
                            <el-link :underline="false" type="primary" v-show="!user.auth" @click="store.commit('setLogin', true)">
                                {{ $t('loginLogout') }}
                            </el-link>
                            <el-link :underline="false" type="danger" v-show="user.auth" @click="doLogout">
                                {{ $t('logout') }}
                            </el-link>
                        </div>
                    </div>
                </div>
            </el-header>
            <el-main style="height: calc(100% - 61px);padding: 0; z-index: -1;">
                <router-view />
            </el-main>
        </div>
    </el-config-provider>
</template>

<script setup>
    import Login from './views/Login.vue'
    import { computed, getCurrentInstance, onMounted, ref } from 'vue'
    import { useStore } from 'vuex'
    import { useRoute, useRouter } from 'vue-router'
    import { useI18n } from 'vue-i18n'
    import zhCn from 'element-plus/es/locale/lang/zh-cn'
    import en from 'element-plus/es/locale/lang/en'
    import http from './api'
    import EditUserInfo from './components/EditUserInfo.vue'

    // 国际化
    const { ctx } = getCurrentInstance()
    const { t } = useI18n()
    const userLocale = ref(localStorage.getItem('locale'))
    const curLocaleName = computed(() => userLocale.value === 'en' ? 'English' : '简体中文')
    const locale = computed(() => userLocale.value === 'en' ? en : zhCn)
    const toggleLang = () => {
        if (userLocale.value === 'en') {
            userLocale.value = 'zh'
            localStorage.setItem('locale', 'zh')
            changeBackendLang('zh-Hans')
        } else {
            userLocale.value = 'en'
            localStorage.setItem('locale', 'en')
            changeBackendLang('en')
        }
    }
    const changeBackendLang  = (langCode) => {
        store.commit('setMainLoading', true)
        http.post(
            '/i18n/',
            {
                language: langCode
            }
        ).finally(() => {
            setTimeout(() => {
                window.location.reload()
            }, 2000)
        })
    }

    // 宽度控制
    const width = ref(window.innerWidth)
    const height = ref(window.innerHeight)
    const screenCheck = computed(() => width.value >= 1000 && height.value >= 600 )
    onMounted(() => {
        window.addEventListener('resize', () => {
            width.value = window.innerWidth
            height.value = window.innerHeight
        })
    })

    // vuex
    const store = useStore()
    const user = computed(() => store.state.user)
    const mainLoading = computed(() => store.state.mainLoading)
    const showLogin = computed(() => store.state.showLogin)
    const showEditUser = computed(() => store.state.showEditUser)

    // 菜单
    const menu = ref([
        {
            name: t('Home'),
            route: {
                name: 'Home'
            },
            index: 'home',
            disabled: false
        },
        {
            name: t('Repo'),
            route: {
                name: 'Repo'
            },
            index: 'repo',
            disabled: false
        },
        {
            name: t('User'),
            route: {
                name: 'Self'
            },
            index: 'user',
            disabled: false
        },
        {
            name: t('New'),
            route: {
                name: 'Publish'
            },
            index: 'publish',
            disabled: false
        },
        {
            name: t('AdminTab'),
            route: {
                name: 'Admin'
            },
            index: 'admin',
            disabled: computed(() => !isManager.value)
        }
    ])

    // 管理员检测
    const isManager = ref(false)
    const checkManager = () => {
        http.get(
            '/account/user_info/is_manager/'
        ).then(res => {
            if (res.result && res.data) {
                isManager.value = true
            }
        })
    }
    checkManager()

    // 路由匹配
    const route = useRoute()
    const router = useRouter()
    const activeIndex = computed(() => {
        if (route.path === '/') {
            return 'home'
        }
        return route.path.split('/')[1]
    })

    // 用户信息
    onMounted(() => {
        store.dispatch('getUserInfo')
    })

    // 登录登出
    const doLogout = () => {
        store.commit('setMainLoading', true)
        http.get(
            '/account/sign_out/'
        ).then(() => {
            window.location.reload()
        }).finally(() => {
            store.dispatch('setMainLoading', false)
        })
    }
</script>

<style>
    @import "./assets/App.css";
</style>
