<template>
    <div class="h-100">
        <ErrorPage :error="errorCode" v-if="!loading && errorCode !== 0" />
        <div v-loading.fullscreen.lock="loading" :element-loading-text="loadingText" class="editor-box" v-if="errorCode === 0">
            <div class="header">
                <el-input :placeholder="$t('title')" :maxlength="64" show-word-limit v-model="docData.title" />
                <el-button class="save-button" type="primary" @click="publishDrawer.visible = true" :disabled="checkDocData">
                    {{ $t('save') }}
                </el-button>
            </div>
            <v-md-editor
                left-toolbar="undo redo | h bold italic strikethrough quote align | ul ol table hr tip emoji todo-list | link image code"
                :toolbar="toolbar"
                v-model="docData.content" :mode="editType ? 'editable' : 'edit'" right-toolbar="fullscreen preview toc sync-scroll" :placeholder="$t('content')"
                :disabled-menus="[]" @image-click="imgClick" @save="checkSave" @upload-image="handleUploadImage" />
            <el-drawer
                :size="480"
                v-model="publishDrawer.visible"
                :title="$t('publishDoc')">
                <el-form :label-width="80" label-position="left" class="publish-form">
                    <el-form-item :label="$t('repo')">
                        <el-select v-model="docData.repo_id">
                            <el-option
                                v-for="item in repos"
                                :key="item.id"
                                :label="item.name"
                                :value="item.id"
                            />
                        </el-select>
                    </el-form-item>
                    <el-form-item :label="$t('available')">
                        <el-select v-model="docData.available">
                            <el-option
                                v-for="item in available"
                                :key="item.id"
                                :label="item.name"
                                :value="item.id"
                            />
                        </el-select>
                    </el-form-item>
                    <el-form-item :label="$t('attachments')">
                        <el-upload
                            :on-progress="handleOnProgress"
                            :on-error="handleErrorFile"
                            :on-success="handleSuccessFile"
                            :action="uploadUrl"
                            :show-file-list="false" :with-credentials="true" multiple>
                            <el-button size="medium" type="primary" :loading="fileUploading" :disabled="fileUploading">
                                {{ $t('uploadAttachment') }}
                            </el-button>
                            <span class="upload-notice">({{ $t('fileUpTo200M') }})</span>
                        </el-upload>
                        <el-table v-if="attachments.length > 0" :data="attachments" :show-header="false" size="medium" style="width: 100%">
                            <el-table-column prop="name" />
                            <el-table-column width="40">
                                <template #default="scope">
                                    <el-button type="text" @click="removeAttachment(scope.row)">
                                        <i class="fa-solid fa-times" style="color: var(--el-color-danger)" />
                                    </el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                    </el-form-item>
                    <el-form-item :label="$t('collaborator')" v-if="user.uid === docData.creator">
                        <div class="collaborator-box">
                            <el-table border :data="collaborators" :show-header="false">
                                <el-table-column prop="username">
                                    <template #default="scope">
                                        <span v-if="scope.row.type === undefined">{{ scope.row.username }}</span>
                                        <el-select
                                            class="add-col-select"
                                            v-else-if="scope.row.type === 'edit'" v-model="newUID"
                                            filterable remote reserve-keyword :placeholder="$t('inputUsername')" :remote-method="remoteMethod" :loading="remoteLoading">
                                            <el-option
                                                v-for="item in userOptions"
                                                :key="item.uid"
                                                :label="item.username"
                                                :value="item.uid" />
                                        </el-select>
                                    </template>
                                </el-table-column>
                                <el-table-column width="80">
                                    <template #default="scope">
                                        <el-link v-if="scope.row.type === undefined" type="danger" @click="removeCol(scope.row)">
                                            {{ $t('delete') }}
                                        </el-link>
                                        <el-link v-else-if="scope.row.type === 'add'" :disabled="hasUnSaveCol" type="primary" @click="addCol()">
                                            {{ $t('add') }}
                                        </el-link>
                                        <el-link v-else-if="scope.row.type === 'edit'" type="primary" @click="doAddCol()">
                                            {{ $t('save') }}
                                        </el-link>
                                    </template>
                                </el-table-column>
                            </el-table>
                        </div>
                    </el-form-item>
                </el-form>
                <div class="publish-button-box">
                    <el-button @click="SaveContent()" :disabled="checkDocDataAndRepo">
                        {{ $t('saveAsDraft') }}
                    </el-button>
                    <el-button type="success" @click="SaveContent(true)" :disabled="checkDocDataAndRepo">
                        {{ $t('Publish') }}
                    </el-button>
                </div>
            </el-drawer>
        </div>
    </div>
