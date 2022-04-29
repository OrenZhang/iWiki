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
  <div class="user-info-box">
    <div>
      <el-upload
        :action="avatarUrl"
        :with-credentials="true"
        :show-file-list="false"
        :disabled="avatarDisabled"
        :on-success="handleAvatarSuccess"
        :before-upload="beforeAvatarUpload"
      >
        <el-avatar
          v-if="userInfo.avatar !== null && userInfo.avatar!== ''"
          :src="userInfo.avatar"
          :size="100"
        />
        <el-avatar
          v-else-if="user.uid === userInfo.uid && user.auth"
          :size="100"
        >
          <i class="fa-solid fa-plus" />
        </el-avatar>
        <el-avatar
          v-else
          :size="100"
        >
          <i class="fa-solid fa-user" />
        </el-avatar>
      </el-upload>
      <div class="user-info-text">
        <h2>
          {{ userInfo.username }}
        </h2>
        <p>{{ $t('registryAt') }}:&nbsp;{{ userInfo.date_joined }}</p>
      </div>
    </div>
    <div style="display: flex">
      <div class="user-statistic-single">
        <h4>{{ $t('memberRepos') }}</h4>
        <p>{{ userInfo.property.repo_count }}</p>
      </div>
      <div class="user-statistic-single">
        <h4>{{ $t('releaseDocs') }}</h4>
        <p>{{ userInfo.property.doc_count }}</p>
      </div>
      <div class="user-statistic-single">
        <h4>{{ $t('commentCount') }}</h4>
        <p>{{ userInfo.property.comment_count }}</p>
      </div>
      <div class="user-statistic-single">
        <h4>{{ $t('activeIndex') }}</h4>
        <p>{{ transIndex(userInfo.property.active_index) }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useStore } from 'vuex';
import message from '../utils/message';
import { computed, defineProps } from 'vue';
import globalContext from '../context';
import { useI18n } from 'vue-i18n';

const store = useStore();
const user = computed(() => store.state.user);

const { t } = useI18n();

const props = defineProps({
  userInfo: {
    type: Object,
    default: () => ({
      uid: '',
    }),
  },
});

const avatarDisabled = computed(() => user.value.uid !== props.userInfo.uid || !user.value.auth);
const transIndex = (num) => {
  if (!num) {
    return 0;
  }
  const numArray = num.toString().split('.');
  if (numArray.length > 1) if (num < 10) {
    return num.toFixed(2);
  } else {
    return num.toFixed(1);
  }
  // 整数输出

  return num;
};

const avatarUrl = computed(() => `${globalContext.backEndUrl}/cos/upload_avatar/`);
const handleAvatarSuccess = () => {
  store.dispatch('getUserInfo');
};
const beforeAvatarUpload = (file) => {
  const isPic = file.type === 'image/jpeg' || file.type === 'image/png';
  const isLt1M = file.size / 1024 / 1024 < 1;
  if (!isPic) {
    message(t('useJPGorPNG'), 'error');
  }
  if (!isLt1M) {
    message(t('upto1M'), 'error');
  }
  return isPic && isLt1M;
};
</script>

<style scoped>
    .user-info-box {
        max-width: 1440px;
        margin: -92px auto 0;
        padding: 40px;
        box-sizing: border-box;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .user-info-box .el-avatar {
        background: var(--el-color-white);
        box-shadow: var(--el-box-shadow-light);
    }

    .user-info-box i {
        font-size: 48px;
        margin-top: 24px;
        color: var(--el-color-primary-light-4);
    }

    .user-info-text {
        margin-left: 20px;
        color: var(--el-color-white);
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .user-info-text h2 {
        margin-top: 0;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
    }

    .user-info-text p {
        margin: 0;
        font-size: 14px;
        color: var(--el-text-color-regular);
    }

    .user-info-box > div {
        display: flex;
    }

    .user-statistic-single {
        display: flex;
        flex-direction: column;
        align-items: center;
        box-shadow: var(--el-box-shadow-light);
        background: var(--el-color-white);
        border-radius: 5px;
        margin-left: 10px;
        box-sizing: border-box;
        padding: 10px;
        width: 92px;
    }

    .user-statistic-single h4 {
        margin: 0;
    }

    .user-statistic-single p {
        margin: 20px 0 0 0;
        color: var(--el-color-primary);
    }

    .edit-info {
        margin-left: 10px;
        background: var(--u-bg-color-login);
        border: none;
        cursor: pointer;
    }

    .user-info-box .fa-plus {
        font-size: 36px;
        margin-top: 32px;
    }
</style>
