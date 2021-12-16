<template>
    <div>
        <el-skeleton :rows="6" v-show="loading" animated style="margin-top: 20px" />
        <el-table size="medium" :data="repos" v-show="!loading">
            <el-table-column :label="$t('repoName')" prop="name" />
            <el-table-column :label="$t('repoType')" width="120px">
                <template #default="scope">
                    <el-tag size="small" v-if="scope.row.r_type === 'public'">
                        {{ $t('publicRepo') }}
                    </el-tag>
                    <el-tag size="small" v-else type="warning">
                        {{ $t('privateRepo') }}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column :label="$t('operation')" width="120px">
                <template #default="scope">
                    <el-button
                        type="text" @click="showExitConfirm(scope.row)"
                        :disabled="scope.row.id === 1 || scope.row.creator === user.uid">
                        {{ $t('exit') }}
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script setup>
    import { computed, onMounted, ref } from 'vue'
    import http from '../api'
    import message from '../utils/message'
    import { ElMessageBox } from 'element-plus'
    import { useStore } from 'vuex'
    import { useI18n } from 'vue-i18n'
    
    const { t } = useI18n()
    
    const store = useStore()
    const user = computed(() => store.state.user)
    
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
    
    const repos = ref([])
    const loadRepos = () => {
        setLoading(true)
        http.get(
            '/repo/common/'
        ).then(res => {
            repos.value = res.data
        }, err => {
            message(err.data.msg, 'error')
        }).finally(() => {
            setLoading(false)
        })
    }
    onMounted(loadRepos)

    const showExitConfirm = (row) => {
        const content = t('exitConfirmMsg', { name: row.name })
        ElMessageBox.alert(content, t('exitConfirm'), {
            confirmButtonText: t('exitConfirmed'),
            confirmButtonClass: 'el-button--danger',
            callback: (action) => {
                if (action === 'confirm') {
                    http.post(
                        '/repo/common/' + row.id + '/exit/'
                    ).then(() => {
                        loadRepos()
                    }, err => {
                        message(err.data.msg, 'error')
                    })
                }
            },
        })
    }
</script>

<style scoped>
    .el-button--danger :deep(span) {
        color: #f56c6c;
    }
</style>