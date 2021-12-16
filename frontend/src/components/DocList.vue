<template>
    <div>
        <el-empty v-if="paginator.count === 0" />
        <div v-else>
            <el-card v-for="item in docs" :key="item.id" class="single-doc-box">
                <el-link target="_blank" :href="'/doc/' + item.id">
                    <h4>{{ item.title }}</h4>
                </el-link>
                <div class="author-box">
                    <div>
                        <el-tag v-if="item.available === 'public'" size="mini">
                            {{ $t('public') }}
                        </el-tag>
                        <el-tag v-else size="mini" type="warning">
                            {{ $t('private') }}
                        </el-tag>
                    </div>
                    <i class="far fa-archive ml-10 mr-2" v-if="item.repo_name" />
                    <el-link :underline="false" :href="'/repo/' + item.repo_id" target="_blank" v-if="item.repo_name">
                        {{ item.repo_name }}
                    </el-link>
                    <i class="far fa-user ml-10 mr-2" v-if="item.creator_name" />
                    <el-link :underline="false" :href="'/user/' + item.creator_name" target="_blank" v-if="item.creator_name">
                        {{ item.creator_name }}
                    </el-link>
                    <i class="far fa-clock ml-10 mr-2" />
                    <el-link :underline="false">
                        {{ item.update_at }}
                    </el-link>
                </div>
            </el-card>
            <el-pagination
                background layout="total, prev, pager, next, jumper"
                :total="paginator.count"
                :current-page="paginator.page"
                @current-change="handlePageChange"
                v-if="usePaginator"
            />
        </div>
    </div>
</template>

<script setup>
    import { computed } from 'vue'

    const props = defineProps({
        data: {
            type: Object,
            default: {
                usePaginator: true,
                paginator: {
                    page: 1,
                    count: 0,
                    size: 10
                },
                data: []
            }
        }
    })

    const emits = defineEmits(['pageChange'])
    
    const docs = computed(() => props.data.data)
    const paginator = computed(() => props.data.paginator)
    const usePaginator = computed(() => props.data.usePaginator)

    const handlePageChange = (page) => {
        emits('pageChange', page)
    }
</script>

<style scoped>
    .el-card {
        border: none;
        margin-bottom: 20px;
        border-radius: 5px;
    }

    .el-pagination {
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .single-doc-box h4 {
        margin-top: 0;
        margin-bottom: 0;
        font-size: 16px;
    }

    .single-doc-box > div > .el-link {
        margin-bottom: 10px;
    }

    .author-box {
        margin: 0;
        display: flex;
        align-items: center;
        font-size: 14px;
    }

    .ml-10 {
        margin-left: 10px;
    }

    .mr-2 {
        margin-right: 2px;
    }
</style>