<template>
    <div class="chart-box" v-loading="loading">
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
    import { onMounted, ref } from 'vue'
    import http from '../api'

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

    const loading = ref(true)

    const initXY = (data) => {
        for (const item in data) {
            options.value.xAxis.data.push(item)
            options.value.series[0].data.push(data[item])
        }
    }
    const initChart = (data) => {
        initXY(data)
        const myChart = echarts.init(document.getElementById('doc-publish-chart-main'), null, { renderer: 'svg' })
        myChart.setOption(options.value)
        loading.value = false
    }
    const options = ref({
        title: {
            text: '文章发布统计',
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
                areaStyle: {
                    color: '#79bbff',
                    opacity: 0.6
                },
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

    const loadData = () => {
        http.get(
            '/doc/public/recent_chart/'
        ).then(res => {
            initChart(res.data)
        })
    }

    onMounted(loadData)
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