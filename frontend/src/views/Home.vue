<template>
    <div class="h-100 home-container">
        <el-scrollbar always>
            <div class="main-container">
                <div class="search-box">
                    <div>
                        <div style="display: flex;">
                            <div style="width: 100%; margin-right: 10px; ">
                                <el-select
                                    :no-data-text="$t('homeSearchNotice')"
                                    popper-class="home-select-popper"
                                    v-model="searchKey"
                                    :options="options"
                                    :placeholder="$t('homeSearchKey')"
                                    style="width: 100%;"
                                    allow-create
                                    filterable
                                    multiple
                                    clearable
                                    default-first-option
                                />
                            </div>
                            <el-button type="primary" size="medium" @click="searchDocs">
                                {{ $t('search') }}
                            </el-button>
                            <el-button type="primary" size="medium" @click="resetSearch">
                                {{ $t('reset') }}
                            </el-button>
                        </div>
                    </div>
                </div>
                <div class="home-notice-box" v-if="showHomeNotice">
                    <el-alert :title="homeNotice.title" :description="homeNotice.desc" :type="homeNotice.type" :show-icon="homeNotice.showIcon" />
                </div>
                <el-container class="next-container">
                    <el-main>
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
    import http from '../api'
    import message from '../utils/message'
    import DocPublishChart from '../components/DocPublishChart.vue'

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
        http.get(
            '/doc/public/?size=' + docs.value.paginator.size + '&page=' + docs.value.paginator.page
        ).then(res => {
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
        http.post(
            '/doc/search/?page=' + docs.value.paginator.page + '&size=' + docs.value.paginator.size,
            {
                searchKey: searchKey.value
            }
        ).then(res => {
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
    const showHomeNotice = ref(false)
    const homeNotice = ref({
        title: '',
        desc: '',
        showIcon: true,
        type: 'info'
    })
    const getHomeNotice = () => {
        http.post(
            '/conf/common/',
            {
                cKey: 'home_notice'
            }
        ).then(res => {
            if (res.result) {
                homeNotice.value = res.data
                showHomeNotice.value = true
            }
        })
    }
    onMounted(getHomeNotice)
</script>

<style scoped>
    @import '../assets/Home.css';
</style>
