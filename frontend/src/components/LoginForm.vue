<template>
    <el-form label-position="left" label-width="80px">
        <el-form-item :label="$t('uLogin')">
            <el-input :placeholder="$t('usernameOrPhone')" v-model="loginData.username" :minlength="4" :maxlength="24" type="text" clearable :disabled="loading">
                <template #prefix>
                    <i class="fa-solid fa-user h-center" style="margin-left: 6px;" />
                </template>
            </el-input>
        </el-form-item>
        <el-form-item :label="$t('Password')">
            <el-input type="password" v-model="loginData.password" :maxlength="24" clearable show-password :disabled="loading">
                <template #prefix>
                    <i class="fa-solid fa-lock h-center" style="margin-left: 6px;" />
                </template>
            </el-input>
        </el-form-item>
        <div style="display: flex">
            <el-button style="width: 100%" type="primary" :disabled="!checkForm" :loading="loading" @click="doLogin(true)">
                {{ $t('login2refresh') }}
            </el-button>
        </div>
    </el-form>
</template>

<script setup>
    import { computed, ref } from 'vue'
    import { useStore } from 'vuex'
    import http from '../api'
    import message from '../utils/message'
    import { useI18n } from 'vue-i18n'
    
    const { t } = useI18n()
    
    // 全局
    const store = useStore()

    // 状态
    const loading = ref(false)
    const setLoading = (status) => {
        if (status) {
            loading.value = true
        } else {
            setTimeout(() => {
                loading.value = false
            }, 600)
        }
    }

    // 数据
    const loginData = ref({
        username: '',
        password: ''
    })
    
    // 校验
    const checkForm = computed(() => {
        return loginData.value.username !== '' && loginData.value.password !== '' && loginData.value.username.length >=4
    })
    
    // 登录
    const doLogin = (refresh = false) => {
        setLoading(true)
        http.post(
            '/account/sign_in/',
            loginData.value
        ).then(res => {
            if (res.result) {
                message(t('loginSuccess'))
                store.commit('setLogin', false)
                store.dispatch('getUserInfo')
                if (refresh) {
                    window.location.reload()
                }
            }
        }, err => {
            message(err.data.msg, 'error')
        }).finally(() => {
            setLoading(false)
        })
    }
</script>

<style scoped>

</style>