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
  <div class="repo-manage">
    <div class="tool-bar">
      <div style="display: flex">
        <el-input
          size="medium"
          class="search-input"
          clearable
          :placeholder="$t('repoName')"
          v-model="searchKey"
        />
        <el-button
          size="medium"
          type="primary"
          @click="doSearch"
        >
          {{ $t('search') }}
        </el-button>
        <el-button
          size="medium"
          type="primary"
          @click="resetSearch"
        >
          {{ $t('reset') }}
        </el-button>
      </div>
      <el-pagination
        background
        layout="prev, pager, next"
        :total="paginator.count"
        :pager-count="5"
        :current-page="paginator.page"
        @current-change="handlePageChange"
      />
    </div>
    <el-skeleton
      :rows="6"
      v-show="loading"
      animated
      style="margin-top: 20px"
    />
    <el-table
      size="medium"
      :data="repos"
      v-show="!loading"
      :show-header="false"
    >
      <el-table-column
        :label="$t('repoName')"
        prop="name"
      />
      <el-table-column
        :label="$t('repoType')"
        width="120px"
      >
        <template #default="scope">
          <el-tag
            size="small"
            v-if="scope.row.r_type === 'public'"
          >
            {{ $t('publicRepo') }}
          </el-tag>
          <el-tag
            size="small"
            v-else
            type="warning"
          >
            {{ $t('privateRepo') }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column
        :label="$t('operation')"
        width="120px"
      >
        <template #default="scope">
          <el-button
            type="text"
            @click="goTo(globalContext.siteUrl + 'repo/' + scope.row.id)"
          >
            {{ $t('open') }}
          </el-button>
          <el-button
            type="text"
            @click="showExitConfirm(scope.row)"
            :disabled="scope.row.creator === user.uid"
          >
            {{ $t('exit') }}
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import message from '../utils/message';
import { ElMessageBox } from 'element-plus';
import { useStore } from 'vuex';
import { useI18n } from 'vue-i18n';
import globalContext from '../context';
import { exitRepoAPI, loadRepoAPI } from '../api/modules/repo';

const { t } = useI18n();

const store = useStore();
const user = computed(() => store.state.user);

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

const repos = ref([]);
const searchKey = ref('');
const paginator = ref({
  page: 1,
  count: 0,
});
const loadRepos = () => {
  setLoading(true);
  loadRepoAPI(paginator.value.page, searchKey.value).then((res) => {
    repos.value = res.data.results;
    paginator.value.count = res.data.count;
  }, (err) => {
    message(err.data.msg, 'error');
  })
    .finally(() => {
      setLoading(false);
    });
};
onMounted(loadRepos);

const handlePageChange = (page) => {
  paginator.value.page = page;
  loadRepos();
};
const doSearch = () => {
  paginator.value.page = 1;
  loadRepos();
};
const resetSearch = () => {
  searchKey.value = '';
  paginator.value.page = 1;
  loadRepos();
};

const showExitConfirm = (row) => {
  const content = t('exitConfirmMsg', { name: row.name });
  ElMessageBox.alert(content, t('exitConfirm'), {
    confirmButtonText: t('exitConfirmed'),
    callback: (action) => {
      if (action === 'confirm') {
        exitRepoAPI(row.id).then(() => {
          loadRepos();
        }, (err) => {
          message(err.data.msg, 'error');
        });
      }
    },
  });
};

const goTo = (url) => {
  window.open(url);
};
</script>

<style scoped>
    .tool-bar {
        width: 100%;
        display: flex;
        justify-content: space-between;
        margin-bottom: 20px;
    }

    .search-input {
        margin-right: 10px;
    }
</style>
