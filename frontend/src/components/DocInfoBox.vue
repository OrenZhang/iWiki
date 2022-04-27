<template>
    <div v-show="!loading">
        <div class="info-box">
            <h2 class="title-box">
                {{ docData.title }}
            </h2>
            <div class="author-box">
                <div style="display: flex; align-items: center">
                    <el-tag size="mini" type="danger" v-if="docData.available === 'private'">
                        {{ $t('private') }}
                    </el-tag>
                    <el-tag size="mini" v-else>
                        {{ $t('public') }}
                    </el-tag>
                    <i class="fa-solid fa-cube ml-10 mr-2" v-if="docData.repo_name" />
                    <el-link :underline="false" :href="globalContext.siteUrl + 'repo/' + docData.repo_id" target="_blank" v-if="docData.repo_name">
                        {{ docData.repo_name }}
                    </el-link>
                    <i class="fa-regular fa-user ml-10 mr-2" v-if="docData.creator_name" />
                    <el-link :underline="false" :href="globalContext.siteUrl + 'user/' + docData.creator_name" target="_blank" v-if="docData.creator_name">
                        {{ docData.creator_name }}
                    </el-link>
                    <i class="fa-regular fa-clock ml-10 mr-2" />
                    {{ docData.update_at }}
                    <el-link :underline="false" v-if="user.auth" @click="toggleCollectStatus">
                        <i class="ml-10 mr-2 fa-star" :class="isCollect ? 'fa-solid color-yellow' : 'fa-regular'" />
                    </el-link>
                </div>
                <div class="operate-box">
                    <el-link type="primary" :href="globalContext.backEndUrl + '/doc/manage/' + docData.id + '/export/'" target="_blank" v-if="docData.creator === user.uid || isCollaborator">
                        {{ $t('export') }}
                    </el-link>
                    <el-link type="primary" :href="globalContext.siteUrl + 'publish/' + docData.id" v-if="docData.creator === user.uid || isCollaborator">
                        {{ $t('edit') }}
                    </el-link>
                    <el-link type="danger" @click="showDeleteConfirm" v-if="docData.creator === user.uid">
                        {{ $t('delete') }}
                    </el-link>
                </div>
            </div>
            <el-divider />
            <div class="content-box">
                <v-md-editor ref="preview" v-if="!loading" v-model="content" mode="preview" @image-click="imgClick" />
            </div>
        </div>
        <el-divider v-if="attachments.length > 0" />
        <div class="attach-box" v-if="attachments.length > 0">
            <h4>
                {{ $t('attachments') }}
            </h4>
            <ul v-if="attachments.length > 0">
                <li v-for="item in attachments" :key="item">
                    <el-link :href="item.url" type="primary" target="_blank">
                        {{ item.name }}
                    </el-link>
                </li>
            </ul>
        </div>
    </div>
</template>

<script setup>
    import globalContext from '../context'
    import { computed, nextTick, onMounted, ref, watch } from 'vue'
    import { ElMessageBox } from 'element-plus'
    import { useStore } from 'vuex'
    import { useI18n } from 'vue-i18n'
    import {
        checkDocCollaboratorAPI,
        collectDocAPI,
        deleteDocAPI,
        getDocCollectStatusAPI,
        unCollectDocAPI
    } from '../api/modules/doc'
    import message from '../utils/message'
    
    const { t } = useI18n()

    const emits = defineEmits(['loadTitle'])

    // vuex
    const store = useStore()
    const user = computed(() => store.state.user)

    const props = defineProps({
        docData: {
            type: Object,
            default: {
                id: '',
                title: '',
                creator_name: '',
                update_at: '',
                content: '',
                creator: '',
                repo_name: '',
                attachments: {}
            }
        },
        loading: {
            type: Boolean,
            default: true
        }
    })

    const attachments = computed(() => {
        const attachmentsTmp = ref([])
        for (const key in props.docData.attachments) {
            attachmentsTmp.value.push({
                name: key,
                url: props.docData.attachments[key]
            })
        }
        return attachmentsTmp.value
    })

    const content = ref('')
    watch(() => props.docData.content, newVal => {
        content.value = newVal
    })
    
    const imgClick = (images, currentIndex) => {
        const imgUrl = images[currentIndex]
        window.open(imgUrl)
    }

    const showDeleteConfirm = () => {
        const message = t('deleteDocConfirmContent', { title: props.docData.title })
        ElMessageBox.alert(
            message,
            t('deleteConfirm'),
            {
                confirmButtonText: t('deleteConfirmed'),
                callback: (action) => {
                    if (action === 'confirm') {
                        doDelete()
                    }
                },
            })
    }
    const doDelete = () => {
        store.dispatch('setMainLoading', true)
        deleteDocAPI(props.docData.id).then(() => {
            window.location.replace(globalContext.siteUrl)
        }).finally(() => {
            store.dispatch('setMainLoading', false)
        })
    }

    const preview = ref(null)
    const titles = ref([])
    const loadTitle = () => {
        try {
            const anchors = preview.value.$el.querySelectorAll('h1,h2,h3,h4,h5,h6')
            const titlesTmp = Array.from(anchors).filter((title) => !!title.innerText.trim())
            const hTags = Array.from(new Set(titlesTmp.map((title) => title.tagName))).sort()
            titles.value = titlesTmp.map((el) => ({
                title: el.innerText,
                lineIndex: el.getAttribute('data-v-md-line'),
                indent: hTags.indexOf(el.tagName),
            }))
        } catch (e) {}
    }
    onMounted(() => {
        nextTick(() => {
            try {
                setTimeout(() => {
                    loadTitle()
                    emits('loadTitle', titles.value)
                }, 3000)
            } catch (e) {}
        })
    })

    const isCollaborator = ref(false)
    const checkCollaborator = () => {
        checkDocCollaboratorAPI(props.docData.id).then(res => {
            isCollaborator.value = res.result
        })
    }

    const isCollect = ref(false)
    const getDocCollectStatus = () => {
        getDocCollectStatusAPI(props.docData.id).then(
            res => isCollect.value = res.data,
            err => message(err.data.msg, 'error')
        )
    }

    const toggleCollectStatus = () => {
        if (isCollect.value) {
            unCollectDocAPI(props.docData.id).then(
                res => isCollect.value = false,
                err => message(err.data.msg, 'error')
            )
        } else {
            collectDocAPI(props.docData.id).then(
                res => isCollect.value = true,
                err => message(err.data.msg, 'error')
            )
        }
    }

    watch(() => props.docData.id, () => {
        if (props.docData.id) {
            checkCollaborator()
            getDocCollectStatus()
        }
    })
</script>

<style scoped>
    @import "../assets/Doc.css";
</style>