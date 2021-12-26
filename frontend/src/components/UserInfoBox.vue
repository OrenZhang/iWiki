<template>
    <el-card class="user-info-box">
        <div class="user-info">
            <div class="user-avatar" @click="goTo('user')">
                <el-avatar class="default-avatar" v-if="user.avatar !== null && user.avatar !== ''" :src="user.avatar" />
                <el-avatar v-else class="default-avatar">
                    <i class="fa-solid fa-user" />
                </el-avatar>
            </div>
            <el-link :underline="false" class="user-name" :href="globalContext.siteUrl + 'user'" target="_blank">
                {{ user.username }}
            </el-link>
        </div>
        <div class="user-statistic">
            <el-row :gutter="30">
                <el-col :span="12" class="statistic-box">
                    <div>{{ $t('myDocs') }}</div>
                    <div>
                        <el-tag size="mini" effect="plain">
                            {{ userProperty.doc_count }}
                        </el-tag>
                    </div>
                </el-col>
                <el-col :span="12" class="statistic-box">
                    <div>{{ $t('myComments') }}</div>
                    <div>
                        <el-tag size="mini" effect="plain">
                            {{ userProperty.comment_count }}
                        </el-tag>
                    </div>
                </el-col>
                <el-col :span="12" class="statistic-box">
                    <div>{{ $t('myRepos') }}</div>
                    <div>
                        <el-tag size="mini" effect="plain">
                            {{ userProperty.repo_count }}
                        </el-tag>
                    </div>
                </el-col>
                <el-col :span="12" class="statistic-box">
                    <div>{{ $t('activeIndex') }}</div>
                    <div>
                        <el-tag size="mini" effect="plain">
                            {{ userProperty.active_index }}
                        </el-tag>
                    </div>
                </el-col>
            </el-row>
        </div>
        <el-button-group class="button-box">
            <el-button style="width: 51%" type="primary" plain @click="goTo('user')">
                <strong>{{ $t('userCenter') }}</strong>
            </el-button>
            <el-button style="width: 51%" type="primary" plain @click="goTo('publish')">
                <strong>{{ $t('NewDoc') }}</strong>
            </el-button>
        </el-button-group>
    </el-card>
</template>

<script setup>
    import globalContext from '../context'
    import { useStore } from 'vuex'
    import { useRouter } from 'vue-router'
    import { computed } from 'vue'
    
    const router = useRouter()

    const goTo = (url) => {
        window.open(globalContext.siteUrl + url)
    }

    const store = useStore()
    const user = computed(() => store.state.user)

    const userProperty = computed(() => {
        const data = {}
        for (const i in user.value.property) {
            const num = user.value.property[i]
            if (num <= 999 ) {
                const numArray = num.toString().split('.')
                // 针对浮点数的处理
                if (numArray.length > 1)
                    if (num < 10) {
                        data[i] = num.toFixed(2)
                    } else {
                        data[i] = num.toFixed(1)
                    }
                // 整数输出
                else {
                    data[i] = num
                }
            } else {
                data[i] = '999+'
            }
        }
        return data
    })
</script>

<style scoped>
    @import "../assets/UserInfoBox.css";
</style>