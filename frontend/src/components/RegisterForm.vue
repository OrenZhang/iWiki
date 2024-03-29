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
    <el-form-item :label="$t('Username')">
      <el-input
        v-model="signData.username"
        :placeholder="$t('characters4to24')"
        :minlength="4"
        :maxlength="24"
        :disabled="loading"
      >
        <template #prefix>
          <i
            class="fa-solid fa-user h-center"
            style="margin-left: 6px;"
          />
        </template>
      </el-input>
      <div
        style="color: var(--el-color-danger); margin-bottom: -10px; height: 32px; margin-top: -10px;"
        v-if="!usernameValid"
      >
        {{ $t('DuplicateUserName') }}
      </div>
      <div
        style="color: var(--el-color-danger); margin-bottom: -10px; height: 32px; margin-top: -10px;"
        v-if="!usernameLengthValid"
      >
        {{ $t('UserNameTooShort') }}
      </div>
    </el-form-item>
    <el-form-item :label="$t('Password')">
      <el-input
        v-model="signData.password"
        :placeholder="$t('within24c')"
        type="password"
        show-password
        :maxlength="24"
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
    <el-form-item :label="$t('Telephone')">
      <el-input
        v-model="signData.phone"
        :minlength="11"
        :maxlength="11"
        show-word-limit
        :disabled="loading"
      >
        <template #prefix>
          <i
            class="fa-solid fa-phone-alt h-center"
            style="margin-left: 6px;"
          />
        </template>
      </el-input>
    </el-form-item>
    <el-form-item
      :label="$t('VerificationCode')"
      class="oneline-code-button-box"
    >
      <el-input
        v-model="signData.code"
        :minlength="6"
        :maxlength="6"
        show-word-limit
        :disabled="loading"
      >
        <template #prefix>
          <i
            class="fa-solid fa-shield h-center"
            style="margin-left: 6px;"
          />
        </template>
      </el-input>
      <el-button
        style="padding: 12px;"
        :disabled="signData.phone.length !== 11 || codeSend || loading"
        @click="sendVerifyCode"
      >
        {{ $t('send') }}{{ showLastTime }}
      </el-button>
    </el-form-item>
    <el-button
      style="width: 100%"
      type="primary"
      :disabled="!checkForm"
      :loading="loading"
      @click="doRegister"
    >
      {{ $t('signup') }}
    </el-button>
  </el-form>
</template>

<script setup>
import { computed, ref, watch } from 'vue';
import message from '../utils/message';
import { useStore } from 'vuex';
import { useI18n } from 'vue-i18n';
import { checkUserNameAPI, signUpAPI } from '../api/modules/user';
import { sendRegistryCodeAPI } from '../api/modules/common';

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
const signData = ref({
  username: '',
  password: '',
  code: '',
  phone: '',
});

// 用户名
const usernameValid = ref(true);
const usernameLengthValid = computed(() => {
  if (signData.value.username !== '') {
    return signData.value.username.length >= 4;
  }
  return true;
});
const checkUsername = () => {
  checkUserNameAPI(signData.value.username).then(() => {
    usernameValid.value = true;
  }, () => {
    usernameValid.value = false;
  });
};
watch(() => signData.value.username, (newVal) => {
  if (newVal) {
    checkUsername();
  } else {
    usernameValid.value = true;
  }
});

// 校验
const checkForm = computed(() => {
  if (!usernameValid.value) {
    return false;
  }
  for (const key in signData.value) {
    if (signData.value[key] === '') {
      return false;
    }
  }
  if (signData.value.username.length < 4 || signData.value.username.length > 24) {
    return false;
  }
  if (signData.value.password.length < 1 || signData.value.password.length > 24) {
    return false;
  }
  return signData.value.phone.length === 11 && signData.value.code.length === 6;
});

// 验证码
const codeSend = ref(false);
const lastTime = ref(60);
const showLastTime = computed(() => {
  if (codeSend.value) {
    return `(${lastTime.value})`;
  }
  return '';
});
const codeReSend = () => {
  setTimeout(() => {
    if (lastTime.value > 0) {
      lastTime.value -= 1;
      codeReSend();
    } else {
      codeSend.value = false;
    }
  }, 1000);
};
const sendVerifyCode = () => {
  codeSend.value = true;
  sendRegistryCodeAPI(signData.value.phone).then((res) => {
    if (res.result) {
      message(t('sendCodeSuccess'));
    }
  }, (err) => {
    message(err.data.msg, 'error');
  })
    .finally(() => {
      lastTime.value = 60;
      codeReSend();
    });
};

// 注册
const doRegister = () => {
  setLoading(true);
  signUpAPI(signData.value).then((res) => {
    if (res.result) {
      store.commit('setLogin', false);
      store.dispatch('getUserInfo');
      message(t('RegistrySuccess'));
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
    @import "../assets/RegisterForm.css";
</style>
