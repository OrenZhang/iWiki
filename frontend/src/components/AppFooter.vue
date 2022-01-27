<template>
    <div class="footerbox" v-if="state.footerInfo.showFooter">
        <div>{{ i18n.global.messages[i18n.global.locale].countinuousRunning }} {{ state.renderTime }}</div>
        <div>Copyright  {{ state.footerInfo.siteStartup.split('-')[0] }} - {{ new Date().getFullYear() }} {{ state.footerInfo.copyright }}. All Rights Reserved. </div>
    </div>
</template>

<script setup>
    import i18n from '../locale/index.js'
    import { reactive, onUnmounted } from 'vue'
    import { useStore } from 'vuex'
    
    let store = useStore()
    let state = reactive({
        footerInfo: store.state.footerInfo,
        renderTime: ''
    })

    // 计算 距离指定时间差值
    const calculateTime = function (siteStartup,format) {
        //当前日期
        let nowDate = new Date()
        //开始时间日期格式化后
        let startDateTime = new Date(siteStartup.replace(/-/g, '/'))
        //两时间戳差值
        let diff = (nowDate - startDateTime)
        let days = Math.floor(diff / (24 * 3600 * 1000)) < 10 ? '0' +  Math.floor(diff / (24 * 3600 * 1000)) : Math.floor(diff / (24 * 3600 * 1000)) // 计算出天数
        let leavel1 = diff % (24 * 3600 * 1000)// 计算天数后剩余的时间
        let hours = Math.floor(leavel1 / (3600 * 1000)) < 10 ? '0' + Math.floor(leavel1 / (3600 * 1000)):Math.floor(leavel1 / (3600 * 1000)) // 计算天数后剩余的小时数
        let leavel2 = diff % (3600 * 1000) // 计算剩余小时后剩余的毫秒数
        let minutes = Math.floor(leavel2 / (60 * 1000)) < 10 ? '0' + Math.floor(leavel2 / (60 * 1000)) : Math.floor(leavel2 / (60 * 1000)) // 计算剩余的分钟数
        let leavel3 = diff %(60 * 1000) // 计算剩余的秒数
        let second = Math.floor(leavel3 / 1000) < 10 ? '0' + Math.floor(leavel3 / 1000) : Math.floor(leavel3 / 1000) //计算秒数
        return `${days}${format[0]} ${hours}${format[1]} ${minutes}${format[2]} ${second}${format[3]}`
    }
    
    let timer = setInterval((params) => {
        state.renderTime = calculateTime(state.footerInfo.siteStartup, i18n.global.locale === 'en' ? ['d','h','m','s']:['天','小时','分钟','秒'])
    }, 1000)
            
    onUnmounted(() => {
        // 清除定时器
        clearInterval(timer)
    })
</script>

<style scoped>
    .footerbox {
        display: flex;
        height: 50px;
        justify-content: center;
        flex-direction: column;
        align-items: center;
        border-top: 1px solid #dcdee5;
        font-size: 12px;
        color: #63656e;
    }
</style>

