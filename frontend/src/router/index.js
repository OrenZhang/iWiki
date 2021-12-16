import * as vueRouter from 'vue-router'
import store from '../store'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: () => import('../views/Home.vue')
    },
    {
        path: '/publish',
        name: 'Publish',
        component: () => import('../views/Publish.vue'),
    },
    {
        path: '/publish/:id',
        name: 'Edit',
        component: () => import('../views/Publish.vue')
    },
    {
        path: '/user',
        name: 'Self',
        component: () => import('../views/UserSelf.vue')
    },
    {
        path: '/user/:username',
        name: 'User',
        component: () => import('../views/User.vue')
    },
    {
        path: '/doc/:id',
        name: 'Doc',
        component: () => import('../views/Doc.vue')
    },
    {
        path: '/repo',
        name: 'Repo',
        component: () => import('../views/Repo.vue'),
    },
    {
        path: '/repo/:id',
        name: 'RepoDetail',
        component: () => import('../views/RepoDetail.vue')
    },
    {
        path: '/:pathMatch(.*)*',
        name: '404',
        component: () => import('../components/ErrorPage.vue')
    }
]

const router = vueRouter.createRouter({
    history: vueRouter.createWebHistory(),
    routes
})

router.beforeEach(() => {
    store.dispatch('setMainLoading', true)
})

router.afterEach(() => {
    store.dispatch('setMainLoading', false)
})

export default router
