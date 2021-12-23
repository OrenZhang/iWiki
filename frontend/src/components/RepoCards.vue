<template>
    <div>
        <el-row :gutter="20">
            <el-col :span="6" v-for="repo in repos" :key="repo.id">
                <el-card>
                    <div class="card-container">
                        <div class="text-info">
                            <div style="height: 100%; display: flex; align-items: center;">
                                <h4 style="margin-top: 0; color: #303133">
                                    {{ repo.name }}
                                </h4>
                            </div>
                            <div style="color: #606266">
                                <div style="display: flex; align-items: center; font-size: 14px; margin-bottom: 6px;">
                                    <el-tag size="mini" type="success" v-if="repo.r_type === 'public'" style="margin-right: 10px;">
                                        {{ $t('publicRepo') }}
                                    </el-tag>
                                    <el-tag size="mini" type="warning" v-else style="margin-right: 10px;">
                                        {{ $t('privateRepo') }}
                                    </el-tag>
                                    <i class="far fa-user-cog" />&nbsp;{{ repo.creator_name }}
                                </div>
                                <div style="font-size: 14px;">
                                    <el-tag size="mini" type="info" style="margin-right: 10px">
                                        {{ $t('createAt') }}
                                    </el-tag>
                                    <i class="far fa-calendar-alt" />&nbsp;{{ repo.create_at }}
                                </div>
                            </div>
                        </div>
                        <div class="check-info" :class="checkUserStatus(repo) ? 'public-repo' : 'private-repo'" @click="goRepo(repo)">
                            <i class="fad" :class="checkUserStatus(repo) ? 'fa-sign-in' : 'fa-lock'" />
                        </div>
                    </div>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script setup>
    import { useStore } from 'vuex'
    import { computed, ref } from 'vue'
    import { useRouter } from 'vue-router'
    import http from '../api'
    import message from '../utils/message'
    import { ElMessageBox } from 'element-plus'
    import { useI18n } from 'vue-i18n'
    import globalContext from '../context'
    
    const { t } = useI18n()
    
    const store = useStore
    const user = computed(() => store.state.user)

    defineProps({
        repos: {
            type: Object,
            default: []
        }
    })

    const checkUserStatus = (repo) => {
        return repo.r_type === 'public' || repo.member_type === 'owner' || repo.member_type === 'admin' || repo.member_type === 'member'
    }
    
    const router = useRouter()
    const goRepo = (repo) => {
        if (checkUserStatus(repo)) {
            window.open(globalContext.siteUrl + 'repo/' + repo.id)
        } else {
            showApplyConfirm(repo)
        }
    }

    const showApplyConfirm = (repo) => {
        const content = t('applyMsg', { name: repo.name })
        ElMessageBox.alert(content, t('applyConfirm'), {
            confirmButtonText: t('applyConfirmed'),
            callback: (action) => {
                if (action === 'confirm') {
                    http.post(
                        '/repo/common/' + repo.id + '/apply/'
                    ).then(() => {
                        message(t('applySuccess'))
                    }, err => {
                        message(err.data.msg, 'error')
                    })
                }
            },
        })
    }
</script>

<style scoped>
    .el-card {
        border: unset;
        height: 100%;
    }

    .el-card :deep(.el-card__body) {
        height: 100%;
        box-sizing: border-box;
        padding: 0;
    }

    .text-info {
        padding: 20px;
        display: flex;
        flex-direction: column;
        box-sizing: border-box;
        justify-content: space-between;
        height: 100%;
        width: 80%;
    }

    .el-col {
        margin-bottom: 20px;
    }

    .item {
        margin-top: 0;
        margin-right: 0;
        width: 100%;
    }

    .card-container {
        display: flex;
        height: 100%;
    }

    .check-info {
        width: 21%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
    }

    .public-repo {
        background: #C3E0C3;
        transition-duration: 0.4s;
    }

    .public-repo:hover {
        background: #e1f3d8;
    }

    .private-repo {
        background: #E3D3C4;
        transition-duration: 0.4s;
    }

    .private-repo:hover {
        background: #faecd8;
    }

    .check-info i {
        font-size: 24px;
        color: white;
    }
</style>