<template>
    <div class="h-center v-center h-100">
        <el-empty :description="description">
            <el-button type="text" @click="router.push({ name: 'Home' })">
                {{ $t('backIndex') }}
            </el-button>
            <el-button v-show="applyInfo.visible && user.auth" type="text" @click="doApply">
                {{ $t('applyForRepo') }}
            </el-button>
            <el-button v-show="!user.auth" type="text" @click="showLogin">
                {{ $t('login') }}
            </el-button>
        </el-empty>
    </div>
</template>


<script setup>
    import { computed } from 'vue'
    import { useRouter } from 'vue-router'
    import { useStore } from 'vuex'
    import message from '../utils/message'
    import { useI18n } from 'vue-i18n'
    import { applyByDocAPI } from '../api/modules/repo'
    
    const { t } = useI18n()
    
    const store = useStore()
    const user = computed(() => store.state.user)

    const router = useRouter()

    const props = defineProps({
        error: {
            type: Number,
            default: 404
        },
        errorMessages: {
            type: Object,
            default: {
                403: 'permissionDenied',
                404: 'Error404',
                400001: 'docEditing'
            }
        },
        applyInfo: {
            type: Object,
            default: {
                visible: false,
                doc_id: null
            }
        }
    })

    const doApply = () => {
        applyByDocAPI(props.applyInfo.doc_id).then(() => {
            message(t('applyForGroupSuccessMsg'))
        }, err => {
            message(err.data.msg, 'error')
        })
    }

    const description = computed(() => {
        if (props.error === 0) {
            return ''
        } else {
            return t(props.errorMessages[props.error])
        }
    })

    const showLogin = (() => {
        store.commit('setLogin', true)
    })
</script>

<style scoped>

</style>