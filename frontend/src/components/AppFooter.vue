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
  <div
    class="footer-box"
    v-if="footerInfo.showFooter"
  >
    <div>
      {{ $t('continuousRunning') }} - {{ continuousRunningTime }}
    </div>
    <div v-if="ip && ipInfoStr">
      {{ $t('currentIpAddress') }} - {{ ipInfoStr }} ({{ ip }})
    </div>
    <div v-else-if="ip">
      {{ $t('currentIpAddress') }} - {{ ip }}
    </div>
    <div>
      Copyright <i class="fa-regular fa-copyright" />{{ startYear }} - {{ currentYear }} {{ footerInfo.copyright }}.
      All Rights Reserved.
    </div>
  </div>
</template>

<script setup>
import { onUnmounted, computed, ref } from 'vue';
import { useStore } from 'vuex';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

// VueX
const store = useStore();
const footerInfo = computed(() => store.state.footerInfo);

// 初始化时间
const startDateTime = computed(() => {
  if (footerInfo.value.siteStartup) {
    return new Date(footerInfo.value.siteStartup.replace(/-/g, '/'));
  }
  return new Date();
});
const startYear = computed(() => startDateTime.value.getFullYear());
const now = ref(new Date());
const currentYear = computed(() => now.value.getFullYear());
const day = ref(0);
const hour = ref(0);
const minute = ref(0);
const second = ref(0);
const continuousRunningTime = computed(() => day.value + t('daySimple') + hour.value + t('hourSimple') + minute.value + t('minuteSimple') + second.value + t('secondSimple'));

// 计算时间差
const calculateTime = () => {
  now.value = new Date();
  // 两时间戳差值
  const dateDiff = now.value.getTime() - startDateTime.value.getTime();
  let leftDiff;
  // 计算天数
  day.value = Math.floor(dateDiff / (24 * 3600 * 1000));
  // 计算小时数
  leftDiff = dateDiff % (24 * 3600 * 1000);
  hour.value = Math.floor(leftDiff / (3600 * 1000));
  // 计算分钟数
  leftDiff = leftDiff % (3600 * 1000);
  minute.value = Math.floor(leftDiff / (60 * 1000));
  // 计算秒数
  leftDiff = leftDiff % (60 * 1000);
  second.value = Math.round(leftDiff / 1000);
};

// 定时器
const startUpTimer = setInterval(calculateTime, 1000);
onUnmounted(() => {
  clearInterval(startUpTimer);
});

const ip = ref('');
const ipInfo = ref({
  nation: '',
  province: '',
  city: '',
});
const ipInfoStr = computed(() => {
  let info = '';
  if (ipInfo.value.nation) {
    info += ipInfo.value.nation;
    if (ipInfo.value.province) {
      info = `${info}/${ipInfo.value.province}`;
      if (ipInfo.value.city) {
        info = `${info}/${ipInfo.value.city}`;
      }
    }
  }
  return info;
});
</script>

<style scoped>
    .footer-box {
        display: flex;
        line-height: 24px;
        justify-content: center;
        flex-direction: column;
        align-items: center;
        border-top: 1px solid var(--el-border-color-light);
        font-size: 12px;
        color: var(--el-text-color-secondary);
        padding-bottom: 20px;
    }

    .footer-box > div:nth-of-type(1) {
        margin-top: 20px;
    }
</style>

