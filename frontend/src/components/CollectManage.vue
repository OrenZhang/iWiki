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
  <div class="collect-manage">
    <div class="tool-bar">
      <div style="display: flex">
        <el-input
          size="medium"
          class="search-input"
          clearable
          :placeholder="$t('docTitle')"
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
      :data="docs"
      v-show="!loading"
      :show-header="false"
    >
      <el-table-column :label="$t('title')">
        <template #default="scope">
          <el-tag
            size="small"
            effect="plain"
          >
            {{ scope.row.repo_name }}
          </el-tag>
          {{ scope.row.title }}
        </template>
      </el-table-column>
      <el-table-column
        :label="$t('author')"
        prop="creator_name"
        width="200px"
      />
      <el-table-column
        :label="$t('updateAt')"
        prop="update_at"
        width="200px"
      />
      <el-table-column
        :label="$t('operation')"
        width="160px"
      >
        <template #default="scope">
          <el-button
            type="text"
            @click="goTo('doc/' + scope.row.doc_id)"
          >
            {{ $t('open') }}
          </el-button>
          <el-button
            type="text"
            @click="showCancelCollectConfirm(scope.row)"
          >
            {{ $t('cancelCollect') }}
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import message from '../utils/message';
import { ElMessageBox } from 'element-plus';
import { useI18n } from 'vue-i18n';
import globalContext from '../context';
import { loadCollectDocAPI, unCollectDocAPI } from '../api/modules/doc';

const { t } = useI18n();

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

const goTo = (url) => {
  window.open(globalContext.siteUrl + url);
};

const docs = ref([]);
const searchKey = ref('');
const paginator = ref({
  page: 1,
  count: 0,
});
const handlePageChange = (page) => {
  paginator.value.page = page;
  loadDocs();
};
const loadDocs = () => {
  setLoading(true);
  loadCollectDocAPI(paginator.value.page, searchKey.value).then((res) => {
    docs.value = res.data.results;
    paginator.value.count = res.data.count;
  }, (err) => {
    message(err.data.msg, 'error');
  })
    .finally(() => {
      setLoading(false);
    });
};
onMounted(loadDocs);

const doSearch = () => {
  paginator.value.page = 1;
  loadDocs();
};
const resetSearch = () => {
  searchKey.value = '';
  paginator.value.page = 1;
  loadDocs();
};

const showCancelCollectConfirm = (row) => {
  const content = t('cancelCollectDocConfirmContent', { title: row.title });
  ElMessageBox.alert(content, t('cancelConfirm'), {
    confirmButtonText: t('cancelConfirmed'),
    callback: (action) => {
      if (action === 'confirm') {
        unCollectDocAPI(row.doc_id).then(() => {
          loadDocs();
        }, (err) => {
          message(err.data.msg, 'error');
        });
      }
    },
  });
};
</script>

<style scoped>
    .tool-bar {
        width: 100%;
        display: flex;
        justify-content: space-between;
    }

    .tool-bar .el-pagination {
        display: flex;
        align-items: center;
    }

    .tool-bar .el-button {
        margin-left: 10px;
    }

    .el-table {
        margin-top: 20px;
    }

    .tool-bar .el-input {
        max-width: 240px;
    }

    .tool-bar .el-select {
        margin-left: 10px;
    }

    .tool-bar .el-select,
    .tool-bar .el-select .el-input {
        width: 120px;
    }

    .search-input {
        height: 100%;
    }

    .search-input :deep(.el-input__inner) {
        height: 100%;
    }
</style>
