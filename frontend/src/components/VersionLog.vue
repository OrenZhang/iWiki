<template>
    <div class="version-container">
        <div class="version-box">
            <el-header>
                <h3>{{ $t('versionLog') }}</h3>
                <el-link :underline="false" class="close-button" @click="closeVersion">
                    <i class="fa-solid fa-times" />
                </el-link>
            </el-header>
            <el-main>
                <el-scrollbar class="menu-scroll" style="margin-right: 10px;">
                    <div class="menu">
                        <div v-for="item in versions" :key="item.vid" class="single-version" @click="changeVersion(item)" :class="{ 'highlight-current': item.vid === curVersion }">
                            <div style="padding: 10px; box-sizing: border-box; width: 180px;">
                                <div style="display: flex; width: 100%">
                                    <h4>{{ item.vid }}</h4>
                                    <el-tag style="float: right" v-if="item.is_current" size="mini">
                                        {{ $t('curVersion') }}
                                    </el-tag>
                                </div>
                                <span style="font-size: 12px; color: var(--el-color-info)">{{ item.release_at }}</span>
                            </div>
                        </div>
                    </div>
                </el-scrollbar>
                <el-scrollbar style="margin-top: -18px">
                    <div style="padding: 20px;" v-show="loading">
                        <el-skeleton :rows="5" animated />
                    </div>
                    <div class="content" v-if="!loading" v-html="versionContent" />
                </el-scrollbar>
            </el-main>
        </div>
    </div>
</template>

<script setup>
    import { useStore } from 'vuex'
    import { computed, onMounted, ref } from 'vue'
    import { marked } from 'marked'
    import { listVersionAPI, loadVersionDataAPI } from '../api/modules/common'

    const store = useStore()

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

    const closeVersion = () => {
        store.commit('setVersion', false)
    }

    const versionContent = computed(() => marked.parse(versionData.value.content))
    const versions = ref([])
    const curVersion = ref('')
    const versionData = ref({
        content: ''
    })
    const loadVersionData = () => {
        versionData.value = {
            content: ''
        }
        setLoading(true)
        loadVersionDataAPI(curVersion.value).then(res => {
            versionData.value = res.data
        }).finally(() => {
            setLoading(false)
        })
    }
    const loadVersion = () => {
        listVersionAPI().then(res => {
            versions.value = res.data
            if (versions.value.length > 0) {
                curVersion.value = versions.value[0].vid
                loadVersionData()
            }
        })
    }
    onMounted(() => {
        setLoading(true)
        loadVersion()
    })

    const changeVersion = (row) => {
        curVersion.value = row.vid
        loadVersionData()
    }
</script>

<style scoped>
    .version-container {
        position: fixed;
        height: 100%;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 3000;
        background: var(--u-bg-color-login);
    }

    .version-box {
        height: 480px;
        width: 800px;
        background: var(--el-color-white);
        box-shadow: var(--el-box-shadow-light);
        border-radius: 5px;
        overflow: hidden;
    }

    .version-box .el-header {
        width: 100%;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .version-box .el-main {
        padding: 20px;
        display: flex;
        height: calc(100% - 60px);
        width: 100%;
    }

    .version-box .el-main .content {
        padding: 0 20px 20px 20px;
        box-sizing: border-box;
        width: 100%;
    }

    .version-box .el-main .el-scrollbar:nth-of-type(1) {
        width: 180px;
    }

    .version-box .el-main .el-scrollbar:nth-of-type(2) {
        width: 580px;
    }

    .version-box .el-main .menu {
        width: 180px;
        background: var(--el-color-primary-light-9);
        height: 100%;
    }

    .single-version {
        display: flex;
        cursor: pointer;
        box-sizing: border-box;
        padding-left: 10px;
    }

    .single-version:hover {
        color: var(--el-color-primary-light-1);
    }

    .single-version h4 {
        margin: 0 10px 0 0;
    }

    .highlight-current {
        color: var(--el-color-primary-light-1);
    }

    .close-button :deep(.el-link--inner) i {
        font-size: 18px;
        right: 0;
        top: 0;
    }

    .menu-scroll :deep(.el-scrollbar__view) {
        height: 100%;
    }

    .menu-scroll {
        background: var(--el-color-primary-light-9);
    }

    .el-main .el-scrollbar,
    .el-main :deep(.el-scrollbar__view) {
        overflow-x: hidden;
    }
</style>