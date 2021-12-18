<template>
    <div class="login-container">
        <div class="login-box">
            <el-aside width="400px">
                <div style="width: 100%; height: 100%; overflow: hidden;">
                    <img alt="side-pic.jpg" class="side-pic" src="https://wiki.incv.net/static/img/bg-3.jpg">
                </div>
            </el-aside>
            <el-main style="width:100%">
                <el-header>
                    <el-link :class="{ 'el-link--primary': curTab === 'sign-in' }" @click="changeCurTab('sign-in')">
                        {{ $t('login') }}
                    </el-link>
                    <span class="mg-20-left-right">/</span>
                    <el-link :class="{ 'el-link--primary': curTab === 'sign-up' }" @click="changeCurTab('sign-up')">
                        {{ $t('signup') }}
                    </el-link>
                </el-header>
                <el-main>
                    <component :is="curComponent" />
                </el-main>
                <el-divider style="margin: 0 0 10px 0" />
                <el-footer>
                    <el-link @click="store.commit('setLogin', false)">
                        {{ $t('exitLogin') }}
                    </el-link>
                    <el-link class="edit-user" v-show="curTab === 'sign-in'" @click="showEdit">
                        {{ $t('updatePassword') }}
                    </el-link>
                </el-footer>
            </el-main>
        </div>
    </div>
</template>

<script setup>
    import LoginForm from '../components/LoginForm.vue'
    import RegisterForm from '../components/RegisterForm.vue'
    import { computed, ref } from 'vue'
    import { useStore } from 'vuex'

    const store = useStore()
    
    // 标签
    const curTab = ref('sign-in')
    const changeCurTab = (tab) => {
        curTab.value = tab
    }
    
    // 组件
    const curComponent = computed(() => {
        switch (curTab.value) {
            case 'sign-in':
                return LoginForm
            case 'sign-up':
                return RegisterForm
            default:
                return LoginForm
        }
    })

    const showEdit = () => {
        store.commit('setLogin', false)
        store.commit('setEditUser', true)
    }
</script>

<style scoped>
    @import "../assets/Login.css";
</style>