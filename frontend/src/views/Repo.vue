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
  <div class="repo-container">
    <div class="search-box">
      <div>
        <div style="display: flex;">
          <div style="width: 100%; margin-right: 10px; ">
            <el-input
              size="medium"
              :placeholder="$t('repoName')"
              v-model="searchKey"
            />
          </div>
          <el-button
            type="primary"
            size="medium"
            @click="doSearch"
          >
            {{ $t('search') }}
          </el-button>
          <el-button
            type="success"
            size="medium"
            @click="createDialog.visible = true"
          >
            {{ $t('create') }}
          </el-button>
        </div>
      </div>
    </div>
    <div class="repo-type-box">
      <el-button
        size="medium"
        :type="!isMember ? 'primary' : ''"
        @click="handleRepoTypeChange(false)"
      >
        {{ $t('allRepos') }}
      </el-button>
      <el-button
        size="medium"
        :type="isMember ? 'primary' : ''"
        @click="handleRepoTypeChange(true)"
      >
        {{ $t('myJoinedRepos') }}
      </el-button>
    </div>
    <div class="card-container">
      <RepoCards
        :repos="repos"
        @load-more="loadMore"
      />
    </div>
    <div
      class="load-more"
      v-show="hasMore"
    >
      <el-link
        :underline="false"
        v-show="!loading"
        @click="loadMore"
      >
        <div>{{ $t('loadMore') }}</div>
        <i class="fa-solid fa-chevron-down" />
      </el-link>
      <el-link
        :underline="false"
        v-show="loading"
      >
        <div>{{ $t('loading') }}</div>
      </el-link>
    </div>
    <div
      class="load-more"
      v-show="!hasMore"
    >
      {{ $t('noMoreData') }}
    </div>
    <el-dialog
      v-model="createDialog.visible"
      :title="$t('createRepo')"
      width="400px"
      @close="handleCreateClose"
    >
      <el-form
        label-width="60px"
        label-position="left"
      >
        <el-form-item :label="$t('repoName')">
          <el-input v-model="createDialog.data.name" />
          <div style="color: var(--el-color-danger); font-size: 12px; margin-bottom: -20px;">
            {{ $t('repoNameWarning') }}
          </div>
        </el-form-item>
        <el-form-item :label="$t('repoType')">
          <el-select v-model="createDialog.data.r_type">
            <el-option
              v-for="item in options"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="createDialog.visible = false">{{ $t('cancel') }}</el-button>
          <el-button
            type="success"
            @click="doCreate(createDialog.data)"
            :disabled="createDialog.data.name.length === 0"
          >{{ $t('create') }}</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import RepoCards from '../components/RepoCards.vue';
import message from '../utils/message';
import { useI18n } from 'vue-i18n';
import { createRepoAPI, loadRepoAPI, loadRepoWithUserAPI } from '../api/modules/repo';
import { setTitle } from '../utils/controller';

const { t } = useI18n();

const searchKey = ref('');
const paginator = ref({
  page: 1,
  count: 0,
  size: 16,
});

const loading = ref(true);

const isMember = ref(false);
const repos = ref([]);
const loadRepo = (refresh) => {
  loading.value = true;
  let loadFunc;
  if (isMember.value) {
    loadFunc = loadRepoAPI(paginator.value.page, searchKey.value);
  } else {
    loadFunc = loadRepoWithUserAPI(paginator.value.page, searchKey.value);
  }
  loadFunc.then((res) => {
    if (refresh) {
      repos.value = res.data.results;
    } else {
      repos.value = repos.value.concat(res.data.results);
    }
    paginator.value.count = res.data.count;
  }).finally(() => {
    setTimeout(() => {
      loading.value = false;
    }, 600);
  });
};
onMounted(loadRepo);
const doSearch = () => {
  paginator.value.page = 1;
  loadRepo(true);
};
const handleRepoTypeChange = (typeString) => {
  isMember.value = typeString;
  paginator.value.page = 1;
  loadRepo(true);
};

const hasMore = computed(() => (paginator.value.count - paginator.value.page * paginator.value.size) > 0);
const loadMore = () => {
  if (hasMore.value) {
    paginator.value.page += 1;
    loadRepo(false);
  }
};

const createDialog = ref({
  visible: false,
  data: {
    name: '',
    r_type: 'public',
  },
});
const options = ref([
  {
    id: 'public',
    name: t('publicRepo'),
  },
  {
    id: 'private',
    name: t('privateRepo'),
  },
]);
const handleCreateClose = () => {
  createDialog.value.data = {
    name: '',
    r_type: 'public',
  };
};
const doCreate = (data) => {
  createRepoAPI(data).then(() => {
    createDialog.value.visible = false;
    loadRepo(true);
  }, (err) => {
    if (err.data.msg.indexOf('已存在') !== -1) {
      message(t('duplicateRepoName'), 'error');
    } else {
      message(err.data.msg, 'error');
    }
  });
};

onMounted(() => {
  setTitle(t('Repo'));
});
</script>

<style scoped>
    .search-box {
        background: url("/extra-assests/imgs/bg-1.webp") no-repeat;
        background-size: cover;
        height: 30vh;
        min-height: 240px;
        max-height: 600px;
        display: flex;
        align-items: center;
    }

    .search-box > div {
        text-align: center;
        max-width: 540px;
        margin: 0 auto;
        width: 100%;
    }

    .search-box .el-input :deep(.el-input__inner) {
        text-align: center;
    }

    .search-box :deep(input),
    .search-box :deep(.el-button),
    .search-box :deep(.el-select-v2__wrapper) {
        border: unset;
        box-shadow: var(--el-box-shadow-light);
    }

    .repo-container {
        margin: 0 auto;
        box-sizing: border-box;
    }

    .toolbar .el-input {
        width: 240px;
        margin-right: 10px;
    }

    .repo-type-box,
    .card-container {
        box-sizing: border-box;
        padding: 40px;
        max-width: 1440px;
        margin: 0 auto;
    }

    .repo-type-box {
        padding-bottom: 0;
    }

    .load-more {
        padding-bottom: 40px;
    }

    .load-more,
    .load-more :deep(.el-link--inner) {
        font-size: 14px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        line-height: 24px;
    }

    .el-select {
        width: 100%;
    }

    .el-form-item .el-input :deep(.el-input__inner),
    .el-form-item .el-select :deep(.select-trigger),
    .el-form-item .el-select :deep(.select-trigger) .el-input,
    .el-form-item .el-select :deep(.select-trigger) .el-input .el-input__inner {
        height: 36px!important;
    }
</style>
