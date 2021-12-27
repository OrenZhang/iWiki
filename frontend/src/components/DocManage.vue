<template>
    <div class="doc-manage">
        <div class="tool-bar">
            <div style="display: flex">
                <el-input size="medium" class="search-input" clearable :placeholder="$t('docTitle')" v-model="searchKey" />
                <el-button size="medium" type="primary" @click="doSearch">
                    {{ $t('search') }}
                </el-button>
                <el-button size="medium" type="primary" @click="resetSearch">
                    {{ $t('reset') }}
                </el-button>
            </div>
            <el-pagination
                background layout="prev, pager, next"
                :total="paginator.count" :pager-count="5"
                :current-page="paginator.page" @current-change="handlePageChange"
            />
        </div>
        <el-skeleton :rows="6" v-show="loading" animated style="margin-top: 20px" />
        <el-table size="medium" :data="docs" v-show="!loading">
            <el-table-column :label="$t('title')">
                <template #default="scope">
                    <el-tooltip :content="scope.row.repo_name" placement="top" effect="light">
                        <span>{{ scope.row.title }}</span>
                    </el-tooltip>
                </template>
            </el-table-column>
            <el-table-column :label="$t('docType')" width="80px">
                <template #default="scope">
                    <el-tag v-if="scope.row.available === 'public'" size="small">
                        {{ $t('public') }}
                    </el-tag>
                    <el-tag v-else size="small" type="warning">
                        {{ $t('private') }}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column :label="$t('docStatus')" width="80px">
                <template #default="scope">
                    <el-tag v-if="scope.row.is_publish" size="small">
                        {{ $t('published') }}
                    </el-tag>
                    <el-tag v-else size="small" type="info">
                        {{ $t('draft') }}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column :label="$t('updateAt')" prop="update_at" width="200px" />
            <el-table-column :label="$t('operation')" width="160px">
                <template #default="scope">
                    <el-button type="text" :disabled="!scope.row.is_publish" @click="goTo('doc/' + scope.row.id)">
                        {{ $t('open') }}
                    </el-button>
                    <el-button type="text" @click="goTo('publish/' + scope.row.id)">
                        {{ $t('edit') }}
                    </el-button>
                    <el-button type="text" class="el-button--danger" @click="showDeleteConfirm(scope.row)">
                        {{ $t('delete') }}
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script setup>
    import { onMounted, ref } from 'vue'
    import http from '../api'
    import message from '../utils/message'
    import { ElMessageBox } from 'element-plus'
    import { useI18n } from 'vue-i18n'
    import globalContext from '../context'
    
    const { t } = useI18n()
    
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

    const goTo = (url) => {
        window.open(globalContext.siteUrl + url)
    }

    const docs = ref([])
    const searchKey = ref('')
    const paginator = ref({
        page: 1,
        count: 0
    })
    const handlePageChange = (page) => {
        paginator.value.page = page
        loadDocs()
    }
    const loadDocs = () => {
        setLoading(true)
        http.get(
            '/doc/manage/?page=' + paginator.value.page + '&searchKey=' + searchKey.value
        ).then(res => {
            docs.value = res.data.results
            paginator.value.count = res.data.count
        }, err => {
            message(err.data.msg, 'error')
        }).finally(() => {
            setLoading(false)
        })
    }
    onMounted(loadDocs)

    const doSearch = () => {
        paginator.value.page = 1
        loadDocs()
    }
    const resetSearch = () => {
        searchKey.value = ''
        paginator.value.page = 1
        loadDocs()
    }

    const showDeleteConfirm = (row) => {
        const content = t('deleteDocConfirmContent', { title: row.title })
        ElMessageBox.alert(content, t('deleteConfirm'), {
            confirmButtonText: t('deleteConfirmed'),
            confirmButtonClass: 'el-button--danger',
            callback: (action) => {
                if (action === 'confirm') {
                    http.delete(
                        '/doc/manage/' + row.id + '/'
                    ).then(() => {
                        loadDocs()
                    }, err => {
                        message(err.data.msg, 'error')
                    })
                }
            },
        })
    }
</script>

<style scoped>
    .tool-bar {
        width: 100%;
        display: flex;
        justify-content: space-between;
    }

    .tool-bar .el-pagination {
        display: flex;
        align-items: center;
    }

    .tool-bar .el-button {
        margin-left: 10px;
    }

    .el-table {
        margin-top: 20px;
    }

    .el-button--danger :deep(span) {
        color: #f56c6c;
    }

    .tool-bar .el-input {
        max-width: 240px;
    }

    .tool-bar .el-select {
        margin-left: 10px;
    }

    .tool-bar .el-select,
    .tool-bar .el-select .el-input {
        width: 120px;
    }

    .search-input {
        height: 100%;
    }

    .search-input :deep(.el-input__inner) {
        height: 100%;
    }
</style>