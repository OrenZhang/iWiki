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
  <div class="h-100">
    <ErrorPage
      :error="errorCode"
      :apply-info="appleInfo"
      v-if="!loading && errorCode !== 0"
    />
    <el-scrollbar
      always
      ref="scroll"
      v-if="errorCode === 0"
    >
      <el-container
        id="doc-container"
        class="doc-container h-100"
      >
        <el-main style="overflow: unset;">
          <el-skeleton
            :rows="6"
            animated
            v-if="loading"
          />
          <DocInfoBox
            @load-title="loadTitle"
            :doc-data="docData"
            :loading="loading"
          />
          <el-divider />
          <DocComment :doc-id="docID" />
        </el-main>
        <el-aside style="overflow: unset;">
          <DocSidebar />
          <DocCatalogue
            @do-scroll="doScroll"
            :titles="titles"
          />
        </el-aside>
      </el-container>
    </el-scrollbar>
  </div>
</template>

<script setup>
import ErrorPage from '../components/ErrorPage.vue';
import DocInfoBox from '../components/DocInfoBox.vue';
import DocComment from '../components/DocComment.vue';
import DocSidebar from '../components/DocSidebar.vue';
import { useRoute } from 'vue-router';
import { computed, onMounted, ref, watch } from 'vue';
import message from '../utils/message';
import DocCatalogue from '../components/DocCatalogue.vue';
import globalContext from '../context';
import { getDocCommonAPI } from '../api/modules/doc';
import { setTitle } from '../utils/controller';

const appleInfo = ref({
  visible: true,
  doc_id: computed(() => docID.value),
});

onMounted(() => {
  if (window.innerWidth < 1000 || window.innerHeight < 600) {
    window.location.replace(`${globalContext.siteUrl}m/doc/${docID.value}`);
  }
});

const titles = ref([]);
const loadTitle = (value) => {
  titles.value = value;
};

// 加载状态
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

// 文章
const docID = ref('');
const docData = ref({
  id: '',
  title: '',
  creator_name: '',
  update_at: '',
  content: '',
  creator: '',
  repo_name: '',
  attachments: {},
  repo_id: '',
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

// 异常
const error404 = ref(false);
const permissionDenied = ref(false);
const errorCode = computed(() => {
  if (error404.value) {
    return 404;
  } if (permissionDenied.value) {
    return 403;
  }
  return 0;
});

// router
const route = useRoute();
docID.value = route.params.id;
watch(() => route.params.id, (id) => {
  docID.value = id;
  if (docID.value !== undefined) {
    loadDoc();
  }
});

const scroll = ref(null);
const doScroll = (top) => {
  scroll.value.setScrollTop(top);
};
</script>

<style scoped>
    @import "../assets/Doc.css";
</style>
