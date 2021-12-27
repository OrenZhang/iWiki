<template>
    <div>
        <el-skeleton :rows="6" animated v-if="loading" />
        <div v-if="!loading" class="comment-container">
            <v-md-editor
                :left-toolbar="leftTool"
                :right-toolbar="rightTool"
                :toolbar="toolbar"
                v-model="newContent" :mode="editType ? 'editable' : 'edit'" :placeholder="$t('content')" height="200px"
                :disabled-menus="[]" @upload-image="handleUploadImage" @save="doAddNewComment" />
            <el-card v-for="comment in comments" :key="comment.id" class="comment-box">
                <div class="card-header">
                    <div class="author-box">
                        <el-link class="user-link" target="_blank" type="primary">
                            {{ comment.username }}
                        </el-link>
                        &nbsp;
                        <div style="color: #909399; font-size: 12px;" class="update-at">
                            {{ comment.update_at }}
                        </div>
                    </div>
                    <div style="display: flex;" class="operate-box">
                        <el-link type="primary" @click="replyComment(comment.id)">
                            {{ $t('reply') }}
                        </el-link>
                        <el-link type="primary" @click="editComment(comment)" v-if="comment.creator === user.uid">
                            {{ $t('edit') }}
                        </el-link>
                        <el-link type="danger" v-if="comment.creator === user.uid" @click="showRemoveConfirm(comment.id)">
                            {{ $t('delete') }}
                        </el-link>
                    </div>
                </div>
                <el-divider />
                <v-md-editor mode="preview" v-model="comment.content" @image-click="imgClick" />
                <div v-if="comment.children.length > 0" class="child-comment-box">
                    <div v-for="childComment in comment.children" :key="childComment.id" class="child-comment">
                        <div style="margin-bottom: 10px; display: flex; justify-content: space-between;">
                            <div class="author-box">
                                <el-link class="user-link" target="_blank" type="primary">
                                    {{ childComment.username }}
                                </el-link>
                                <div style="color: #909399; font-size: 12px;" class="update-at">
                                    {{ childComment.update_at }}
                                </div>
                            </div>
                            <div class="operate-box">
                                <el-link type="primary" @click="replyComment(comment.id)">
                                    {{ $t('reply') }}
                                </el-link>
                                <el-link type="primary" @click="editComment(childComment)" v-if="childComment.creator === user.uid">
                                    {{ $t('edit') }}
                                </el-link>
                                <el-link type="danger" v-if="childComment.creator === user.uid" @click="showRemoveConfirm(childComment.id)">
                                    {{ $t('delete') }}
                                </el-link>
                            </div>
                        </div>
                        <v-md-editor mode="preview" v-model="childComment.content" @image-click="imgClick" />
                    </div>
                </div>
            </el-card>
            <el-pagination
                hide-on-single-page
                background layout="total, prev, pager, next, jumper"
                :page-size="commentsPaginator.size"
                :total="commentsPaginator.count"
                v-model:currentPage="commentsPaginator.page"
                @current-change="handlePageChange"
            />
        </div>
        <el-dialog
            v-model="commentDialog.visible"
            :title="$t('comment')"
            width="800px">
            <v-md-editor
                :left-toolbar="leftTool"
                :right-toolbar="rightToolWithoutSave"
                :toolbar="toolbar"
                v-model="commentDialog.content" :mode="editType ? 'editable' : 'edit'" :placeholder="$t('content')" height="200px"
                :disabled-menus="[]" @upload-image="handleUploadImage" />
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="commentDialog.visible = false">{{ $t('close') }}</el-button>
                    <el-button type="primary" @click="submitComment(commentDialog.content)">{{ $t('submit') }}</el-button>
                </span>
            </template>
        </el-dialog>
    </div>
</template>

