<template>
    <div class="user-info-box">
        <div>
            <el-upload
                :action="avatarUrl"
                :with-credentials="true"
                :show-file-list="false"
                :disabled="avatarDisabled"
                :on-success="handleAvatarSuccess"
                :before-upload="beforeAvatarUpload">
                <el-avatar v-if="userInfo.avatar !== null && userInfo.avatar!== ''" :src="userInfo.avatar" :size="100" />
                <el-avatar v-else :size="100">
                    <i class="fa-solid fa-user" />
                </el-avatar>
            </el-upload>
            <div class="user-info-text">
                <h2>
                    {{ userInfo.username }}
                    <el-tag v-show="showLogout && user.uid === userInfo.uid && user.auth" class="edit-info" effect="plain" size="small" @click="doLogout">
                        {{ $t('logout') }}
                    </el-tag>
                </h2>
                <p>{{ $t('registryAt') }}:&nbsp;{{ userInfo.date_joined }}</p>
            </div>
        </div>
        <div style="display: flex">
            <div class="user-statistic-single">
                <h4>{{ $t('memberRepos') }}</h4>
                <p>{{ userInfo.property.repo_count }}</p>
            </div>
            <div class="user-statistic-single">
                <h4>{{ $t('releaseDocs') }}</h4>
                <p>{{ userInfo.property.doc_count }}</p>
            </div>
            <div class="user-statistic-single">
                <h4>{{ $t('commentCount') }}</h4>
                <p>{{ userInfo.property.comment_count }}</p>
            </div>
            <div class="user-statistic-single">
                <h4>{{ $t('activeIndex') }}</h4>
                <p>{{ transIndex(userInfo.property.active_index) }}</p>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { useStore } from 'vuex'
    import message from '../utils/message'
    import { computed } from 'vue'
    import globalContext from '../context'
    import http from '../api'
    import { useRouter } from 'vue-router'
    import { useI18n } from 'vue-i18n'

    const store = useStore()
    const router = useRouter()
    const user = computed(() => store.state.user)
    
    const { t } = useI18n()
    
    defineProps({
        userInfo: {
            type: Object,
            default: {}
        },
        avatarDisabled: {
            type: Boolean,
            default: true
        },
        showLogout: {
            type: Boolean,
            default: true
        }
    })

    const transIndex = (num) => {
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

    const avatarUrl = computed(() => globalContext.backEndUrl + '/cos/upload_avatar/')
    const handleAvatarSuccess = () => {
        store.dispatch('getUserInfo')
    }
    const beforeAvatarUpload = (file) => {
        const isPic = file.type === 'image/jpeg' || file.type === 'image/png'
        const isLt2M = file.size / 1024 / 1024 < 2
        if (!isPic) {
            message(t('useJPGorPNG'), 'error')
        }
        if (!isLt2M) {
            message(t('upto2M'), 'error')
        }
        return isPic && isLt2M
    }
    
    const doLogout = () => {
        http.get(
            '/account/sign_out/'
        ).then(() => {
            store.dispatch('getUserInfo')
            router.push({ name: 'Home' })
        })
    }
</script>

<style scoped>
    .user-info-box {
        max-width: 1440px;
        margin: -92px auto 0;
        padding: 40px;
        box-sizing: border-box;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .user-info-box .el-avatar {
        background: white;
        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    }

    .user-info-box i {
        font-size: 48px;
        margin-top: 24px;
        color: #8cc5ff;
    }

    .user-info-text {
        margin-left: 20px;
        color: white;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .user-info-text h2 {
        margin-top: 0;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
    }

    .user-info-text p {
        margin: 0;
        font-size: 14px;
        color: #606266;
    }

    .user-info-box > div {
        display: flex;
    }

    .user-statistic-single {
        display: flex;
        flex-direction: column;
        align-items: center;
        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
        background: white;
        border-radius: 5px;
        margin-left: 10px;
        box-sizing: border-box;
        padding: 10px;
        width: 92px;
    }

    .user-statistic-single h4 {
        margin: 0;
    }

    .user-statistic-single p {
        margin: 20px 0 0 0;
        color: #409EFF;
    }

    .edit-info {
        margin-left: 10px;
        background: rgba(255, 255, 255, 0.8);
        border: none;
        cursor: pointer;
    }
</style>