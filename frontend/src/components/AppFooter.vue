<template>
    <div class="footerbox">
        <div>{{ state.countinuousRunning[i18n.global.locale] }} : {{ state.renderTime }}</div>
        <div>Copyright  2021 - {{ new Date().getFullYear() }} Oren Zhang. All Rights Reserved. </div>
    </div>
</template>

<script setup>
    import i18n from '@/locale/index.js'
    import _utils from '@/utils/index.js'
    import { reactive, onUnmounted } from 'vue'
    import { useStore } from 'vuex'
    
    let store = useStore()
    let state = reactive({
        footerInfo: store.state.footerInfo,
        renderTime: '',
        // 国际化
        countinuousRunning:{
            'zh':'本站已运行',
            'en':'Countinuous Running'
        }
    })

    let timer = setInterval((params) => {
        state.renderTime = _utils.calculateTime( state.footerInfo.siteStartup,i18n.global.locale === 'en' ? ['d','h','m','s']:['天','小时','分钟','秒'])
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
.text {
  position: relative;
  top: -3px;
}
</style>

