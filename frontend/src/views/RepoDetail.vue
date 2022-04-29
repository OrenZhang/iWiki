<!--
 - MIT License
 -
 - Copyright (c) 2021 Oren Zhang
 -
 - Permission is hereby granted, free of charge, to any person obtaining a copy
 - of this software and associated documentation files (the "Software"), to deal
 - in the Software without restriction, including without limitation the rights
 - to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 - copies of the Software, and to permit persons to whom the Software is
 - furnished to do so, subject to the following conditions:
 -
 - The above copyright notice and this permission notice shall be included in all
 - copies or substantial portions of the Software.
 -
 - THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 - IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 - FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 - AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 - LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 - OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 - SOFTWARE.
-->

<template>
  <div class="h-100 repo-container">
    <el-scrollbar always>
      <div class="main-container">
        <div class="head-box" />
        <div class="box-container">
          <RepoDetailInfo
            :is-admin="isAdmin"
            :repo="repo"
            @reload-repo-info="loadRepoInfo"
          />
        </div>
        <div class="content-box">
          <el-main>
            <el-skeleton
              :rows="6"
              animated
              v-show="loading"
            />
            <PinDocList
              :repo-id="repoId"
              v-show="!loading"
            />
            <DocList
              :data="docs"
              @page-change="handlePageChange"
              v-show="!loading"
            />
          </el-main>
          <el-aside>
            <div class="search-bar">
              <el-input
                v-model="searchKey"
                :placeholder="$t('title')"
              />
              <el-button @click="doSearch">
                <i class="fa-solid fa-search" />
              </el-button>
            </div>
            <DocSidebar />
          </el-aside>
        </div>
      </div>
    </el-scrollbar>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router';
import { computed, onMounted, ref } from 'vue';
import RepoDetailInfo from '../components/RepoDetailInfo.vue';
import DocSidebar from '../components/DocSidebar.vue';
import DocList from '../components/DocList.vue';
import { useStore } from 'vuex';
import PinDocList from '../components/PinDocList.vue';
import { loadRepoDetailAPI } from '../api/modules/repo';
import { loadRepoDocAPI } from '../api/modules/doc';
import { setTitle } from '../utils/controller';

const store = useStore();
const user = computed(() => store.state.user);

const route = useRoute();
const repoId = route.params.id;

const repo = ref({});
const loadRepoInfo = () => {
  loadRepoDetailAPI(repoId).then((res) => {
    repo.value = res.data;
    setTitle(repo.value.name);
  });
};
onMounted(loadRepoInfo);

const loading = ref(true);
const setLoading = (status) => {
  if (status) {
    loading.value = true;
  } else {
    setTimeout(() => {
      loading.value = false;
    }, 600);
  }
};

const docs = ref({
  usePaginator: true,
  paginator: {
    page: 1,
    count: 0,
    size: 10,
  },
  data: [],
});
const handlePageChange = (page) => {
  docs.value.paginator.page = page;
  loadDocs();
};
const searchKey = ref('');
const doSearch = () => {
  docs.value.paginator.page = 1;
  loadDocs();
};
const loadDocs = () => {
  setLoading(true);
  loadRepoDocAPI(repoId, searchKey.value, docs.value.paginator.page).then((res) => {
    docs.value.data = res.data.results;
    docs.value.paginator.count = res.data.count;
  })
    .finally(() => {
      setLoading(false);
    });
};
onMounted(loadDocs);

const isAdmin = computed(() => {
  for (const i in repo.value.admins) {
    if (repo.value.admins[i].uid === user.value.uid) {
      return true;
    }
  }
  return false;
});
</script>

<style scoped>
    @import "../assets/RepoDetail.css";
</style>
