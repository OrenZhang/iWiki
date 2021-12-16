<template>
    <div class="h-100">
        <ErrorPage :error="errorCode" :apply-info="appleInfo" v-if="!loading && errorCode !== 0" />
        <el-scrollbar always ref="scroll" v-if="errorCode === 0">
            <el-container id="doc-container" class="doc-container h-100">
                <el-main style="overflow: unset;">
                    <el-skeleton :rows="6" animated v-if="loading" />
                    <DocInfoBox @loadTitle="loadTitle" :doc-data="docData" :loading="loading" />
                    <el-divider />
                    <DocComment :doc-id="docID" />
                </el-main>
                <el-aside style="overflow: unset;">
                    <DocSidebar />
                    <DocCatalogue @doScroll="doScroll" :titles="titles" />
                </el-aside>
            </el-container>
        </el-scrollbar>
    </div>
</template>

<script setup>
    import ErrorPage from '../components/ErrorPage.vue'
    import DocInfoBox from '../components/DocInfoBox.vue' 
    import DocComment from '../components/DocComment.vue'
    import DocSidebar from '../components/DocSidebar.vue'
    import { useRoute } from 'vue-router'
    import { useStore } from 'vuex'
    import { computed, onMounted, ref, watch } from 'vue'
    import http from '../api'
    import message from '../utils/message'
    import DocCatalogue from '../components/DocCatalogue.vue'

    const appleInfo = ref({
        visible: true,
        doc_id: computed(() => docID.value)
    })

    const titles = ref([])
    const loadTitle = (value) => {
        titles.value = value
    }

    // 加载状态
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

    // vuex
    const store = useStore()
    
    // 文章
    const docID = ref('')
    const docData = ref({
        id: '',
        title: '',
        creator_name: '',
        update_at: '',
        content: '',
        creator: '',
        repo_name: '',
        attachments: {},
        repo_id: ''
    })
    const loadDoc = () => {
        setLoading(true)
        http.get(
            '/doc/common/' + docID.value + '/'
        ).then(res => {
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

    // 异常
    const error404 = ref(false)
    const permissionDenied = ref(false)
    const errorCode = computed(() => {
        if (error404.value) {
            return 404
        } else if (permissionDenied.value) {
            return 403
        }
        return 0
    })

    // router
    const route = useRoute()
    docID.value = route.params.id
    watch(() => route.params.id, id => {
        docID.value = id
        if (docID.value !== undefined) {
            loadDoc()
        }
    })

    const scroll = ref(null)
    const doScroll = (top) => {
        scroll.value.setScrollTop(top)
    }
</script>

<style scoped>
    @import "../assets/Doc.css";
</style>