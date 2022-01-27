<template>
    <div class="footer-box" v-if="footerInfo.showFooter">
        <div>
            {{ $t('continuousRunning') }} - {{ continuousRunningTime }}
        </div>
        <div>
            Copyright <i class="fa-regular fa-copyright" /> {{ startYear }} - {{ now.getFullYear() }} {{ footerInfo.copyright }}. All Rights Reserved.
        </div>
    </div>
</template>

<script setup>
    import { onUnmounted, computed, ref } from 'vue'
    import { useStore } from 'vuex'
    import { useI18n } from 'vue-i18n'
    
    const { t } = useI18n()
    
    // VueX
    const store = useStore()
    const footerInfo = computed(() => store.state.footerInfo)

    // 初始化时间
    const startDateTime = new Date(footerInfo.value.siteStartup.replace(/-/g, '/'))
    const now = ref(new Date())
    const startYear = startDateTime.getFullYear()
    const day = ref(0)
    const hour = ref(0)
    const minute = ref(0)
    const second = ref(0)
    const continuousRunningTime = computed(() => {
        return day.value + t('daySimple') + hour.value + t('hourSimple') + minute.value + t('minuteSimple') + second.value + t('secondSimple')
    })

    // 计算时间差
    const calculateTime = () => {
        now.value = new Date()
        // 两时间戳差值
        const dateDiff = now.value.getTime() - startDateTime.getTime()
        let leftDiff
        // 计算天数
        day.value = Math.floor(dateDiff / (24 * 3600 * 1000))
        // 计算小时数
        leftDiff = dateDiff % (24 * 3600 * 1000)
        hour.value = Math.floor(leftDiff / (3600 * 1000))
        // 计算分钟数
        leftDiff = leftDiff % (3600 * 1000)
        minute.value = Math.floor(leftDiff / (60 * 1000))
        // 计算秒数
        leftDiff = leftDiff % (60 * 1000)
        second.value = Math.round(leftDiff / 1000)
    }

    // 定时器
    const startUpTimer = setInterval(calculateTime, 1000)
    onUnmounted(() => {
        clearInterval(startUpTimer)
    })
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

