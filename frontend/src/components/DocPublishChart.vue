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
    class="chart-box"
    v-if="showChart"
    v-loading="loading"
  >
    <div id="doc-publish-chart-main" />
  </div>
</template>

<script setup>
import * as echarts from 'echarts/core';
import { LineChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  DatasetComponent,
  TransformComponent,
} from 'echarts/components';
import { LabelLayout, UniversalTransition } from 'echarts/features';
import { SVGRenderer } from 'echarts/renderers';
import { onMounted, ref, markRaw } from 'vue';
import { useI18n } from 'vue-i18n';
import { loadDocChartDataAPI } from '../api/modules/doc';

echarts.use([
  TitleComponent,
  TooltipComponent,
  GridComponent,
  DatasetComponent,
  TransformComponent,
  LineChart,
  LabelLayout,
  UniversalTransition,
  SVGRenderer,
]);

const { t } = useI18n();

const loading = ref(true);

const initXY = (data) => {
  for (const item in data) {
    options.value.xAxis.data.push(item);
    options.value.series[0].data.push(data[item]);
  }
};
const myChart = ref(null);
const initChart = (data) => {
  initXY(data);
  myChart.value = markRaw(echarts.init(document.getElementById('doc-publish-chart-main'), null, { renderer: 'svg' }));
  myChart.value.setOption(options.value);
  loading.value = false;
};
const options = ref({
  title: {
    text: t('docPublishStatistic'),
    textStyle: {
      color: '#606266',
    },
    left: 'center',
  },
  xAxis: {
    data: [],
  },
  yAxis: {},
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow',
      label: {
        show: true,
        precision: 0,
      },
      axis: 'x',
    },
    backgroundColor: 'rgba(255, 255, 255, 0.8)',
  },
  series: [
    {
      data: [],
      type: 'line',
      smooth: 0.2,
      lineStyle: {
        color: '#409eff',
        type: 'inherit',
      },
      showSymbol: false,
      label: {
        show: false,
        position: 'top',
        color: '#909399',
        fontSize: 16,
      },
    },
  ],
});

const showChart = ref(true);
const loadData = () => {
  loadDocChartDataAPI().then((res) => {
    initChart(res.data);
    if (Object.keys(res.data).length <= 1) {
      showChart.value = false;
    }
  });
};

onMounted(loadData);
</script>

<style scoped>
.chart-box {
    border-radius: 5px;
    box-shadow: var(--el-box-shadow-light);
    margin-bottom: 20px;
    box-sizing: border-box;
    padding: 20px 0 0 0;
}

#doc-publish-chart-main {
    height: 360px;
    width: 100%;
}
</style>
