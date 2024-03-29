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
  <el-card class="active-user">
    <div class="title">
      {{ $t('activeUser') }}
    </div>
    <el-table
      :data="activeUsers"
      :show-header="false"
    >
      <el-table-column
        width="40px"
        class-name="avatar-column"
      >
        <template #default="scope">
          <el-avatar
            v-if="scope.row.avatar !== '' && scope.row.avatar !== null"
            :src="scope.row.avatar"
          />
          <el-avatar v-else>
            <i class="fa-solid fa-user" />
          </el-avatar>
        </template>
      </el-table-column>
      <el-table-column prop="username">
        <template #default="scope">
          <el-link
            target="_blank"
            :href="globalContext.siteUrl + 'user/' + scope.row.username"
            :underline="false"
          >
            {{ scope.row.username }}
          </el-link>
        </template>
      </el-table-column>
      <el-table-column
        width="60px"
        align="right"
      >
        <template #default="scope">
          <el-tag
            size="mini"
            effect="plain"
          >
            {{ dealWithFloat(scope.row.active_index) }}
          </el-tag>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script setup>
import globalContext from '../context';
import { onMounted, ref } from 'vue';
import { loadActiveUserAPI } from '../api/modules/user';

const activeUsers = ref([]);
const loadActiveUser = () => {
  loadActiveUserAPI().then((res) => {
    activeUsers.value = res.data;
  });
};
onMounted(loadActiveUser);

const dealWithFloat = (num) => {
  const numArray = num.toString().split('.');
  if (numArray.length > 1) if (num < 10) {
    return num.toFixed(2);
  } else {
    return num.toFixed(1);
  }
  // 整数输出

  return num;
};
</script>

<style scoped>
    .title {
        color: var(--el-color-primary);
        font-size: 14px;
        text-align: center;
        padding-bottom: 9px;
        border-bottom: 2px solid var(--el-border-color-light);
    }

    .active-user {
        margin-top: 20px;
    }

    .active-user .fa-user {
        font-size: 16px;
        margin-top: 0;
    }

    .active-user :deep(.cell) {
        line-height: unset;
        font-size: 14px;
    }

    .el-avatar {
        background: var(--el-color-primary-light-7);
        box-sizing: border-box;
    }

    .el-avatar .fa-user {
        color: var(--el-color-white);
    }

    :deep(.avatar-column) .cell {
        padding: 0 10px 0 0;
    }
</style>
