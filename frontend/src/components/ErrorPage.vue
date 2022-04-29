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
  <div class="h-center v-center h-100">
    <el-empty :description="description">
      <el-button
        type="text"
        @click="router.push({ name: 'Home' })"
      >
        {{ $t('backIndex') }}
      </el-button>
      <el-button
        v-show="applyInfo.visible && user.auth"
        type="text"
        @click="doApply"
      >
        {{ $t('applyForRepo') }}
      </el-button>
      <el-button
        v-show="!user.auth"
        type="text"
        @click="showLogin"
      >
        {{ $t('login') }}
      </el-button>
    </el-empty>
  </div>
</template>


<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';
import message from '../utils/message';
import { useI18n } from 'vue-i18n';
import { applyByDocAPI } from '../api/modules/repo';

const { t } = useI18n();

const store = useStore();
const user = computed(() => store.state.user);

const router = useRouter();

const props = defineProps({
  error: {
    type: Number,
    default: 404,
  },
  errorMessages: {
    type: Object,
    default: () => ({
      403: 'permissionDenied',
      404: 'Error404',
      400001: 'docEditing',
    }),
  },
  applyInfo: {
    type: Object,
    default: () => ({
      visible: false,
      doc_id: null,
    }),
  },
});

const doApply = () => {
  applyByDocAPI(props.applyInfo.doc_id).then(() => {
    message(t('applyForGroupSuccessMsg'));
  }, (err) => {
    message(err.data.msg, 'error');
  });
};

const description = computed(() => {
  if (props.error === 0) {
    return '';
  }
  return t(props.errorMessages[props.error]);
});

const showLogin = (() => {
  store.commit('setLogin', true);
});
</script>

<style scoped>

</style>
