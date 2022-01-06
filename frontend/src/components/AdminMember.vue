<template>
    <div class="admin-member">
        <div class="admin-member-header">
            <div>
                <el-input size="medium" v-model="searchKey" :placeholder="$t('username')" />
                <el-button size="medium" type="primary" style="margin-left: 10px;" @click="paginator.page = 1; loadMembers()">
                    {{ $t('search') }}
                </el-button>
                <el-button size="medium" type="primary" style="margin-left: 10px;" @click="searchKey = '';paginator.page = 1; loadMembers()">
                    {{ $t('reset') }}
                </el-button>
            </div>
            <el-pagination
                background layout="total, prev, pager, next, sizes" :current-page="paginator.page" :total="paginator.count" :page-size="paginator.size"
                @current-change="handlePageChange" @size-change="handleSizeChange" />
        </div>
        <el-table :data="members">
            <el-table-column prop="username" :label="$t('username')" />
            <el-table-column :label="$t('userType')">
                <template #default="scope">
                    <el-tag v-if="scope.row.u_type === 'admin'" size="mini">
                        {{ $t('admin') }}
                    </el-tag>
                    <el-tag v-else-if="scope.row.u_type === 'owner'" size="mini">
                        {{ $t('owner') }}
                    </el-tag>
                    <el-tag v-else-if="scope.row.u_type === 'member'" size="mini">
                        {{ $t('member') }}
                    </el-tag>
                    <el-tag v-else-if="scope.row.u_type === 'visitor'" type="info" size="mini">
                        {{ $t('visitor') }}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column :label="$t('operation')">
                <template #default="scope">
                    <el-link :underline="false" type="success" @click="dealApply(scope.row, true)" v-if="scope.row.u_type === 'visitor'" style="margin-right: 10px">
                        {{ $t('passApply') }}
                    </el-link>
                    <el-link :underline="false" type="danger" @click="dealApply(scope.row, false)" v-if="scope.row.u_type === 'visitor'" style="margin-right: 10px">
                        {{ $t('rejectApply') }}
                    </el-link>
                    <el-dropdown trigger="click" v-if="scope.row.u_type !== 'visitor'" style="margin-right: 10px" @command="showUType">
                        <el-link type="primary" :underline="false" class="el-dropdown-link" :disabled="checkEditAvailable(scope.row)">
                            {{ $t('changeUType') }}
                        </el-link>
                        <template #dropdown>
                            <el-dropdown-menu>
                                <el-dropdown-item :disabled="checkEditAvailable(scope.row)" :command="'a' + scope.row.uid">
                                    {{ $t('Admin') }}
                                </el-dropdown-item>
                                <el-dropdown-item :disabled="checkEditAvailable(scope.row)" :command="'m' + scope.row.uid">
                                    {{ $t('Member') }}
                                </el-dropdown-item>
                            </el-dropdown-menu>
                        </template>
                    </el-dropdown>
                    <el-link :underline="false" type="danger" @click="doRemoveMember(scope.row)" :disabled="checkEditAvailable(scope.row)" v-if="scope.row.u_type !== 'visitor'">
                        {{ $t('remove') }}
                    </el-link>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script setup>
    import { computed, onMounted, ref, watch } from 'vue'
    import http from '../api'
    import { useStore } from 'vuex'
    import message from '../utils/message'
    import { useI18n } from 'vue-i18n'
    import { ElMessageBox } from 'element-plus'
    
    const { t } = useI18n()
    
    const store = useStore()
    const user = computed(() => store.state.user)
    
    const props = defineProps({
        repoId: {
            type: String,
            default: null
        }
    })

    const searchKey = ref('')
    const members = ref([])
    const paginator = ref({
        page: 1,
        size: 10,
        count: 0
    })
    const handlePageChange = (page) => {
        paginator.value.page = page
        loadMembers()
    }
    const handleSizeChange = (size) => {
        paginator.value.page = 1
        paginator.value.size = size
        loadMembers()
    }
    const loadMembers = () => {
        if (!props.repoId) {
            return
        }
        http.get(
            '/repo/manage/' + props.repoId + '/load_user/?page=' + paginator.value.page + '&size=' + paginator.value.size + '&searchKey=' + searchKey.value
        ).then(res => {
            members.value = res.data.results
            paginator.value.count = res.data.count
        })
    }
    onMounted(loadMembers)

    watch(() => props.repoId, () => {
        loadMembers()
    })

    const checkEditAvailable = (row) => {
        return row.u_type === 'owner'
    }

    const doRemoveMember = (row) => {
        const content = t('removeMemberMsg', { name: row.username })
        ElMessageBox.alert(content, t('removeConfirm'), {
            confirmButtonText: t('removeConfirmed'),
            callback: (action) => {
                if (action === 'confirm') {
                    http.post(
                        '/repo/manage/' + props.repoId + '/remove_user/',
                        {
                            uid: row.uid
                        }
                    ).then(() => {
                        loadMembers()
                    })
                }
            },
        })
    }

    const dealApply = (row, status) => {
        http.post(
            '/repo/manage/' + props.repoId + '/deal_apply/',
            {
                status: status,
                uid: row.uid
            }
        ).then(() => {
            loadMembers()
        })
    }

    const showUType = (command) => {
        const u_type = command[0]
        let uType = null
        const uid = command.slice(1, command.length)
        switch (u_type) {
            case 'a':
                uType = 'admin'
                break
            case 'm':
                uType = 'member'
                break
            default:
                uType = 'member'
        }
        http.post(
            '/repo/manage/' + props.repoId + '/change_u_type/',
            {
                uid,
                uType
            }
        ).then(() => {
            loadMembers()
        })
    }
</script>

<style scoped>
    .admin-member-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .admin-member-header > div {
        display: flex;
    }

    .admin-member-header .el-pagination :deep(.el-pagination__sizes) {
        margin: 0;
    }
</style>