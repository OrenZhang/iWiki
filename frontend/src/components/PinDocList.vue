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
  <div>
    <el-card
      v-for="item in docs"
      :key="item.id"
      class="single-doc-box"
    >
      <div class="title-box">
        <el-tag
          size="mini"
          type="danger"
          effect="dark"
        >
          {{ $t('pinDoc') }}
        </el-tag>
        <el-link
          target="_blank"
          :href="globalContext.siteUrl + 'doc/' + item.id"
        >
          <h4>{{ item.title }}</h4>
        </el-link>
      </div>
      <div class="author-box">
        <div>
          <el-tag
            v-if="item.available === 'public'"
            size="mini"
          >
            {{ $t('public') }}
          </el-tag>
          <el-tag
            v-else
            size="mini"
            type="warning"
          >
            {{ $t('private') }}
          </el-tag>
        </div>
        <i
          class="fa-solid fa-cube ml-10 mr-2"
          v-if="item.repo_name"
        />
        <el-link
          :underline="false"
          :href="globalContext.siteUrl + 'repo/' + item.repo_id"
          target="_blank"
          v-if="item.repo_name"
        >
          {{ item.repo_name }}
        </el-link>
        <i
          class="fa-regular fa-user ml-10 mr-2"
          v-if="item.creator_name"
        />
        <el-link
          :underline="false"
          :href="globalContext.siteUrl + 'user/' + item.creator_name"
          target="_blank"
          v-if="item.creator_name"
        >
          {{ item.creator_name }}
        </el-link>
        <i class="fa-regular fa-clock ml-10 mr-2" />
        <el-link :underline="false">
          {{ item.update_at }}
        </el-link>
      </div>
    </el-card>
    <el-divider v-if="docs.length > 0" />
  </div>
</template>

<script setup>
import globalContext from '../context';
import { onMounted, ref, watch } from 'vue';
import { loadPinDocAPI } from '../api/modules/doc';

const props = defineProps({
  repoId: {
    type: String,
    default: null,
  },
});

const docs = ref([]);
const loadDocs = () => {
  if (!props.repoId) {
    return;
  }
  loadPinDocAPI(props.repoId).then((res) => {
    docs.value = res.data;
  });
};
onMounted(loadDocs);
watch(() => props.repoId, () => {
  loadDocs();
});
</script>

<style scoped>
    .el-card {
        border: none;
        margin-bottom: 20px;
        border-radius: 5px;
    }

    .el-pagination {
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .single-doc-box h4 {
        margin-top: 0;
        margin-bottom: 0;
        font-size: 16px;
    }

    .single-doc-box > div > .title-box {
        margin-bottom: 10px;
        display: flex;
    }

    .single-doc-box > div > .title-box > .el-tag {
        margin-right: 10px;
    }

    .author-box {
        margin: 0;
        display: flex;
        align-items: center;
        font-size: 14px;
    }

    .ml-10 {
        margin-left: 10px;
    }

    .mr-2 {
        margin-right: 2px;
    }
</style>
