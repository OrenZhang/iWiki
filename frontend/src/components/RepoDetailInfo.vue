<template>
    <div class="repo-info">
        <div style="display: flex; align-items: center; margin-bottom: 20px; justify-content: space-between;">
            <div style="display: flex; align-items: center;">
                <h2>{{ repo.name }}</h2>
                <el-tag size="small" v-if="repo.r_type === 'public'" style="margin-left: 10px;" type="success">
                    {{ $t('publicRepo') }}
                </el-tag>
                <el-tag size="small" v-else style="margin-left: 10px;" type="warning">
                    {{ $t('privateRepo') }}
                </el-tag>
            </div>
            <div>
                <el-link v-show="!isMember" :underline="false" @click="showApplyConfirm">
                    <el-tag size="small" style="margin-left: 10px;">
                        {{ $t('applyRepo') }}
                    </el-tag>
                </el-link>
            </div>
        </div>
        <div class="user-avatars">
            <el-avatar class="head-avatar">
                <el-tooltip :content="$t('admin')" placement="top" effect="light">
                    <i class="fa-solid fa-shield" />
                </el-tooltip>
            </el-avatar>
            <div class="users-inline">
                <template v-for="member in repo.admins" :key="member.uid">
                    <el-tooltip :content="member.username" placement="top" effect="light">
                        <el-avatar @click="goTo('user/' + member.username)" :src="member.avatar" v-if="member.avatar !== null" />
                        <el-avatar @click="goTo('user/' + member.username)" v-else>
                            {{ member.username[0].toUpperCase() }}
                        </el-avatar>
                    </el-tooltip>
                </template>
            </div>
        </div>
        <div class="user-avatars" v-if="repo.members !== undefined && repo.members.length > 0">
            <el-avatar class="head-avatar">
                <el-tooltip :content="$t('member')" placement="top" effect="light">
                    <i class="fa-solid fa-users" />
                </el-tooltip>
            </el-avatar>
            <div class="users-inline">
                <template v-for="member in repo.members" :key="member.uid">
                    <el-tooltip :content="member.username" placement="top" effect="light">
                        <el-avatar @click="goTo('user/' + member.username)" :src="member.avatar" v-if="member.avatar !== null" />
                        <el-avatar @click="goTo('user/' + member.username)" v-else>
                            {{ member.username[0].toUpperCase() }}
                        </el-avatar>
                    </el-tooltip>
                </template>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { computed, ref } from 'vue'
    import http from '../api'
    import { ElMessageBox } from 'element-plus'
    import { useRouter } from 'vue-router'
    import message from '../utils/message'
    import { useStore } from 'vuex'
    import { useI18n } from 'vue-i18n'
    import globalContext from '../context'
    
    const { t } = useI18n()
    
    const store = useStore()
    const user = computed(() => store.state.user)
    const router = useRouter()
    
    const emits = defineEmits(['reloadRepoInfo', 'reloadApply', 'handleCurrentChange'])

    const props = defineProps({
        repo: {
            type: Object,
            default: {
                name: '',
                admins: [],
                members: []
            }
        }
    })

    const handleCurrentChange = (page) => {
        emits('handleCurrentChange', page)
    }

    const goTo = (url) => {
        window.open(globalContext.siteUrl + url)
    }
    
    const isMember = computed(() => {
        for (const i in props.repo.admins) {
            if (props.repo.admins[i].uid === user.value.uid) {
                return true
            }
        }
        for (const i in props.repo.members) {
            if (props.repo.members[i].uid === user.value.uid) {
                return true
            }
        }
        return false
    })
    const showApplyConfirm = () => {
        const content = t('applyMsg', { name:props.repo.name })
        ElMessageBox.alert(content, t('applyConfirm'), {
            confirmButtonText: t('applyConfirmed'),
            callback: (action) => {
                if (action === 'confirm') {
                    http.post(
                        '/repo/common/' + props.repo.id + '/apply/'
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
    .repo-info {
        padding: 40px;
        box-sizing: border-box;
        border-radius: 5px;
        background: rgba(255, 255, 255, 0.8);
        min-height: 300px;
        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    }

    .user-avatars {
        display: flex;
    }

    .users-inline {
        display: flex;
        flex-wrap: wrap;
        line-height: 50px;
        width: 100%;
    }

    .user-avatars .el-avatar {
        cursor: pointer;
    }

    .head-avatar {
        background: white;
        cursor: unset!important;
    }

    .el-avatar {
        margin-right: 10px;
        margin-top: 10px;
    }

    .head-avatar .fa-users,
    .head-avatar .fa-shield {
        font-size: 18px;
        margin-top: 12px;
    }

    .admin-dialog h4 {
        margin: 0 0 20px 0;
    }

    :deep(.el-drawer__header) {
        margin-bottom: 10px;
    }
</style>