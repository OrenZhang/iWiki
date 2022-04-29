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
  <div class="mobile-doc-container">
    <el-skeleton
      :rows="6"
      animated
      v-if="loading"
    />
    <ErrorPage
      :error="errorCode"
      v-if="!loading && errorCode !== 0"
    />
    <DocInfoBox
      v-else
      :doc-data="docData"
      :loading="loading"
    />
    <DocComment :doc-id="docID" />
  </div>
</template>

<script setup>
import DocInfoBox from '../components/DocInfoBox.vue';
import DocComment from '../components/DocComment.vue';
import ErrorPage from '../components/ErrorPage.vue';
import { computed, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import message from '../utils/message';
import globalContext from '../context';
import { getDocCommonAPI } from '../api/modules/doc';
import { setTitle } from '../utils/controller';

onMounted(() => {
  if (window.innerWidth >= 1000 && window.innerHeight >= 600) {
    window.location.replace(`${globalContext.siteUrl}doc/${docID.value}`);
  }
});

const loading = ref(true);
const setLoading = (status) => {
  if (status) {
    loading.value = true;
  } else {
    setTimeout(() => {
      loading.value = false;
    }, 600);
  }
};

const permissionDenied = ref(false);
const error404 = ref(false);
const errorCode = computed(() => {
  if (error404.value) {
    return 404;
  } if (permissionDenied.value) {
    return 403;
  }
  return 0;
});

const docData = ref({
  id: '',
  title: '',
  creator_name: '',
  update_at: '',
  content: '',
  creator: '',
  repo_name: '',
  attachments: {},
});
const loadDoc = () => {
  setLoading(true);
  getDocCommonAPI(docID.value).then((res) => {
    if (res.result) {
      docData.value = res.data;
      setTitle(docData.value.title);
    }
  }, (err) => {
    message(err.data.msg, 'error');
    if (err.status === 403) {
      permissionDenied.value = true;
    } else if (err.status === 404) {
      error404.value = true;
    }
  })
    .finally(() => {
      setLoading(false);
    });
};
onMounted(loadDoc);

const route = useRoute();
const docID = ref(route.params.id);
</script>

<style scoped>
    .mobile-doc-container {
        padding: 20px;
        box-sizing: border-box;
    }
</style>
