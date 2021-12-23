<template>
    <div class="h-center v-center h-100">
        <el-empty :description="description">
            <el-button type="text" @click="router.push({ name: 'Home' })">
                {{ $t('backIndex') }}
            </el-button>
            <el-button v-show="applyInfo.visible" type="text" @click="doApply">
                {{ $t('applyForRepo') }}
            </el-button>
        </el-empty>
    </div>
</template>


<script setup>
    import { computed } from 'vue'
    import { useRouter } from 'vue-router'
    import { useStore } from 'vuex'
    import http from '../api'
    import message from '../utils/message'
    import { useI18n } from 'vue-i18n'
    
    const { t } = useI18n()
    
    const store = useStore()

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
        http.post(
            '/repo/common/apply_by_doc/',
            {
                doc_id: props.applyInfo.doc_id
            }
        ).then(() => {
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
</script>

<style scoped>

</style>