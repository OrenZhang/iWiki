<template>
    <div class="h-100 repo-container">
        <el-scrollbar always>
            <div class="main-container">
                <div class="head-box" />
                <div class="box-container">
                    <RepoDetailInfo
                        :is-admin="isAdmin" :repo="repo" @reloadRepoInfo="loadRepoInfo"
                    />
                </div>
                <div class="content-box">
                    <el-main>
                        <el-skeleton :rows="6" animated v-show="loading" />
                        <PinDocList :repo-id="repo_id" v-show="!loading" />
                        <DocList :data="docs" @pageChange="handlePageChange" v-show="!loading" />
                    </el-main>
                    <el-aside>
                        <div class="search-bar">
                            <el-input v-model="searchKey" :placeholder="$t('title')" />
                            <el-button @click="doSearch">
                                <i class="fa-solid fa-search" />
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
    import { computed, onMounted, ref } from 'vue'
    import RepoDetailInfo from '../components/RepoDetailInfo.vue'
    import DocSidebar from '../components/DocSidebar.vue'
    import DocList from '../components/DocList.vue'
    import { useStore } from 'vuex'
    import PinDocList from '../components/PinDocList.vue'
    import { loadRepoDetailAPI } from '../api/modules/repo'
    import { loadRepoDocAPI } from '../api/modules/doc'

    const store = useStore()
    const user = computed(() => store.state.user)
    
    const route = useRoute()
    const repo_id = route.params.id
    
    const repo = ref({})
    const loadRepoInfo = () => {
        loadRepoDetailAPI(repo_id).then(res => {
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
        loadRepoDocAPI(repo_id, searchKey.value, docs.value.paginator.page).then(res => {
            docs.value.data = res.data.results
            docs.value.paginator.count = res.data.count
        }).finally(() => {
            setLoading(false)
        })
    }
    onMounted(loadDocs)

    const isAdmin = computed(() => {
        for (const i in repo.value.admins) {
            if (repo.value.admins[i].uid === user.value.uid) {
                return true
            }
        }
        return false
    })
</script>

<style scoped>
    @import "../assets/RepoDetail.css";
</style>