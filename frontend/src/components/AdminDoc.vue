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
  <div>
    <div class="admin-doc-header">
      <div>
        <el-input
          v-model="searchKey"
          size="medium"
          :placeholder="$t('titleSearchKey')"
        />
        <el-button
          size="medium"
          type="primary"
          style="margin-left: 10px;"
          @click="paginator.page = 1; loadDoc()"
        >
          {{ $t('search') }}
        </el-button>
        <el-button
          size="medium"
          type="primary"
          style="margin-left: 10px;"
          @click="searchKey = '';paginator.page = 1; loadDoc()"
        >
          {{ $t('reset') }}
        </el-button>
      </div>
      <el-pagination
        background
        layout="total, prev, pager, next, sizes"
        :current-page="paginator.page"
        :total="paginator.count"
        :page-size="paginator.size"
        @current-change="handlePageChange"
        @size-change="handleSizeChange"
      />
    </div>
    <div class="admin-doc-main">
      <el-table :data="docs">
        <el-table-column :label="$t('title')">
          <template #default="scope">
            <el-link
              type="primary"
              :underline="false"
              @click="goTo(scope.row)"
            >
              {{ scope.row.title }}
            </el-link>
          </template>
        </el-table-column>
        <el-table-column
          prop="creator_name"
          :label="$t('author')"
        />
        <el-table-column
          prop="update_at"
          :label="$t('updateAt')"
        />
        <el-table-column
          :label="$t('operation')"
          width="300"
        >
          <template #default="scope">
            <el-link
              v-show="!scope.row.pin_status"
              type="primary"
              :underline="false"
              style="margin-left: 10px"
              @click="showPinDoc(scope.row)"
            >
              {{ $t('pinDoc') }}
            </el-link>
            <el-link
              v-show="scope.row.pin_status"
              type="primary"
              :underline="false"
              style="margin-left: 10px"
              @click="unpinDoc(scope.row)"
            >
              {{ $t('unpinDoc') }}
            </el-link>
            <el-link
              type="primary"
              :underline="false"
              style="margin-left: 10px"
              @click="changeDoc(scope.row, 'available', 'private')"
            >
              {{ $t('toPrivate') }}
            </el-link>
            <el-link
              type="primary"
              :underline="false"
              style="margin-left: 10px"
              @click="changeDoc(scope.row, 'is_publish', false)"
            >
              {{ $t('toDraft') }}
            </el-link>
            <el-link
              type="danger"
              :underline="false"
              style="margin-left: 10px"
              @click="showDeleteConfirm(scope.row)"
            >
              {{ $t('delete') }}
            </el-link>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <el-dialog
      v-model="pinDocDialog.visible"
      :title="$t('pinDoc')"
      width="360px"
    >
      <el-form
        label-width="80px"
        label-position="left"
      >
        <el-form-item :label="$t('title')">
          <el-input
            v-model="pinDocDialog.data.title"
            disabled
          />
        </el-form-item>
        <el-form-item :label="$t('pinTo')">
          <el-date-picker
            v-model="pinDocDialog.data.pin_to"
            type="datetime"
            :disabled-date="checkDate"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="pinDocDialog.visible = false">{{ $t('cancel') }}</el-button>
          <el-button
            type="primary"
            @click="doPinDoc"
          >{{ $t('submit') }}</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import moment from 'moment';
import { onMounted, ref, watch, defineProps } from 'vue';
import { ElMessageBox } from 'element-plus';
import { useI18n } from 'vue-i18n';
import globalContext from '../context';
import {
  changeDocStatusAdminAPI,
  deleteDocAdminAPI,
  loadDocByRepoAdminAPI, pinDocAdminAPI,
  unPinDocAdminAPI,
} from '../api/modules/doc';

const { t } = useI18n();

const props = defineProps({
  repoId: {
    type: String,
    default: '',
  },
});

const docs = ref([]);
const searchKey = ref('');
const paginator = ref({
  page: 1,
  size: 10,
  count: 0,
});
const handlePageChange = (page) => {
  paginator.value.page = page;
  loadDoc();
};
const handleSizeChange = (size) => {
  paginator.value.page = 1;
  paginator.value.size = size;
  loadDoc();
};
const loadDoc = () => {
  if (!props.repoId) {
    return;
  }
  loadDocByRepoAdminAPI(props.repoId, paginator.value.page, paginator.value.size, searchKey.value).then((res) => {
    docs.value = res.data.results;
    paginator.value.count = res.data.count;
  });
};
onMounted(loadDoc);
watch(() => props.repoId, () => {
  paginator.value.page = 1;
  loadDoc();
});

const showDeleteConfirm = (row) => {
  const content = t('deleteDocConfirmContent', { title: row.title });
  ElMessageBox.alert(content, t('deleteConfirm'), {
    confirmButtonText: t('deleteConfirmed'),
    callback: (action) => {
      if (action === 'confirm') {
        deleteDocAdminAPI(props.repoId, row.id).finally(() => {
          loadDoc();
        });
      }
    },
  });
};

const goTo = (row) => {
  window.open(`${globalContext.siteUrl}doc/${row.id}`);
};

const changeDoc = (row, key, val) => {
  const data = {};
  data[key] = val;
  changeDocStatusAdminAPI(row.id, data).finally(() => {
    loadDoc();
  });
};

const showPinDoc = (row) => {
  pinDocDialog.value.data.title = row.title;
  pinDocDialog.value.data.doc_id = row.id;
  pinDocDialog.value.visible = true;
};
const pinDocDialog = ref({
  visible: false,
  data: {
    title: '',
    doc_id: '',
    pin_to: new Date(new Date().getTime() + 24 * 60 * 60 * 1000),
  },
});
const checkDate = date => date < new Date(new Date(new Date().toLocaleDateString()).getTime());
const unpinDoc = (row) => {
  unPinDocAdminAPI(props.repoId, row.id).then(() => {
    loadDoc();
  });
};
const doPinDoc = () => {
  pinDocDialog.value.visible = false;
  const data = {
    doc_id: pinDocDialog.value.data.doc_id,
    pin_to: moment(pinDocDialog.value.data.pin_to).format('YYYY-MM-DD HH:mm:ss'),
  };
  pinDocDialog.value.data.doc_id = '';
  pinDocDialog.value.data.title = '';
  pinDocAdminAPI(props.repoId, data).then(() => {
    loadDoc();
  });
};
</script>

<style scoped>
    .admin-doc-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .admin-doc-header > div {
        display: flex;
    }

    .admin-doc-header .el-pagination :deep(.el-pagination__sizes) {
        margin: 0;
    }
</style>
