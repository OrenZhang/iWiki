<template>
    <div class="h-100 home-container">
        <el-scrollbar always>
            <div class="main-container">
                <div class="search-box">
                    <div>
                        <div style="display: flex;">
                            <div style="width: 100%; margin-right: 10px; height: 36px;">
                                <el-select
                                    :no-data-text="$t('homeSearchNotice')"
                                    popper-class="home-select-popper"
                                    v-model="searchKey"
                                    :options="options"
                                    :placeholder="$t('homeSearchKey')"
                                    style="width: 100%; height: 36px;"
                                    allow-create
                                    filterable
                                    multiple
                                    clearable
                                    default-first-option
                                />
                            </div>
                            <el-button type="primary" size="medium" @click="docs.paginator.page = 1; searchDocs()">
                                {{ $t('search') }}
                            </el-button>
                            <el-button type="primary" size="medium" @click="resetSearch">
                                {{ $t('reset') }}
                            </el-button>
                        </div>
                    </div>
                </div>
                <el-container class="next-container">
                    <el-main>
                        <div class="home-notice-box" v-if="homeNotice.showNotice">
                            <el-alert :title="homeNotice.title" :description="homeNotice.desc" :type="homeNotice.type" :show-icon="homeNotice.showIcon" />
                        </div>
                        <DocPublishChart />
                        <el-skeleton :rows="6" animated v-show="loading" />
                        <DocList :data="docs" @pageChange="handlePageChange" v-show="!loading" />
                    </el-main>
                    <el-aside>
                        <DocSidebar />
                    </el-aside>
                </el-container>
            </div>
        </el-scrollbar>
    </div>
</template>

<script setup>
    import { onMounted, ref } from 'vue'
    import DocSidebar from '../components/DocSidebar.vue'
    import DocList from '../components/DocList.vue'
    import message from '../utils/message'
    import DocPublishChart from '../components/DocPublishChart.vue'
    import { loadDocPublicAPI, searchDocAPI } from '../api/modules/doc'
    import { getConfAPI } from '../api/modules/common'
    import { setTitle } from '../utils/controller'

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

    // 文章列表
    const docs = ref({
        usePaginator: true,
        paginator: {
            page: 1,
            count: 0,
            size: 10
        },
        data: []
    })
    const loadDocs = () => {
        setLoading(true)
        loadDocPublicAPI(docs.value.paginator.size, docs.value.paginator.page).then(res => {
            docs.value.data = res.data.results
            docs.value.paginator.count = res.data.count
            docs.value.paginator.page = res.data.page
        }, err => {
            message(err.data.msg, 'error')
            if (err.data.code === 404) {
                docs.value.paginator.page = 1
                loadDocs()
            }
        }).finally(() => {
            setLoading(false)
        })
    }
    onMounted(loadDocs)

    // 搜索
    const searchKey = ref([])
    const options = ref([])
    const searchDocs = () => {
        setLoading(true)
        searchDocAPI(searchKey.value, docs.value.paginator.page, docs.value.paginator.size).then(res => {
            docs.value.data = res.data.results
            docs.value.paginator.count = res.data.count
            docs.value.paginator.page = res.data.page
        }, err => {
            message(err.data.msg, 'warning')
        }).finally(() => {
            setLoading(false)
        })
    }
    const resetSearch = () => {
        searchKey.value = []
        docs.value.paginator.page = 1
        loadDocs()
    }

    const handlePageChange = (page) => {
        docs.value.paginator.page = page
        if (searchKey.value.length > 0) {
            searchDocs()
        } else {
            loadDocs()
        }
    }

    // 提示信息
    const homeNotice = ref({
        title: '',
        desc: '',
        showIcon: true,
        type: 'info',
        showNotice: false
    })
    const getHomeNotice = () => {
        getConfAPI('home_notice').then(res => {
            if (res.result) {
                homeNotice.value = res.data
            }
        })
    }
    onMounted(getHomeNotice)

    onMounted(() => {
        setTitle()
    })
</script>

<style scoped>
    @import '../assets/Home.css';
</style>
