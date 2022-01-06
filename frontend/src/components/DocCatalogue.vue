<template>
    <el-card class="catalogue-box">
        <div class="title">
            {{ $t('docCatalogue') }}
        </div>
        <ul v-if="titles.length > 0">
            <template v-for="anchor in titles" :key="anchor">
                <li
                    v-if="anchor.indent <= 2"
                    :style="{ padding: `0 0 10px ${anchor.indent * 20}px` }"
                    @click="doScroll(anchor)">
                    <a style="cursor: pointer">{{ anchor.title }}</a>
                </li>
            </template>
        </ul>
        <div v-else style="text-align: center; margin-top: 20px; color: var(--el-text-color-secondary)">
            {{ $t('noMoreCat') }}
        </div>
    </el-card>
</template>

<script setup>
    defineProps({
        titles: {
            type: Object,
            default: []
        }
    })

    const emits = defineEmits(['doScroll'])

    const doScroll = (anchor) => {
        const { lineIndex } = anchor
        const top = document.querySelector(`[data-v-md-line="${lineIndex}"]`).offsetTop
        emits('doScroll', top)
    }
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