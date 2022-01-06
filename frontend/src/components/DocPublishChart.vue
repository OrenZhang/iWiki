<template>
    <div class="chart-box" v-if="showChart" v-loading="loading">
        <div id="doc-publish-chart-main" />
    </div>
</template>

<script setup>
    import * as echarts from 'echarts/core'
    import { LineChart } from 'echarts/charts'
    import {
        TitleComponent,
        TooltipComponent,
        GridComponent,
        DatasetComponent,
        TransformComponent
    } from 'echarts/components'
    import { LabelLayout, UniversalTransition } from 'echarts/features'
    import { SVGRenderer } from 'echarts/renderers'
    import { onMounted, ref, markRaw } from 'vue'
    import http from '../api'
    import { useI18n } from 'vue-i18n'

    echarts.use([
        TitleComponent,
        TooltipComponent,
        GridComponent,
        DatasetComponent,
        TransformComponent,
        LineChart,
        LabelLayout,
        UniversalTransition,
        SVGRenderer
    ])
    
    const { t } = useI18n()

    const loading = ref(true)

    const initXY = (data) => {
        for (const item in data) {
            options.value.xAxis.data.push(item)
            options.value.series[0].data.push(data[item])
        }
    }
    const myChart = ref(null)
    const initChart = (data) => {
        initXY(data)
        myChart.value = markRaw(echarts.init(document.getElementById('doc-publish-chart-main'), null, { renderer: 'svg' }))
        myChart.value.setOption(options.value)
        loading.value = false
    }
    const options = ref({
        title: {
            text: t('docPublishStatistic'),
            textStyle: {
                color: '#606266'
            },
            left: 'center'
        },
        xAxis: {
            data: []
        },
        yAxis: {},
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow',
                label: {
                    show: true,
                    precision: 0
                },
                axis: 'x'
            },
            backgroundColor: 'rgba(255, 255, 255, 0.8)'
        },
        series: [
            {
                data: [],
                type: 'line',
                smooth: 0.2,
                lineStyle: {
                    color: '#409eff',
                    type: 'inherit'
                },
                showSymbol: false,
                label: {
                    show: false,
                    position: 'top',
                    color: '#909399',
                    fontSize: 16
                }
            }
        ]
    })

    const showChart = ref(true)
    const loadData = () => {
        http.get(
            '/doc/public/recent_chart/'
        ).then(res => {
            initChart(res.data)
            if (Object.keys(res.data).length <= 1) {
                showChart.value = false
            }
        })
    }

    onMounted(loadData)

    onMounted(() => {
        window.addEventListener('resize', () => {
            myChart.value.resize()
        })
    })
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