</template>

<script setup>
    import ErrorPage from '../components/ErrorPage.vue'
    import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
    import { useStore } from 'vuex'
    import { onBeforeRouteLeave, useRoute, useRouter } from 'vue-router'
    import message from '../utils/message'
    import globalContext from '../context'
    import { useI18n } from 'vue-i18n'
    import { loadRepoAPI } from '../api/modules/repo'
    import { uploadFileAPI } from '../api/modules/common'
    import {
        addDocCollaboratorAPI, checkDocEditingAPI,
        createOrUpdateDocAPI,
        loadDocCollaboratorAPI,
        loadDocDataManageAPI,
        removeDocCollaboratorAPI
    } from '../api/modules/doc'
    import { searchUserAPI } from '../api/modules/user'
    import { setTitle } from '../utils/controller'

    const { t } = useI18n()

    onMounted(() => {
        setTitle(t('New'))
    })

    // vuex
    const store = useStore()
    const user = computed(() => store.state.user)

    // toolbar
    const toolbar = ref({
        code: {
            title: t('code'),
            icon: 'v-md-icon-code',
            menus: [
                {
                    name: 'line-code',
                    text: t('inlineCode'),
                    action(editor) {
                        editor.insert(function (selected) {
                            const prefix = '`'
                            const suffix = '`'
                            const placeholder = 'you code here'
                            const content = selected || placeholder
                            return {
                                text: `${prefix}${content}${suffix}`,
                                selected: content,
                            }
                        })
                    }
                },
                {
                    name: 'code-block',
                    text: t('codeBlock'),
                    action(editor) {
                        editor.insert(function (selected) {
                            const prefix = '```language\n'
                            const suffix = '\n```'
                            const placeholder = 'you code here'
                            const content = selected || placeholder
                            return {
                                text: `${prefix}${content}${suffix}`,
                                selected: content,
                            }
                        })
                    },
                },
            ],
        },
        align: {
            title: t('align'),
            icon: 'fa-solid fa-align-left',
            menus: [
                {
                    name: 'left',
                    text: t('alignLeft'),
                    action(editor) {
                        editor.insert(function (selected) {
                            const prefix = ':::align-left\n'
                            const suffix = '\n:::'
                            const placeholder = 'you text here'
                            const content = selected || placeholder
                            return {
                                text: `${prefix}${content}${suffix}`,
                                selected: content,
                            }
                        })
                    }
                },
                {
                    name: 'center',
                    text: t('alignCenter'),
                    action(editor) {
                        editor.insert(function (selected) {
                            const prefix = ':::align-center\n'
                            const suffix = '\n:::'
                            const placeholder = 'you text here'
                            const content = selected || placeholder
                            return {
                                text: `${prefix}${content}${suffix}`,
                                selected: content,
                            }
                        })
                    }
                },
                {
                    name: 'right',
                    text: t('alignRight'),
                    action(editor) {
                        editor.insert(function (selected) {
                            const prefix = ':::align-right\n'
                            const suffix = '\n:::'
                            const placeholder = 'you text here'
                            const content = selected || placeholder
                            return {
                                text: `${prefix}${content}${suffix}`,
                                selected: content,
                            }
                        })
                    }
                },
            ]
        },
    })

    // 加载状态
    const loading = ref(false)
    const loadingText = ref('')
    const setLoading = (status, text = '') => {
        if (status) {
            loadingText.value = text
            loading.value = true
        } else {
            setTimeout(() => {
                loading.value = false
                loadingText.value = ''
            }, 600)
        }
    }

    // 数据
    const repos = ref([])
    const docID = computed(() => route.params.id)
    const docData = ref({
        repo_id: '',
        available: 'public',
        title: '',
        content: '',
        attachments: {},
        is_publish: false,
        creator: ''
    })
    const available = ref([
        {
            id: 'public',
            name: t('public')
        },
        {
            id: 'private',
            name: t('private')
        }
    ])
    const checkDocData = computed(() => docData.value.title === '' || docData.value.content === '')
    const checkDocDataAndRepo = computed(() => docData.value.repo_id === '' || docData.value.title === '' || docData.value.content === '')
    const attachments = computed(() => {
        const attachmentsTmp = ref([])
        for (const key in docData.value.attachments) {
            attachmentsTmp.value.push({
                name: key,
                url: docData.value.attachments[key]
            })
        }
        return attachmentsTmp.value
    })

    // 保存
    const checkSave = () => {
        if (!checkDocData.value) {
            publishDrawer.value.visible = true
        }
    }

    // 发布抽屉
    const publishDrawer = ref({
        visible: false
    })

    // 仓库数据
    const loadRepos = () => {
        loadRepoAPI().then(res => {
            if (res.result) {
                repos.value = res.data
                if (repos.value.length > 0 && docData.value.repo_id === '') {
                    docData.value.repo_id = repos.value[0].id
                }
            }
        })
    }
    onMounted(loadRepos)

    // 编辑器
    const editType = computed(() => window.innerWidth >= 1100 )
    const uploadUrl = globalContext.backEndUrl + '/cos/upload/'
    const imgClick = (images, currentIndex) => {
        const imgUrl = images[currentIndex]
        window.open(imgUrl)
    }
    const handleUploadImage = (event, insertImage, files) => {
        setLoading(true, t('imgUploading'))
        let form = new FormData()
        form.append('file', files[0])
        uploadFileAPI('/cos/upload/', form).then(res => {
            if (res.result) {
                insertImage({
                    url: res.data[0].url,
                    desc: res.data[0].filename,
                    width: 'auto',
                    height: 'auto'
                })
                message(t('imgUploadSuccess'))
            }
        }, err => {
            message(err.data.msg, 'error')
        }).finally(() => {
            setLoading(false)
        })
    }
    const savedStatus = ref(false)
    const SaveContent = (isPublish = false) => {
        publishDrawer.value.visible = false
        setLoading(true)
        docData.value.is_publish = isPublish
        const messageContent = isPublish ? t('publishSuccess') : t('saveSuccess')
        const url = ref('/doc/manage/')
        const method = ref('POST')
        if (docID.value !== undefined) {
            url.value = '/doc/manage/' + docID.value + '/'
            method.value = 'PATCH'
        }
        createOrUpdateDocAPI(url.value, method.value, docData.value).then(res => {
            if (res.result) {
                message(messageContent)
                clearInterval(autoSaveInterval)
                clearLocalData()
                if (isPublish) {
                    savedStatus.value = true
                    router.push({ path: '/doc/' + res.data.id })
                } else {
                    window.location.href = '/publish/' + res.data.id
                }
            }
        }, err => {
            message(err.data.msg, 'error')
        }).finally(() => {
            setLoading(false)
        })
    }

    // 自动保存(本地)
    const localStorageKey = computed(() => docID.value ? 'autoSavePublishContent-' + docID.value : 'autoSavePublishContent')
    let autoSaveInterval
    onMounted(() => {
        autoSaveInterval = setInterval(() => {
            try {
                localStorage.setItem(localStorageKey.value, docData.value.content)
            } catch (e) {
                localStorage.clear()
                console.log(e)
            }
        }, 10000)
    })
    onUnmounted(() => {
        clearInterval(autoSaveInterval)
    })
    const loadLocalData = () => {
        const localData = localStorage.getItem(localStorageKey.value)
        if (localData) {
            docData.value.content = localData
        }
    }
    const clearLocalData = () => {
        localStorage.removeItem(localStorageKey.value)
    }

    // 文章数据
    const permissionDenied = ref(false)
    const error404 = ref(false)
    const errorCode = computed(() => {
        if (error404.value) {
            return 404
        } else if (permissionDenied.value) {
            return 403
        } else if (!editStatus.value) {
            return 400001
        }
        return 0
    })
    const loadDocData = () => {
        setLoading(true)
        loadDocDataManageAPI(docID.value).then(res => {
            docData.value = {
                repo_id: res.data.repo_id,
                available: res.data.available,
                title: res.data.title,
                content: res.data.content,
                attachments: res.data.attachments,
                is_publish: res.data.is_publish,
                creator: res.data.creator
            }
        }, err => {
            message(err.data.msg, 'error')
            if (err.status === 403) {
                permissionDenied.value = true
            } else if (err.status === 404) {
                error404.value = true
            }
        }).finally(() => {
            loadLocalData()
            setLoading(false)
        })
    }

    // 附件
    const fileUploading = ref(false)
    const removeAttachment = (row) => {
        delete docData.value.attachments[row.name]
    }
    const handleSuccessFile = (response) => {
        const fileName = response.data[0].filename
        fileUploading.value = false
        docData.value.attachments[fileName] = response.data[0].url
    }
    const handleErrorFile = (err) => {
        const errData = JSON.parse(err.message)
        fileUploading.value = false
        message(errData.msg, 'error')
    }
    const handleOnProgress = () => {
        fileUploading.value = true
    }

    // 协作者
    const newUID = ref('')
    const remoteLoading = ref(false)
    const userOptions = ref([])
    const collaborators = ref([])
    const remoteMethod = (searchKey) => {
        if (searchKey === '') {
            return
        }
        remoteLoading.value = true
        searchUserAPI(searchKey).then(res => {
            userOptions.value = res.data
        }).finally(() => {
            remoteLoading.value = false
        })
    }
    const loadCol = () => {
        loadDocCollaboratorAPI(docID.value).then(res => {
            collaborators.value = res.data
            collaborators.value.push({ username: '', uid: '', type: 'add' })
        })
    }
    const removeCol = (row) => {
        removeDocCollaboratorAPI(docID.value, row.uid).finally(() => {
            loadCol()
        })
    }
    const addCol = () => {
        const length = collaborators.value.length
        collaborators.value.splice(length - 1, 0, { username: '', uid: '', type: 'edit' })
    }
    const hasUnSaveCol = computed(() => {
        for (const item of collaborators.value) {
            if (item.type === 'edit') {
                return true
            }
        }
        return false
    })
    const doAddCol = () => {
        addDocCollaboratorAPI(docID.value, newUID.value).then(() => {
            newUID.value = ''
        }, err => {
            message(err.data.msg, 'error')
        }).finally(() => {
            loadCol()
        })
    }

    // router
    const route = useRoute()
    const router = useRouter()
    onMounted(() => {
        if (docID.value !== undefined) {
            loadDocData()
            loadCol()
        } else {
            loadLocalData()
        }
    })
    watch(() => docID.value, () => {
        if (docID.value === undefined) {
            window.location.reload()
        }
    })
    
    onBeforeRouteLeave(() => {
        if (!savedStatus.value) {
            const answer = window.confirm(t('leaveConfirm'))
            if (!answer) return false
        }
    })

    // 编辑状态
    const editStatus = ref(true)
    let editStatusInterval
    const checkEditStatus = () => {
        if (!docID.value) {
            return
        }
        checkDocEditingAPI(docID.value).then(res => {
            editStatus.value = res.data
        }).finally(() => {
            if (editStatus.value) {
                editStatusInterval = setInterval(() => {
                    checkDocEditingAPI(docID.value)
                }, 10000)
            }
        })
    }
    onMounted(checkEditStatus)
    onUnmounted(() => {
        clearInterval(editStatusInterval)
    })
</script>

<style scoped>
    @import "../assets/Publish.css";
</style>