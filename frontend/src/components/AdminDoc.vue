<template>
    <div>
        <div class="admin-doc-header">
            <div>
                <el-input size="medium" v-model="searchKey" :placeholder="$t('titleSearchKey')" />
                <el-button size="medium" type="primary" style="margin-left: 10px;" @click="paginator.page = 1; loadDoc()">
                    {{ $t('search') }}
                </el-button>
                <el-button size="medium" type="primary" style="margin-left: 10px;" @click="searchKey = '';paginator.page = 1; loadDoc()">
                    {{ $t('reset') }}
                </el-button>
            </div>
            <el-pagination
                background layout="total, prev, pager, next, sizes" :current-page="paginator.page" :total="paginator.count" :page-size="paginator.size"
                @current-change="handlePageChange" @size-change="handleSizeChange" />
        </div>
        <div class="admin-doc-main">
            <el-table :data="docs" stripe>
                <el-table-column prop="title" :label="$t('title')" />
                <el-table-column prop="creator_name" :label="$t('author')" />
                <el-table-column prop="update_at" :label="$t('updateAt')" />
                <el-table-column :label="$t('operation')">
                    <template #default="scope">
                        <el-link type="primary" :underline="false" @click="goTo(scope.row)">
                            {{ $t('open') }}
                        </el-link>
                        <el-link type="primary" :underline="false" @click="changeDoc(scope.row, 'available', 'private')" style="margin-left: 10px">
                            {{ $t('toPrivate') }}
                        </el-link>
                        <el-link type="primary" :underline="false" @click="changeDoc(scope.row, 'is_publish', false)" style="margin-left: 10px">
                            {{ $t('toDraft') }}
                        </el-link>
                        <el-link type="danger" :underline="false" @click="showDeleteConfirm(scope.row)" style="margin-left: 10px">
                            {{ $t('delete') }}
                        </el-link>
                    </template>
                </el-table-column>
            </el-table>
        </div>
    </div>
</template>

<script setup>
    import { onMounted, ref, watch } from 'vue'
    import http from '../api'
    import { ElMessageBox } from 'element-plus'
    import { useI18n } from 'vue-i18n'
    import globalContext from '../context'
    
    const { t } = useI18n()
    
    const props = defineProps({
        repoId: {
            type: String,
            default: ''
        }
    })
    
    const docs = ref([])
    const searchKey = ref('')
    const paginator = ref({
        page: 1,
        size: 10,
        count: 0
    })
    const handlePageChange = (page) => {
        paginator.value.page = page
        loadDoc()
    }
    const handleSizeChange = (size) => {
        paginator.value.page = 1
        paginator.value.size = size
        loadDoc()
    }
    const loadDoc = () => {
        if (!props.repoId) {
            return
        } 
        http.get(
            '/repo/manage/' + props.repoId + '/load_doc/?page=' + paginator.value.page + '&size=' + paginator.value.size + '&searchKey=' + searchKey.value
        ).then(res => {
            docs.value = res.data.results
            paginator.value.count = res.data.count
        })
    }
    onMounted(loadDoc)
    watch(() => props.repoId, () => {
        loadDoc()
    })

    const showDeleteConfirm = (row) => {
        const content = t('deleteDocConfirmContent', { title: row.title })
        ElMessageBox.alert(content, t('deleteConfirm'), {
            confirmButtonText: t('deleteConfirmed'),
            callback: (action) => {
                if (action === 'confirm') {
                    http({
                        url: '/repo/manage/' + props.repoId + '/delete_doc/',
                        method: 'DELETE',
                        data: {
                            docID: row.id
                        }
                    }).finally(() => {
                        loadDoc()
                    })
                }
            },
        })
    }

    const goTo = (row) => {
        window.open(globalContext.siteUrl + 'doc/' + row.id)
    }

    const changeDoc = (row, key, val) => {
        const data = {}
        data[key] = val
        console.log(data)
        http.patch(
            '/doc/manage/' + row.id + '/',
            data
        ).finally(() => {
            loadDoc()
        })
    }
</script>

<style scoped>
    .admin-doc-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .admin-doc-header > div {
        display: flex;
    }

    .admin-doc-header .el-pagination :deep(.el-pagination__sizes) {
        margin: 0;
    }
</style>