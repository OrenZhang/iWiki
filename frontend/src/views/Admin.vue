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
  <div class="admin-container">
    <div class="head-box">
      {{ repoName }}
    </div>
    <div class="main-box">
      <div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
        <el-select-v2
          class="admin-header-select"
          v-model="curRepoID"
          :options="options"
          size="medium"
          filterable
          :placeholder="$t('chooseRepo')"
        />
        <div style="display: flex;">
          <el-select
            @change="changeRepoType"
            class="admin-header-select2"
            v-model="repoType"
            :placeholder="$t('repoType')"
          >
            <el-option
              v-for="item in repoTypeOptions"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
          <el-button
            type="danger"
            size="medium"
            v-show="isOwner"
            @click="showDeleteConfirm"
          >
            {{ $t('deleteRepo') }}
          </el-button>
          <el-button
            type="primary"
            size="medium"
            v-show="isSuperAdmin"
            @click="goToBackend"
          >
            {{ $t('backendAdmin') }}
          </el-button>
        </div>
      </div>
      <el-container class="admin-container-box">
        <el-aside width="120px">
          <el-menu
            @select="changeActiveIndex"
            :default-active="activeIndex"
            :ellipsis="false"
          >
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
            <component
              :is="curComponent"
              :repo-id="curRepoID"
            />
          </keep-alive>
        </el-main>
      </el-container>
    </div>
    <el-dialog
      v-model="deleteDialog.visible"
      custom-class="delete-dialog"
      :title="$t('deleteConfirm')"
      width="360px"
    >
      <p>
        {{ $t('deleteRepoConfirmMsg1') }}
      </p>
      <p>
        {{ $t('deleteRepoConfirmMsg2') }}
        <span style="font-weight: bold; color: var(--el-color-danger)">{{ repoName }}</span>
        {{ $t('deleteRepoConfirmMsg3') }}
      </p>
      <el-input
        v-model="deleteConfirmStr"
        style="width: 100%"
      />
      <template #footer>
        <span class="dialog-footer">
          <el-button
            size="medium"
            @click="deleteDialog.visible = false"
          >{{ $t('cancel') }}</el-button>
          <el-button
            size="medium"
            :disabled="deleteConfirmStr !== repoName"
            type="danger"
            @click="doDeleteRepo"
          >{{ $t('delete') }}</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue';
import AdminMember from '../components/AdminMember.vue';
import AdminDoc from '../components/AdminDoc.vue';
import { useI18n } from 'vue-i18n';
import globalContext from '../context';
import { changeRepoTypeAPI, checkOwnerAPI, deleteRepoAPI, loadManageRepoAPI } from '../api/modules/repo';
import { checkSuperAdminAPI } from '../api/modules/user';
import { setTitle } from '../utils/controller';
import message from '../utils/message';

const { t } = useI18n();

const repoType = ref('');
const repoTypeOptions = ref([
  {
    id: 'public',
    name: t('publicRepo'),
  },
  {
    id: 'private',
    name: t('privateRepo'),
  },
]);
const changeRepoType = (value) => {
  if (!value) {
    return;
  }
  changeRepoTypeAPI(curRepoID.value, value).then(() => {
    loadRepo();
  });
};
const repoName = computed(() => {
  for (const i in repos.value) {
    if (repos.value[i].id === curRepoID.value) {
      repoType.value = repos.value[i].r_type;
      return repos.value[i].name;
    }
  }
  repoType.value = '';
  return '';
});
const curComponent = computed(() => {
  switch (activeIndex.value) {
    case 'doc':
      return AdminDoc;
    case 'member':
      return AdminMember;
    default:
      return AdminMember;
  }
});
const curRepoID = ref('');
const repos = ref([]);
const options = computed(() => repos.value.map(item => ({
  value: item.id,
  label: item.name,
})));
const loadRepo = () => {
  loadManageRepoAPI().then((res) => {
    repos.value = res.data;
    if (repos.value.length > 0 && !curRepoID.value) {
      curRepoID.value = repos.value[0].id;
    }
  });
};
onMounted(loadRepo);

const activeIndex = ref('member');
const changeActiveIndex = (index) => {
  activeIndex.value = index;
};

const isOwner = ref(false);
const checkOwner = () => {
  checkOwnerAPI(curRepoID.value).then((res) => {
    isOwner.value = res.data;
  });
};
watch(() => curRepoID.value, () => {
  checkOwner();
});

const isSuperAdmin = ref(false);
const checkSuperAdmin = () => {
  checkSuperAdminAPI().then((res) => {
    isSuperAdmin.value = res.data;
  });
};
onMounted(checkSuperAdmin);
const goToBackend = () => {
  window.open(`${globalContext.backEndUrl}/admin/`);
};

const deleteDialog = ref({
  visible: false,
});
const deleteConfirmStr = ref('');
const showDeleteConfirm = () => {
  deleteDialog.value.visible = true;
};

const doDeleteRepo = () => {
  deleteRepoAPI(curRepoID.value).then(
    () => window.location.reload(),
    err => message(err.data.msg, 'error'),
  );
};

onMounted(() => {
  setTitle(t('AdminTab'));
});
</script>

<style scoped>
    @import "../assets/Admin.css";
</style>
