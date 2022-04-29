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
  <el-card class="repo-doc-box">
    <el-tabs v-model="activeTab">
      <el-tab-pane
        :label="$t('hotRepo')"
        name="repo"
      >
        <el-table
          :show-header="false"
          :data="hotRepos"
          size="small"
        >
          <el-table-column
            type="index"
            width="40"
          />
          <el-table-column>
            <template #default="scope">
              <el-link
                target="_blank"
                :underline="false"
                :href="globalContext.siteUrl + 'repo/' + scope.row.id"
              >
                {{ scope.row.name }}
              </el-link>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      <el-tab-pane
        :label="$t('hotDoc')"
        name="doc"
      >
        <el-table
          :show-header="false"
          :data="recentDocs"
          size="small"
        >
          <el-table-column
            type="index"
            width="40"
          />
          <el-table-column>
            <template #default="scope">
              <el-link
                target="_blank"
                :underline="false"
                :href="globalContext.siteUrl + 'doc/' + scope.row.id"
              >
                {{ scope.row.title }}
              </el-link>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
  </el-card>
</template>

<script setup>
import globalContext from '../context';
import { onMounted, ref } from 'vue';
import { loadHotRepoAPI, loadRecentDocAPI } from '../api/modules/doc';

const activeTab = ref('repo');

const hotRepos = ref([]);
const loadHotRepo = () => {
  loadHotRepoAPI().then((res) => {
    hotRepos.value = res.data;
  });
};
onMounted(loadHotRepo);

const recentDocs = ref([]);
const loadRecentDoc = () => {
  loadRecentDocAPI().then((res) => {
    recentDocs.value = res.data;
  });
};
onMounted(loadRecentDoc);
</script>

<style scoped>
    .repo-doc-box {
        margin-top: 20px;
        border-radius: 5px;

    }

    .repo-doc-box :deep(.cell),
    .el-link {
        font-size: 14px;
    }

    .repo-doc-box :deep(.el-tabs__nav) {
        justify-content: center;
        display: flex;
        width: 100%;
    }
</style>
