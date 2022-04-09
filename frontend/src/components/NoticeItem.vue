<template>
    <el-card class="notice-item-container">
        <template #header>
            <div class="card-header" :class="data.is_read ? 'already-read' : ''">
                <div class="info">
                    <div style="font-weight: bold; padding: 12px 0">
                        {{ data.title }}
                    </div>
                    <div class="create-at">
                        {{ data.create_at }}
                    </div>
                </div>
                <div class="button">
                    <el-button v-if="!data.is_read" type="text" @click="readNotice(data.log_id)">
                        {{ $t('readNotice') }}
                    </el-button>
                </div>
            </div>
        </template>
        <div class="content" :class="data.is_read ? 'already-read' : ''" v-html="data.content" />
        <div v-if="data.button_text" class="deal-button" :class="data.is_read ? 'already-read' : ''">
            <el-button type="text" @click="dealNotice(data.log_id, data.url)">
                {{ data.button_text }}
            </el-button>
        </div>
    </el-card>
</template>

<script setup>
    const props = defineProps({
        data: {
            type: Object,
            default: {
                id: 0,
                log_id: 0,
                title: '',
                content: '',
                is_read: false,
                button_text: '',
                url: '',
                create_at: ''
            }
        }
    })

    const emits = defineEmits(['readNotice'])

    const readNotice = (id) => {
        emits('readNotice', id)
    }

    const dealNotice = (id, url) => {
        readNotice(id)
        window.open(url)
    }
</script>

<style scoped>
    .notice-item-container {
        margin-bottom: 20px;
    }

    .notice-item-container :deep(.el-card__body) .content a {
        color: var(--el-color-primary);
        text-decoration: none;
    }

    .notice-item-container :deep(.el-card__header) {
        padding: 6px 20px;
    }

    .create-at {
        color: var(--el-text-color-secondary);
        margin-top: -12px;
        padding: 0 0 12px 0;
        font-size: 14px;
    }

    .notice-item-container .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .deal-button {
        display: flex;
        justify-content: flex-end;
        margin-top: 20px;
    }

    .deal-button .el-button {
        padding: 0;
        min-height: unset;
    }

    :deep(.already-read){
        color: var(--el-text-color-secondary);
        /*text-decoration:line-through;*/
    }

    :deep(.already-read) a,
    :deep(.already-read) .el-button--text {
        color: var(--el-color-primary-light-4) !important;
        /*text-decoration:line-through;*/
    }

    .content {
        font-size: 14px;
    }
</style>