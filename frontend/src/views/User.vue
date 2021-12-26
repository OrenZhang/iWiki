<template>
    <div class="h-100">
        <el-scrollbar always>
            <div class="head-box" />
            <HUserInfoBox :show-logout="false" :user-info="searchUserInfo" />
            <div class="doc-list">
                <el-skeleton :rows="6" animated v-show="docLoading" />
                <DocList :data="docData" @pageChange="handlePageChange" v-show="!docLoading" />
            </div>
        </el-scrollbar>
    </div>
</template>

<script setup>
    import { onMounted, ref, watch } from 'vue'
    import { useRoute } from 'vue-router'
    import http from '../api'
    import message from '../utils/message'
    import DocList from '../components/DocList.vue'
    import HUserInfoBox from '../components/HUserInfoBox.vue'
    
    const roure = useRoute()

    const searchUser = ref('')
    const searchUserInfo = ref({
        uid: '',
        username: '',
        avatar: '',
        date_joined: '',
        property: {
            repo_count: 0,
            doc_count: 0,
            comment_count: 0,
            active_index: 0
        }
    })
    const loadUser = () => {
        http.get(
            '/account/user_info/' + searchUser.value + '/'
        ).then(res => {
            searchUserInfo.value = res.data
        }, err => {
            message(err.data.msg, 'error')
        })
    }

    const docData = ref({
        usePaginator: true,
        paginator: {
            page: 1,
            count: 0
        },
        data: []
    })
    const handlePageChange = (page) => {
        docData.value.paginator.page = page
        loadUserDoc()
    }
    const docLoading = ref(true)
    const loadUserDoc = () => {
        docLoading.value = true
        http.get(
            '/doc/public/user_doc/?username=' + searchUser.value + '&page=' + docData.value.paginator.page
        ).then(res => {
            docData.value.data = res.data.results
            docData.value.paginator.count = res.data.count
        }, err => {
            message(err.data.msg, 'error')
        }).finally(() => {
            setTimeout(() => {
                docLoading.value = false
            }, 600)
        })
    }

    const loadData = () => {
        searchUser.value = roure.params.username
        loadUser()
        loadUserDoc()
    }
    onMounted(loadData)
    watch(() => roure.params.username, (newVal, oldVal) => {
        if (newVal !== oldVal && newVal) {
            loadData()
        }
    })
</script>

<style scoped>
    @import "../assets/User.css";
</style>