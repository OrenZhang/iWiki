<template>
    <div class="h-100 repo-container">
        <el-scrollbar always>
            <div class="main-container">
                <div class="head-box" />
                <div class="box-container">
                    <RepoDetailInfo
                        :is-admin="isAdmin" :apply="apply" :repo="repo"
                        @reloadApply="loadApply" @handleCurrentChange="handleCurrentChange" @reloadRepoInfo="loadRepoInfo"
                    />
                </div>
                <div class="content-box">
                    <el-main>
                        <el-skeleton :rows="6" animated v-show="loading" />
                        <DocList :data="docs" @pageChange="handlePageChange" v-show="!loading" />
                    </el-main>
                    <el-aside>
                        <div class="search-bar">
                            <el-input v-model="searchKey" :placeholder="$t('title')" />
                            <el-button @click="doSearch">
                                <i class="fa fa-search" />
                            </el-button>
                        </div>
                        <DocSidebar />
                    </el-aside>
                </div>
            </div>
        </el-scrollbar>
    </div>
</template>

<script setup>
    import { useRoute } from 'vue-router'
    import http from '../api'
    import { computed, onMounted, ref, watch } from 'vue'
    import RepoDetailInfo from '../components/RepoDetailInfo.vue'
    import DocSidebar from '../components/DocSidebar.vue'
    import DocList from '../components/DocList.vue'
    import { useStore } from 'vuex'

    const store = useStore()
    const user = computed(() => store.state.user)
    
    const route = useRoute()
    const repo_id = route.params.id
    
    const repo = ref({})
    const loadRepoInfo = () => {
        http.get(
            '/repo/common/' + repo_id + '/'
        ).then(res => {
            repo.value = res.data
        })
    }
    onMounted(loadRepoInfo)

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

    const docs = ref({
        usePaginator: true,
        paginator: {
            page: 1,
            count: 0,
            size: 10
        },
        data: []
    })
    const handlePageChange = (page) => {
        docs.value.paginator.page = page
        loadDocs()
    }
    const searchKey = ref('')
    const doSearch = () => {
        docs.value.paginator.page = 1
        loadDocs()
    }
    const loadDocs = () => {
        setLoading(true)
        http.get(
            '/doc/common/?repo_id=' + repo_id + '&searchKey=' + searchKey.value + '&page=' + docs.value.paginator.page
        ).then(res => {
            docs.value.data = res.data.results
            docs.value.paginator.count = res.data.count
        }).finally(() => {
            setLoading(false)
        })
    }
    onMounted(loadDocs)

    const apply = ref({
        data: [],
        paginator: {
            page: 1,
            count: 0
        }
    })
    const handleCurrentChange = () => {
        apply.value.paginator.page++
        loadApply()
    }
    const isAdmin = computed(() => {
        for (const i in repo.value.admins) {
            if (repo.value.admins[i].uid === user.value.uid) {
                return true
            }
        }
        return false
    })
    const loadApply = () => {
        http.get(
            '/repo/manage/' + repo_id + '/list_apply/?page=' + apply.value.paginator.page
        ).then(res => {
            apply.value.data = res.data.results
            apply.value.paginator.count = res.data.count
        })
    }
    watch(isAdmin, newVal => {
        if (newVal) {
            loadApply()
        }
    })
</script>

<style scoped>
    @import "../assets/RepoDetail.css";
</style>