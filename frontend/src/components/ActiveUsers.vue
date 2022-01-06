<template>
    <el-card class="active-user">
        <div class="title">
            {{ $t('activeUser') }}
        </div>
        <el-table :data="activeUsers" :show-header="false">
            <el-table-column width="40px" class-name="avatar-column">
                <template #default="scope">
                    <el-avatar v-if="scope.row.avatar !== '' && scope.row.avatar !== null" :src="scope.row.avatar" />
                    <el-avatar v-else>
                        <i class="fa-solid fa-user" />
                    </el-avatar>
                </template>
            </el-table-column>
            <el-table-column prop="username">
                <template #default="scope">
                    <el-link target="_blank" :href="globalContext.siteUrl + 'user/' + scope.row.username" :underline="false">
                        {{ scope.row.username }}
                    </el-link>
                </template>
            </el-table-column>
            <el-table-column width="60px" align="right">
                <template #default="scope">
                    <el-tag size="mini" effect="plain">
                        {{ dealWithFloat(scope.row.active_index) }}
                    </el-tag>
                </template>
            </el-table-column>
        </el-table>
    </el-card>
</template>

<script setup>
    import globalContext from '../context'
    import { onMounted, ref } from 'vue'
    import http from '../api'
    import { useRouter } from 'vue-router'
    
    const router = useRouter()
    
    const activeUsers = ref([])
    const loadActiveUser = () => {
        http.get(
            '/account/user_info/active_user/'
        ).then(res => {
            activeUsers.value = res.data
        })
    }
    onMounted(loadActiveUser)

    const dealWithFloat = (num) => {
        const numArray = num.toString().split('.')
        if (numArray.length > 1)
            if (num < 10) {
                return num.toFixed(2)
            } else {
                return num.toFixed(1)
            }
        // 整数输出
        else {
            return num
        }
    }
</script>

<style scoped>
    .title {
        color: var(--el-color-primary);
        font-size: 14px;
        text-align: center;
        padding-bottom: 9px;
        border-bottom: 2px solid var(--el-border-color-light);
    }

    .active-user {
        margin-top: 20px;
    }

    .active-user .fa-user {
        font-size: 16px;
        margin-top: 0;
    }

    .active-user :deep(.cell) {
        line-height: unset;
        font-size: 14px;
    }

    .el-avatar {
        background: var(--el-color-primary-light-7);
        box-sizing: border-box;
    }

    .el-avatar .fa-user {
        color: var(--el-color-white);
    }

    :deep(.avatar-column) .cell {
        padding: 0 10px 0 0;
    }
</style>