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
  <div class="h-100 home-container">
    <el-scrollbar always>
      <div class="main-container">
        <div class="search-box">
          <div>
            <div style="display: flex;">
              <div style="width: 100%; margin-right: 10px; height: 36px;">
                <el-select
                  :no-data-text="$t('homeSearchNotice')"
                  popper-class="home-select-popper"
                  v-model="searchKey"
                  :options="options"
                  :placeholder="$t('homeSearchKey')"
                  style="width: 100%; height: 36px;"
                  allow-create
                  filterable
                  multiple
                  clearable
                  default-first-option
                />
              </div>
              <el-button
                type="primary"
                size="medium"
                @click="docs.paginator.page = 1; searchDocs()"
              >
                {{ $t('search') }}
              </el-button>
              <el-button
                type="primary"
                size="medium"
                @click="resetSearch"
              >
                {{ $t('reset') }}
              </el-button>
            </div>
          </div>
        </div>
        <el-container class="next-container">
          <el-main>
            <div
              class="home-notice-box"
              v-if="homeNotice.showNotice"
            >
              <el-alert
                :title="homeNotice.title"
                :description="homeNotice.desc"
                :type="homeNotice.type"
                :show-icon="homeNotice.showIcon"
              />
            </div>
            <DocPublishChart v-if="showChart" />
            <el-skeleton
              :rows="6"
              animated
              v-show="loading"
            />
            <DocList
              :data="docs"
              @page-change="handlePageChange"
              v-show="!loading"
            />
          </el-main>
          <el-aside>
            <DocSidebar />
          </el-aside>
        </el-container>
      </div>
      <AppFooter />
    </el-scrollbar>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import DocSidebar from '../components/DocSidebar.vue';
import DocList from '../components/DocList.vue';
import message from '../utils/message';
import DocPublishChart from '../components/DocPublishChart.vue';
import { loadDocPublicAPI, searchDocAPI } from '../api/modules/doc';
import { getConfAPI } from '../api/modules/common';
import { setTitle } from '../utils/controller';
import AppFooter from '../components/AppFooter.vue';

// 加载状态
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

// 文章列表
const docs = ref({
  usePaginator: true,
  paginator: {
    page: 1,
    count: 0,
    size: 10,
  },
  data: [],
});
const loadDocs = () => {
  setLoading(true);
  loadDocPublicAPI(docs.value.paginator.size, docs.value.paginator.page).then((res) => {
    docs.value.data = res.data.results;
    docs.value.paginator.count = res.data.count;
    docs.value.paginator.page = res.data.page;
  }, (err) => {
    message(err.data.msg, 'error');
    if (err.data.code === 404) {
      docs.value.paginator.page = 1;
      loadDocs();
    }
  })
    .finally(() => {
      setLoading(false);
    });
};
onMounted(loadDocs);

// 搜索
const searchKey = ref([]);
const options = ref([]);
const searchDocs = () => {
  setLoading(true);
  searchDocAPI(searchKey.value, docs.value.paginator.page, docs.value.paginator.size).then((res) => {
    docs.value.data = res.data.results;
    docs.value.paginator.count = res.data.count;
    docs.value.paginator.page = res.data.page;
  }, (err) => {
    message(err.data.msg, 'warning');
  })
    .finally(() => {
      setLoading(false);
    });
};
const resetSearch = () => {
  searchKey.value = [];
  docs.value.paginator.page = 1;
  loadDocs();
};

const handlePageChange = (page) => {
  docs.value.paginator.page = page;
  if (searchKey.value.length > 0) {
    searchDocs();
  } else {
    loadDocs();
  }
};

// 提示信息
const homeNotice = ref({
  title: '',
  desc: '',
  showIcon: true,
  type: 'info',
  showNotice: false,
});
const getHomeNotice = () => {
  getConfAPI('home_notice').then((res) => {
    if (res.result) {
      homeNotice.value = res.data;
    }
  });
};
onMounted(getHomeNotice);

onMounted(() => {
  setTitle();
});

const showChart = ref(false);
const checkShowChart = () => {
  getConfAPI('show_doc_publish_chart').then((res) => {
    if (res.result) {
      showChart.value = res.data;
    }
  });
};
onMounted(checkShowChart);
</script>

<style scoped>
    @import '../assets/Home.css';
</style>
