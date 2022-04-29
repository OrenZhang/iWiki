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
  <el-card class="catalogue-box">
    <div class="title">
      {{ $t('docCatalogue') }}
    </div>
    <ul v-if="titles.length > 0">
      <template
        v-for="anchor in titles"
        :key="anchor"
      >
        <li
          v-if="anchor.indent <= 2"
          :style="{ padding: `0 0 10px ${anchor.indent * 20}px` }"
          @click="doScroll(anchor)"
        >
          <a style="cursor: pointer">{{ anchor.title }}</a>
        </li>
      </template>
    </ul>
    <div
      v-else
      style="text-align: center; margin-top: 20px; color: var(--el-text-color-secondary)"
    >
      {{ $t('noMoreCat') }}
    </div>
  </el-card>
</template>

<script setup>
defineProps({
  titles: {
    type: Array,
    default: () => [],
  },
});

const emits = defineEmits(['doScroll']);

const doScroll = (anchor) => {
  const { lineIndex } = anchor;
  const top = document.querySelector(`[data-v-md-line="${lineIndex}"]`).offsetTop;
  emits('doScroll', top);
};
</script>

<style scoped>
    .catalogue-box {
        margin-top: 20px;
        border-radius: 5px;
        overflow: hidden;
        font-size: 14px;
    }

    .title {
        color: var(--el-color-primary);
        font-size: 14px;
        text-align: center;
        padding-bottom: 9px;
        border-bottom: 2px solid var(--el-border-color-light);
    }
</style>
