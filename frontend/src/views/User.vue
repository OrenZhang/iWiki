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
  <div class="h-100 user-view">
    <el-scrollbar always>
      <div class="head-box" />
      <HUserInfoBox
        :show-logout="false"
        :user-info="searchUserInfo"
      />
      <div class="doc-list">
        <el-skeleton
          :rows="6"
          animated
          v-show="docLoading"
        />
        <DocList
          :data="docData"
          @page-change="handlePageChange"
          v-show="!docLoading"
        />
      </div>
    </el-scrollbar>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import message from '../utils/message';
import DocList from '../components/DocList.vue';
import HUserInfoBox from '../components/HUserInfoBox.vue';
import { getExactUserInfoAPI } from '../api/modules/user';
import { loadUserDocPublicAPI } from '../api/modules/doc';
import { setTitle } from '../utils/controller';

const roure = useRoute();

const searchUser = ref('');
const searchUserInfo = ref({
  uid: '',
  username: '',
  avatar: '',
  date_joined: '',
  property: {
    repo_count: 0,
    doc_count: 0,
    comment_count: 0,
    active_index: 0,
  },
});
const loadUser = () => {
  getExactUserInfoAPI(searchUser.value).then((res) => {
    searchUserInfo.value = res.data;
    setTitle(searchUserInfo.value.username);
  }, (err) => {
    message(err.data.msg, 'error');
  });
};

const docData = ref({
  usePaginator: true,
  paginator: {
    page: 1,
    count: 0,
  },
  data: [],
});
const handlePageChange = (page) => {
  docData.value.paginator.page = page;
  loadUserDoc();
};
const docLoading = ref(true);
const loadUserDoc = () => {
  docLoading.value = true;
  loadUserDocPublicAPI(searchUser.value, docData.value.paginator.page).then((res) => {
    docData.value.data = res.data.results;
    docData.value.paginator.count = res.data.count;
  }, (err) => {
    message(err.data.msg, 'error');
  })
    .finally(() => {
      setTimeout(() => {
        docLoading.value = false;
      }, 600);
    });
};

const loadData = () => {
  searchUser.value = roure.params.username;
  loadUser();
  loadUserDoc();
};
onMounted(loadData);
watch(() => roure.params.username, (newVal, oldVal) => {
  if (newVal !== oldVal && newVal) {
    loadData();
  }
});
</script>

<style scoped>
    @import "../assets/User.css";
</style>