<script setup>
    import { computed, onMounted, ref, watch } from 'vue'
    import http from '../api'
    import message from '../utils/message'
    import { useStore } from 'vuex'
    import { ElMessageBox } from 'element-plus'
    import { useI18n } from 'vue-i18n'

    const { t } = useI18n()
    
    // 界面适配
    const editType = computed(() => window.innerWidth >= 1100 )
    const width = ref(window.innerWidth)
    const leftTool = 'h bold italic strikethrough quote | ul ol table hr tip emoji todo-list | link image code'
    const rightTool = 'fullscreen preview toc save'
    const rightToolWithoutSave = 'fullscreen preview toc'
    onMounted(() => {
        window.addEventListener('resize', () => {
            width.value = window.innerWidth
        })
    })

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
        }
    })

    // 全局
    const store = useStore()
    const user = computed(() => store.state.user)

    // 加载状态
    const loading = ref(false)
    const setLoading = (status) => {
        if (status) {
            loading.value = true
        } else {
            setTimeout(() => {
                loading.value = false
            }, 600)
        }
    }

    // 传参
    const props = defineProps({
        docId: {
            type: String,
            default: ''
        }
    })

    // dialog
    const commentDialog = ref({
        visible: false,
        content: '',
        reply_to: null,
        id: null,
        method: 'add'
    })
    const submitComment = (text) => {
        commentDialog.value.visible = false
        switch (commentDialog.value.method) {
            case 'add':
                handleNewComment(text, null)
                break
            case 'reply':
                handleNewComment(text, commentDialog.value.reply_to)
                break
            case 'edit':
                handleUpdateComment(text, commentDialog.value.id)
                break
        }
    }
    const replyComment = (reply_to) => {
        commentDialog.value ={
            visible: true,
            content: '',
            reply_to: reply_to,
            id: null,
            method: 'reply'
        }
    }
    const editComment = (comment) => {
        commentDialog.value ={
            visible: true,
            content: comment.content,
            reply_to: comment.reply_to,
            id: comment.id,
            method: 'edit'
        }
    }

    const newContent = ref('')
    const doAddNewComment = (text, html) => {
        handleNewComment(text, null)
    }

    // 评论
    const comments = ref([])
    const commentsPaginator = ref({
        page: 1,
        count: 0,
        size: 10
    })
    const handlePageChange = (page) => {
        commentsPaginator.value.page = page
        loadComments()
    }
    const loadComments = () => {
        if (typeof props.docId !== 'string' || props.docId.length === 0) {
            return
        }
        setLoading(true)
        http.get(
            '/doc/comments/?doc_id=' + props.docId + '&size=' + commentsPaginator.value.size + '&page=' + commentsPaginator.value.page
        ).then(res => {
            comments.value = res.data.results
            commentsPaginator.value.count = res.data.count
            commentsPaginator.value.page = res.data.page
        }, err => {
            if (err.data.code === 404) {
                handlePageChange(1)
            }
        }).finally(() => {
            setLoading(false)
        })
    }
    watch(() => props.docId, () => {
        loadComments()
    })
    onMounted(loadComments)

    const imgClick = (images, currentIndex) => {
        const imgUrl = images[currentIndex]
        window.open(imgUrl)
    }

    // 新评论
    const handleNewComment = (text, reply_to) => {
        http.post(
            '/doc/comment/',
            {
                doc_id: props.docId,
                reply_to: reply_to,
                content: text
            }
        ).then(res => {
            loadComments()
            commentDialog.value.content = ''
            newContent.value = ''
        })
    }
    const handleUploadImage = (event, insertImage, files) => {
        let form = new FormData()
        form.append('file', files[0])
        http({
            url: '/cos/upload/',
            method: 'POST',
            headers: { 'Content-Type':'multipart/form-data' },
            data: form
        }).then(res => {
            if (res.result) {
                insertImage({
                    url: res.data[0].url,
                    desc: res.data[0].filename,
                    width: 'auto',
                    height: 'auto'
                })
            }
        }, err => {
            message(err.data.msg, 'error')
        })
    }
    const handleUpdateComment = (text, id) => {
        http.patch(
            '/doc/comment/' + id + '/',
            {
                content: text
            }
        ).then(() => {
            comments.value = updateLocalContent(id, text, comments.value)
        })
    }
    const updateLocalContent = (id, text, comments) => {
        for (const i in comments) {
            if (comments[i].id === id) {
                comments[i].content = text
                break
            }
            if (comments[i].children.length > 0) {
                comments[i].children = updateLocalContent(id, text, comments[i].children)
            }
        }
        return comments
    }
    const showRemoveConfirm = (id) => {
        const message = t('removeCommentConfirm')
        ElMessageBox.alert(
            message, 
            t('deleteConfirm'), {
                confirmButtonText: t('deleteConfirmed'),
                callback: (action) => {
                    if (action === 'confirm') {
                        http.delete(
                            '/doc/comment/' + id + '/'
                        ).then(() => {
                            loadComments()
                        })
                    }
                },
            })
    }
</script>

<style scoped>
    @import "../assets/Doc.css";
</style>