<template>
    <div class="admin-container">
        <div class="head-box">
            {{ repoName }}
        </div>
        <div style="max-width: 1440px; box-sizing: border-box; padding: 40px; margin: 0 auto">
            <el-select-v2
                class="admin-header-select"
                v-model="curRepoID"
                :options="options"
                size="medium"
                filterable
                :placeholder="$t('chooseRepo')"
            />
            <el-container class="admin-container-box">
                <el-aside width="120px">
                    <el-menu
                        @select="changeActiveIndex"
                        :default-active="activeIndex"
                        :ellipsis="false">
                        <el-menu-item index="member">
                            {{ $t('memberManage') }}
                        </el-menu-item>
                        <el-menu-item index="doc">
                            {{ $t('docManage') }}
                        </el-menu-item>
                    </el-menu>
                </el-aside>
                <el-main>
                    <keep-alive>
                        <component :is="curComponent" :repo-id="curRepoID" />
                    </keep-alive>
                </el-main>
            </el-container>
        </div>
    </div>
</template>

<script setup>
    import { computed, onMounted, ref } from 'vue'
    import http from '../api'
    import AdminMember from '../components/AdminMember.vue'
    import AdminDoc from '../components/AdminDoc.vue'

    const repoName = computed(() => {
        for (const i in repos.value) {
            if (repos.value[i].id === curRepoID.value) {
                return repos.value[i].name
            }
        }
        return ''
    })
    const curComponent = computed(() => {
        switch (activeIndex.value) {
            case 'doc':
                return AdminDoc
            case 'member':
                return AdminMember
            default:
                return AdminMember
        }
    })
    const curRepoID = ref('')
    const repos = ref([])
    const options = computed(() => {
        return repos.value.map((item) => {
            return {
                value: item.id,
                label: item.name
            }
        })
    })
    const loadRepo = () => {
        http.get(
            '/repo/manage/load_repo/'
        ).then(res => {
            repos.value = res.data
            if (repos.value.length > 0 && !curRepoID.value) {
                curRepoID.value = repos.value[0].id
            }
        })
    }
    onMounted(loadRepo)

    const activeIndex = ref('member')
    const changeActiveIndex = (index) => {
        activeIndex.value = index
    }
</script>

<style scoped>
    @import "../assets/Admin.css";
</style>