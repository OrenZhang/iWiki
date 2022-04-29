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
  <el-form
    label-position="left"
    label-width="80px"
  >
    <el-form-item :label="$t('uLogin')">
      <el-input
        :placeholder="$t('usernameOrPhone')"
        v-model="loginData.username"
        :minlength="4"
        :maxlength="24"
        type="text"
        clearable
        :disabled="loading"
      >
        <template #prefix>
          <i
            class="fa-solid fa-user h-center"
            style="margin-left: 6px;"
          />
        </template>
      </el-input>
    </el-form-item>
    <el-form-item :label="$t('Password')">
      <el-input
        type="password"
        v-model="loginData.password"
        :maxlength="24"
        clearable
        show-password
        :disabled="loading"
      >
        <template #prefix>
          <i
            class="fa-solid fa-lock h-center"
            style="margin-left: 6px;"
          />
        </template>
      </el-input>
    </el-form-item>
    <div style="display: flex">
      <el-button
        style="width: 100%"
        type="primary"
        :disabled="!checkForm"
        :loading="loading"
        @click="doLogin(true)"
      >
        {{ $t('login2refresh') }}
      </el-button>
    </div>
  </el-form>
</template>

<script setup>
import { computed, ref } from 'vue';
import { useStore } from 'vuex';
import message from '../utils/message';
import { useI18n } from 'vue-i18n';
import { signInAPI } from '../api/modules/user';

const { t } = useI18n();

// 全局
const store = useStore();

// 状态
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

// 数据
const loginData = ref({
  username: '',
  password: '',
});

// 校验
const checkForm = computed(() => loginData.value.username !== '' && loginData.value.password !== '' && loginData.value.username.length >= 4);

// 登录
const doLogin = (refresh = false) => {
  setLoading(true);
  signInAPI(loginData.value).then((res) => {
    if (res.result) {
      message(t('loginSuccess'));
      store.commit('setLogin', false);
      store.dispatch('getUserInfo');
      if (refresh) {
        window.location.reload();
      }
    }
  }, (err) => {
    message(err.data.msg, 'error');
  })
    .finally(() => {
      setLoading(false);
    });
};
</script>

<style scoped>

</style>
