<template>
    <div class="h-100">
        <el-scrollbar always>
            <div class="head-box" />
            <HUserInfoBox :user-info="userInfo" />
            <div class="content-box">
                <div>
                    <el-aside width="120px">
                        <el-menu :default-active="activeMenu">
                            <el-menu-item
                                v-for="item in menu" :key="item.index"
                                :index="item.index"
                                @click="activeMenu = item.index">
                                <i :class="item.icon" />
                                <span>{{ item.name }}</span>
                            </el-menu-item>
                        </el-menu>
                    </el-aside>
                    <el-main>
                        <keep-alive>
                            <component :is="curComponent" />
                        </keep-alive>
                    </el-main>
                </div>
            </div>
        </el-scrollbar>
    </div>
</template>

<script setup>
    import { computed, onMounted, ref } from 'vue'
    import http from '../api'
    import { useStore } from 'vuex'
    import HUserInfoBox from '../components/HUserInfoBox.vue'
    import DocManage from '../components/DocManage.vue'
    import RepoManage from '../components/RepoManage.vue'
    import { useI18n } from 'vue-i18n'

    const { t } = useI18n()
    
    const store = useStore()
    const userInfo = computed(() => store.state.user)

    const checkLogin = () => {
        http.get(
            '/account/login_check/'
        ).then(() => {}, () => {
            store.commit('setLogin', true)
        })
    }
    onMounted(checkLogin)

    const curComponent = computed(() => {
        switch (activeMenu.value) {
            case 'doc':
                return DocManage
            case 'repo':
                return RepoManage
            default:
                return DocManage
        }
    })
    const activeMenu = ref('doc')
    const menu = ref([
        {
            index: 'doc',
            name: t('docManage'),
            icon: 'fa-solid fa-copy',
        },
        {
            index: 'repo',
            name: t('repoManage'),
            icon: 'fa-solid fa-cube'
        }
    ])
</script>

<style scoped>
    @import "../assets/UserSelf.css";
</style>