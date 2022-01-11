<template>
    <div class="mobile-doc-container">
        <el-skeleton :rows="6" animated v-if="loading" />
        <ErrorPage :error="errorCode" v-if="!loading && errorCode !== 0" />
        <DocInfoBox v-else :doc-data="docData" :loading="loading" />
        <DocComment :doc-id="docID" />
    </div>
</template>

<script setup>
    import DocInfoBox from '../components/DocInfoBox.vue'
    import DocComment from '../components/DocComment.vue'
    import ErrorPage from '../components/ErrorPage.vue'
    import { computed, onMounted, ref } from 'vue'
    import { useRoute } from 'vue-router'
    import message from '../utils/message'
    import globalContext from '../context'
    import { getDocCommonAPI } from '../api/modules/doc'

    onMounted(() => {
        if (window.innerWidth >= 1000 && window.innerHeight >= 600) {
            window.location.replace(globalContext.siteUrl + 'doc/' + docID.value)
        }
    })
    
    const loading = ref(true)
    const setLoading = (status) => {
        if (status) {
            loading.value = true
        } else {
            setTimeout(() => {
                loading.value = false
            }, 600)
        }
    }

    const permissionDenied = ref(false)
    const error404 = ref(false)
    const errorCode = computed(() => {
        if (error404.value) {
            return 404
        } else if (permissionDenied.value) {
            return 403
        }
        return 0
    })

    const docData = ref({
        id: '',
        title: '',
        creator_name: '',
        update_at: '',
        content: '',
        creator: '',
        repo_name: '',
        attachments: {}
    })
    const loadDoc = () => {
        setLoading(true)
        getDocCommonAPI(docID.value).then(res => {
            if (res.result) {
                docData.value = res.data
            }
        }, err => {
            message(err.data.msg, 'error')
            if (err.status === 403) {
                permissionDenied.value = true
            } else if (err.status === 404) {
                error404.value = true
            }
        }).finally(() => {
            setLoading(false)
        })
    }
    onMounted(loadDoc)

    const route = useRoute()
    const docID = ref(route.params.id)
</script>

<style scoped>
    .mobile-doc-container {
        padding: 20px;
        box-sizing: border-box;
    }
</style>
