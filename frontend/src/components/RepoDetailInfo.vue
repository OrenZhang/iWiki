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
  <div class="repo-info">
    <div style="display: flex; align-items: center; margin-bottom: 20px; justify-content: space-between;">
      <div style="display: flex; align-items: center;">
        <h2>{{ repo.name }}</h2>
        <el-tag
          size="small"
          v-if="repo.r_type === 'public'"
          style="margin-left: 10px;"
          type="success"
        >
          {{ $t('publicRepo') }}
        </el-tag>
        <el-tag
          size="small"
          v-else
          style="margin-left: 10px;"
          type="warning"
        >
          {{ $t('privateRepo') }}
        </el-tag>
      </div>
      <div>
        <el-link
          v-show="!isMember && repo.is_allow_apply"
          :underline="false"
          @click="showApplyConfirm"
        >
          <el-tag
            size="small"
            style="margin-left: 10px;"
          >
            {{ $t('applyRepo') }}
          </el-tag>
        </el-link>
      </div>
    </div>
    <div class="user-avatars">
      <el-avatar class="head-avatar">
        <el-tooltip
          :content="$t('admin')"
          placement="top"
          effect="light"
        >
          <i class="fa-solid fa-shield" />
        </el-tooltip>
      </el-avatar>
      <div class="users-inline">
        <template
          v-for="member in repo.admins"
          :key="member.uid"
        >
          <el-tooltip
            :content="member.username"
            placement="top"
            effect="light"
          >
            <el-avatar
              @click="goTo('user/' + member.username)"
              :src="member.avatar"
              v-if="member.avatar !== null"
            />
            <el-avatar
              @click="goTo('user/' + member.username)"
              v-else
            >
              {{ member.username[0].toUpperCase() }}
            </el-avatar>
          </el-tooltip>
        </template>
      </div>
    </div>
    <div
      class="user-avatars"
      v-if="repo.members !== undefined && repo.members.length > 0"
    >
      <el-avatar class="head-avatar">
        <el-tooltip
          :content="$t('member')"
          placement="top"
          effect="light"
        >
          <i class="fa-solid fa-users" />
        </el-tooltip>
      </el-avatar>
      <div class="users-inline">
        <template
          v-for="member in repo.members"
          :key="member.uid"
        >
          <el-tooltip
            :content="member.username"
            placement="top"
            effect="light"
          >
            <el-avatar
              @click="goTo('user/' + member.username)"
              :src="member.avatar"
              v-if="member.avatar !== null"
            />
            <el-avatar
              @click="goTo('user/' + member.username)"
              v-else
            >
              {{ member.username[0].toUpperCase() }}
            </el-avatar>
          </el-tooltip>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, defineEmits } from 'vue';
import { ElMessageBox } from 'element-plus';
import message from '../utils/message';
import { useStore } from 'vuex';
import { useI18n } from 'vue-i18n';
import globalContext from '../context';
import { applyForRepoAPI } from '../api/modules/repo';

const { t } = useI18n();

const store = useStore();
const user = computed(() => store.state.user);

defineEmits(['reloadRepoInfo', 'reloadApply', 'handleCurrentChange']);

const props = defineProps({
  repo: {
    type: Object,
    default: () => ({
      name: '',
      admins: [],
      members: [],
      is_allow_apply: true,
    }),
  },
});

const goTo = (url) => {
  window.open(globalContext.siteUrl + url);
};

const isMember = computed(() => {
  for (const i in props.repo.admins) {
    if (props.repo.admins[i].uid === user.value.uid) {
      return true;
    }
  }
  for (const i in props.repo.members) {
    if (props.repo.members[i].uid === user.value.uid) {
      return true;
    }
  }
  return false;
});
const showApplyConfirm = () => {
  const content = t('applyMsg', { name: props.repo.name });
  ElMessageBox.alert(content, t('applyConfirm'), {
    confirmButtonText: t('applyConfirmed'),
    callback: (action) => {
      if (action === 'confirm') {
        applyForRepoAPI(props.repo.id).then(() => {
          message(t('applySuccess'));
        }, (err) => {
          message(err.data.msg, 'error');
        });
      }
    },
  });
};
</script>

<style scoped>
    .repo-info {
        padding: 40px;
        box-sizing: border-box;
        border-radius: 5px;
        background: var(--u-bg-color-login);
        min-height: 300px;
        box-shadow: var(--el-box-shadow-light);
    }

    .user-avatars {
        display: flex;
    }

    .users-inline {
        display: flex;
        flex-wrap: wrap;
        line-height: 50px;
        width: 100%;
    }

    .user-avatars .el-avatar {
        cursor: pointer;
    }

    .head-avatar {
        background: var(--el-color-white);
        cursor: unset!important;
    }

    .el-avatar {
        margin-right: 10px;
        margin-top: 10px;
    }

    .head-avatar .fa-users,
    .head-avatar .fa-shield {
        font-size: 18px;
        margin-top: 12px;
    }

    .admin-dialog h4 {
        margin: 0 0 20px 0;
    }

    :deep(.el-drawer__header) {
        margin-bottom: 10px;
    }
</style>
