<template>
    <el-card class="repo-doc-box">
        <el-tabs v-model="activeTab">
            <el-tab-pane :label="$t('hotRepo')" name="repo">
                <el-table :show-header="false" :data="hotRepos" size="small">
                    <el-table-column type="index" width="24" />
                    <el-table-column>
                        <template #default="scope">
                            <el-link target="_blank" :underline="false" :href="globalContext.siteUrl + 'repo/' + scope.row.id">
                                {{ scope.row.name }}
                            </el-link>
                        </template>
                    </el-table-column>
                </el-table>
            </el-tab-pane>
            <el-tab-pane :label="$t('newDoc')" name="doc">
                <el-table :show-header="false" :data="recentDocs" size="small">
                    <el-table-column type="index" width="24" />
                    <el-table-column>
                        <template #default="scope">
                            <el-link target="_blank" :underline="false" :href="globalContext.siteUrl + 'doc/' + scope.row.id">
                                {{ scope.row.title }}
                            </el-link>
                        </template>
                    </el-table-column>
                </el-table>
            </el-tab-pane>
        </el-tabs>
    </el-card>
</template>

<script setup>
    import globalContext from '../context'
    import { useRouter } from 'vue-router'
    import { onMounted, ref } from 'vue'
    import http from '../api'

    const router = useRouter()

    const activeTab = ref('repo')
    
    const hotRepos = ref([])
    const loadHotRepo = () => {
        http.get(
            '/doc/public/hot_repo/'
        ).then(res => {
            hotRepos.value = res.data
        })
    }
    onMounted(loadHotRepo)

    const recentDocs = ref([])
    const loadRecentDoc = () => {
        http.get(
            '/doc/public/recent/'
        ).then(res => {
            recentDocs.value = res.data
        })
    }
    onMounted(loadRecentDoc)
</script>

<style scoped>
    .repo-doc-box {
        margin-top: 20px;
        border-radius: 5px;

    }

    .repo-doc-box :deep(.cell),
    .el-link {
        font-size: 14px;
    }

    .repo-doc-box :deep(.el-tabs__nav) {
        justify-content: center;
        display: flex;
        width: 100%;
    }
</style>