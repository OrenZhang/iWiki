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
  <div class="comment-manage">
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
      :data="comments"
      v-show="!loading"
      :show-header="false"
    >
      <el-table-column :label="$t('comment')">
        <template #default="scope">
          <el-tag
            size="small"
            type="plain"
          >
            {{ scope.row.title }}
          </el-tag>
          <br>
          {{ getContent(scope.row) }}
        </template>
      </el-table-column>
      <el-table-column
        :label="$t('updateAt')"
        prop="update_at"
        width="200px"
      />
      <el-table-column
        :label="$t('operation')"
        width="120px"
      >
        <template #default="scope">
          <el-button
            type="text"
            @click="goTo(globalContext.siteUrl + 'doc/' + scope.row.doc_id)"
          >
            {{ $t('open') }}
          </el-button>
          <el-button
            type="text"
            @click="deleteConfirm(scope.row)"
          >
            {{ $t('delete') }}
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
import { deleteCommentAPI, loadUserCommentAPI } from '../api/modules/comment';

const { t } = useI18n();

const loading = ref(false);
const setLoading = (status) => {
  if (status) {
    loading.value = true;
  } else {
    setTimeout(() => {
      loading.value = false;
    }, 600);
  }
};

const comments = ref([]);
const searchKey = ref('');
const paginator = ref({
  page: 1,
  count: 0,
});
const getContent = (row) => {
  if (row.content.length > 50) {
    return `${row.content.slice(0, 50)}……`;
  }
  return row.content;
};
const loadComments = () => {
  setLoading(true);
  loadUserCommentAPI(paginator.value.page, 10, searchKey.value).then(
    (res) => {
      comments.value = res.data.results;
      paginator.value.count = res.data.count;
    },
    err => message(err.data.msg, 'error'),
  )
    .finally(() => {
      setLoading(false);
    });
};
const handlePageChange = (page) => {
  paginator.value.page = page;
  loadComments();
};
const doSearch = () => {
  paginator.value.page = 1;
  loadComments();
};
const resetSearch = () => {
  searchKey.value = '';
  paginator.value.page = 1;
  loadComments();
};
onMounted(loadComments);

const deleteConfirm = (row) => {
  const content = t('deleteCommentMsg', { name: row.name });
  ElMessageBox.alert(content, t('deleteConfirm'), {
    confirmButtonText: t('deleteConfirmed'),
    callback: (action) => {
      if (action === 'confirm') {
        deleteCommentAPI(row.id).then(() => {
          loadComments();
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
