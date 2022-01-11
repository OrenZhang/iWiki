<template>
    <div class="login-container">
        <div class="login-box">
            <el-aside width="400px">
                <div style="width: 100%; height: 100%; overflow: hidden;">
                    <img alt="side-pic.jpg" class="side-pic" src="/extra-assests/imgs/bg-3.jpg">
                </div>
            </el-aside>
            <el-main style="width:100%">
                <el-header>
                    {{ $t('updatePassword') }}
                </el-header>
                <el-main>
                    <el-form label-position="left" label-width="80px">
                        <el-form-item :label="$t('username')">
                            <el-input :disabled="loading" v-model="username" :maxlength="24">
                                <template #prefix>
                                    <i class="fa-solid fa-user h-center" style="margin-left: 6px;" />
                                </template>
                            </el-input>
                        </el-form-item>
                        <el-form-item :label="$t('phone')">
                            <el-input :disabled="loading" v-model="phone" :maxlength="11" show-word-limit>
                                <template #prefix>
                                    <i class="fa-solid fa-phone-alt h-center" style="margin-left: 6px;" />
                                </template>
                            </el-input>
                        </el-form-item>
                        <el-form-item :label="$t('VerificationCode')" class="oneline-code-button-box">
                            <el-input v-model="code" :minlength="6" :maxlength="6" show-word-limit :disabled="loading">
                                <template #prefix>
                                    <i class="fa-solid fa-shield h-center" style="margin-left: 6px;" />
                                </template>
                            </el-input>
                            <el-button style="padding: 12px;" :disabled="phone.length !== 11 || codeSend || loading" @click="sendVerifyCode">
                                {{ $t('send') }}{{ showLastTime }}
                            </el-button>
                        </el-form-item>
                        <el-form-item :label="$t('password')">
                            <el-input :disabled="loading" type="password" show-password v-model="password">
                                <template #prefix>
                                    <i class="fa-solid fa-lock h-center" style="margin-left: 6px;" />
                                </template>
                            </el-input>
                        </el-form-item>
                    </el-form>
                    <el-button style="width: 100%" type="primary" :disabled="!checkForm" :loading="loading" @click="doEdit()">
                        {{ $t('submit') }}
                    </el-button>
                </el-main>
                <el-divider style="margin: 0 0 10px 0" />
                <el-footer>
                    <el-link @click="showLogin">
                        {{ $t('backToLogin') }}
                    </el-link>
                </el-footer>
            </el-main>
        </div>
    </div>
</template>

<script setup>
    import { useStore } from 'vuex'
    import { computed, ref } from 'vue'
    import { useI18n } from 'vue-i18n'
    import message from '../utils/message'
    import { sendRepassCodeAPI } from '../api/modules/common'
    import { repassAPI } from '../api/modules/user'
    
    const { t } = useI18n()
    const store = useStore()

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

    const showLogin = () => {
        store.commit('setEditUser', false)
        store.commit('setLogin', true)
    }

    const username = ref('')
    const password = ref('')
    const code = ref('')
    const phone = ref('')
    const checkForm = computed(() => {
        if (username.value.length < 4 || username.value.length > 24) {
            return false
        }
        if (password.value.length === 0 || password.value.length > 24) {
            return false
        }
        if (code.value.length !== 6) {
            return false
        }
        if (phone.value.length !== 11) {
            return false
        }
        return true
    })

    const codeSend = ref(false)
    const lastTime = ref(60)
    const showLastTime = computed(() => {
        if (codeSend.value) {
            return '(' + lastTime.value + ')'
        }
        return ''
    })
    const codeReSend = () => {
        setTimeout(() => {
            if (lastTime.value > 0) {
                lastTime.value--
                codeReSend()
            } else {
                codeSend.value = false
            }
        }, 1000)
    }
    const sendVerifyCode = () => {
        codeSend.value = true
        sendRepassCodeAPI(username.value, phone.value).then(res => {
            if (res.result) {
                message(t('sendCodeSuccess'))
            }
        }, err => {
            message(err.data.msg, 'error')
        }).finally(() => {
            lastTime.value = 60
            codeReSend()
        })
    }

    const clearData = () => {
        username.value = ''
        code.value = ''
        phone.value = ''
        password.value = ''
    }
    const doEdit = () => {
        setLoading(true)
        repassAPI(username.value, password.value, code.value, phone.value).then(() => {
            message(t('changeSuccess'))
            clearData()
            store.commit('setEditUser', false)
            store.commit('setLogin', true)
        }, err => {
            message(err.data.msg, 'error')
        }).finally(() => {
            setLoading(false)
        })
    }
</script>

<style scoped>
    @import "../assets/Login.css";
</style>
