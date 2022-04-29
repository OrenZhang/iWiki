<!--
 - MIT License
 -
 - Copyright (c) 2021 Oren Zhang
 -
 - Permission is hereby granted, free of charge, to any person obtaining a copy
 - of this software and associated documentation files (the "Software"), to deal
 - in the Software without restriction, including without limitation the rights
 - to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 - copies of the Software, and to permit persons to whom the Software is
 - furnished to do so, subject to the following conditions:
 -
 - The above copyright notice and this permission notice shall be included in all
 - copies or substantial portions of the Software.
 -
 - THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 - IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 - FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 - AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 - LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 - OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 - SOFTWARE.
-->

<template>
  <div v-loading.fullscreen.lock="fullLoading">
    <el-skeleton
      :rows="6"
      animated
      v-if="loading"
    />
    <div
      v-if="!loading"
      class="comment-container"
    >
      <v-md-editor
        :left-toolbar="leftTool"
        :right-toolbar="rightTool"
        :toolbar="toolbar"
        v-model="newContent"
        :mode="editType ? 'editable' : 'edit'"
        :placeholder="$t('content')"
        height="200px"
        :disabled-menus="[]"
        @upload-image="handleUploadImage"
        @save="doAddNewComment"
      />
      <el-card
        v-for="comment in comments"
        :key="comment.id"
        class="comment-box"
      >
        <div class="card-header">
          <div class="author-box">
            <el-link
              class="user-link"
              :href="globalContext.siteUrl + 'user/' + comment.username"
              target="_blank"
              type="primary"
            >
              {{ comment.username }}
            </el-link>
                        &nbsp;
            <div
              style="color: var(--el-text-color-secondary); font-size: 12px;"
              class="update-at"
            >
              {{ comment.update_at }}
            </div>
          </div>
          <div
            style="display: flex;"
            class="operate-box"
          >
            <el-link
              type="primary"
              @click="replyComment(comment.id)"
            >
              {{ $t('reply') }}
            </el-link>
            <el-link
              type="primary"
              @click="editComment(comment)"
              v-if="comment.creator === user.uid"
            >
              {{ $t('edit') }}
            </el-link>
            <el-link
              type="danger"
              v-if="comment.creator === user.uid"
              @click="showRemoveConfirm(comment.id)"
            >
              {{ $t('delete') }}
            </el-link>
          </div>
        </div>
        <el-divider />
        <v-md-editor
          mode="preview"
          v-model="comment.content"
          @image-click="imgClick"
        />
        <div
          v-if="comment.children.length > 0"
          class="child-comment-box"
        >
          <div
            v-for="childComment in comment.children"
            :key="childComment.id"
            class="child-comment"
          >
            <div style="margin-bottom: 10px; display: flex; justify-content: space-between;">
              <div class="author-box">
                <el-link
                  class="user-link"
                  target="_blank"
                  type="primary"
                >
                  {{ childComment.username }}
                </el-link>
                <div
                  style="color: var(--el-text-color-secondary); font-size: 12px;"
                  class="update-at"
                >
                  {{ childComment.update_at }}
                </div>
              </div>
              <div class="operate-box">
                <el-link
                  type="primary"
                  @click="replyComment(comment.id)"
                >
                  {{ $t('reply') }}
                </el-link>
                <el-link
                  type="primary"
                  @click="editComment(childComment)"
                  v-if="childComment.creator === user.uid"
                >
                  {{ $t('edit') }}
                </el-link>
                <el-link
                  type="danger"
                  v-if="childComment.creator === user.uid"
                  @click="showRemoveConfirm(childComment.id)"
                >
                  {{ $t('delete') }}
                </el-link>
              </div>
            </div>
            <v-md-editor
              mode="preview"
              v-model="childComment.content"
              @image-click="imgClick"
            />
          </div>
        </div>
      </el-card>
      <el-pagination
        hide-on-single-page
        background
        layout="total, prev, pager, next, jumper"
        :page-size="commentsPaginator.size"
        :total="commentsPaginator.count"
        v-model:currentPage="commentsPaginator.page"
        @current-change="handlePageChange"
      />
    </div>
    <el-dialog
      v-model="commentDialog.visible"
      :close-on-press-escape="false"
      :title="$t('comment')"
      width="800px"
    >
      <v-md-editor
        :left-toolbar="leftTool"
        :right-toolbar="rightToolWithoutSave"
        :toolbar="toolbar"
        v-model="commentDialog.content"
        :mode="editType ? 'editable' : 'edit'"
        :placeholder="$t('content')"
        height="200px"
        :disabled-menus="[]"
        @upload-image="handleUploadImage"
      />
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="commentDialog.visible = false">{{ $t('close') }}</el-button>
          <el-button
            type="primary"
            @click="submitComment(commentDialog.content)"
          >{{ $t('submit') }}</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch, defineProps } from 'vue';
import message from '../utils/message';
import { useStore } from 'vuex';
import { ElMessageBox } from 'element-plus';
import { useI18n } from 'vue-i18n';
import globalContext from '../context';
import { createCommentAPI, deleteCommentAPI, loadCommentAPI, updateCommentAPI } from '../api/modules/comment';
import { uploadFileAPI } from '../api/modules/common';

const { t } = useI18n();

// 界面适配
const editType = computed(() => window.innerWidth >= 1100);
const width = ref(window.innerWidth);
const leftTool = 'h bold italic strikethrough quote align | ul ol table hr tip emoji todo-list | link image code';
const rightTool = 'fullscreen preview toc save';
const rightToolWithoutSave = 'fullscreen preview toc';
onMounted(() => {
  window.addEventListener('resize', () => {
    width.value = window.innerWidth;
  });
});

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
          editor.insert((selected) => {
            const prefix = '`';
            const suffix = '`';
            const placeholder = 'you code here';
            const content = selected || placeholder;
            return {
              text: `${prefix}${content}${suffix}`,
              selected: content,
            };
          });
        },
      },
      {
        name: 'code-block',
        text: t('codeBlock'),
        action(editor) {
          editor.insert((selected) => {
            const prefix = '```language\n';
            const suffix = '\n```';
            const placeholder = 'you code here';
            const content = selected || placeholder;
            return {
              text: `${prefix}${content}${suffix}`,
              selected: content,
            };
          });
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
          editor.insert((selected) => {
            const prefix = ':::align-left\n';
            const suffix = '\n:::';
            const placeholder = 'you text here';
            const content = selected || placeholder;
            return {
              text: `${prefix}${content}${suffix}`,
              selected: content,
            };
          });
        },
      },
      {
        name: 'center',
        text: t('alignCenter'),
        action(editor) {
          editor.insert((selected) => {
            const prefix = ':::align-center\n';
            const suffix = '\n:::';
            const placeholder = 'you text here';
            const content = selected || placeholder;
            return {
              text: `${prefix}${content}${suffix}`,
              selected: content,
            };
          });
        },
      },
      {
        name: 'right',
        text: t('alignRight'),
        action(editor) {
          editor.insert((selected) => {
            const prefix = ':::align-right\n';
            const suffix = '\n:::';
            const placeholder = 'you text here';
            const content = selected || placeholder;
            return {
              text: `${prefix}${content}${suffix}`,
              selected: content,
            };
          });
        },
      },
    ],
  },
});

// 全局
const store = useStore();
const user = computed(() => store.state.user);

// 加载状态
const fullLoading = ref(false);
const loading = ref(false);
const setLoading = (status) => {
  if (status) {
    loading.value = true;
  } else {
    setTimeout(() => {
      loading.value = false;
    }, 600);
  }
};

// 传参
const props = defineProps({
  docId: {
    type: String,
    default: '',
  },
});

// dialog
const commentDialog = ref({
  visible: false,
  content: '',
  reply_to: null,
  id: null,
  method: 'add',
});
const submitComment = (text) => {
  commentDialog.value.visible = false;
  switch (commentDialog.value.method) {
    case 'add':
      handleNewComment(text, null);
      break;
    case 'reply':
      handleNewComment(text, commentDialog.value.reply_to);
      break;
    case 'edit':
      handleUpdateComment(text, commentDialog.value.id);
      break;
  }
};
const replyComment = (replyTo) => {
  commentDialog.value = {
    visible: true,
    content: '',
    reply_to: replyTo,
    id: null,
    method: 'reply',
  };
};
const editComment = (comment) => {
  commentDialog.value = {
    visible: true,
    content: comment.content,
    reply_to: comment.reply_to,
    id: comment.id,
    method: 'edit',
  };
};

const newContent = ref('');
const doAddNewComment = (text) => {
  handleNewComment(text, null);
};

// 评论
const comments = ref([]);
const commentsPaginator = ref({
  page: 1,
  count: 0,
  size: 10,
});
const handlePageChange = (page) => {
  commentsPaginator.value.page = page;
  loadComments();
};
const loadComments = () => {
  if (typeof props.docId !== 'string' || props.docId.length === 0) {
    return;
  }
  setLoading(true);
  loadCommentAPI(props.docId, commentsPaginator.value.size, commentsPaginator.value.page).then((res) => {
    comments.value = res.data.results;
    commentsPaginator.value.count = res.data.count;
    commentsPaginator.value.page = res.data.page;
  }, (err) => {
    if (err.data.code === 404) {
      handlePageChange(1);
    }
  })
    .finally(() => {
      setLoading(false);
    });
};
watch(() => props.docId, () => {
  loadComments();
});
onMounted(loadComments);

const imgClick = (images, currentIndex) => {
  const imgUrl = images[currentIndex];
  window.open(imgUrl);
};

// 新评论
const handleNewComment = (text, replyTo) => {
  fullLoading.value = true;
  createCommentAPI(props.docId, replyTo, text).then(() => {
    loadComments();
    commentDialog.value.content = '';
    newContent.value = '';
  })
    .finally(() => {
      setTimeout(() => {
        fullLoading.value = false;
      }, 600);
    });
};
const handleUploadImage = (event, insertImage, files) => {
  fullLoading.value = true;
  const form = new FormData();
  form.append('file', files[0]);
  uploadFileAPI('/cos/upload/', form).then((res) => {
    if (res.result) {
      insertImage({
        url: res.data[0].url,
        desc: res.data[0].filename,
        width: 'auto',
        height: 'auto',
      });
    }
  }, (err) => {
    message(err.data.msg, 'error');
  })
    .finally(() => {
      setTimeout(() => {
        fullLoading.value = false;
      }, 600);
    });
};
const handleUpdateComment = (text, id) => {
  fullLoading.value = true;
  updateCommentAPI(id, text).then(() => {
    comments.value = updateLocalContent(id, text, comments.value);
  })
    .finally(() => {
      setTimeout(() => {
        fullLoading.value = false;
      }, 600);
    });
};
const updateLocalContent = (id, text, comments) => {
  for (const i in comments) {
    if (comments[i].id === id) {
      comments[i].content = text;
      break;
    }
    if (comments[i].children.length > 0) {
      comments[i].children = updateLocalContent(id, text, comments[i].children);
    }
  }
  return comments;
};
const showRemoveConfirm = (id) => {
  const message = t('removeCommentConfirm');
  ElMessageBox.alert(
    message,
    t('deleteConfirm'), {
      confirmButtonText: t('deleteConfirmed'),
      callback: (action) => {
        if (action === 'confirm') {
          deleteCommentAPI(id).then(() => {
            loadComments();
          });
        }
      },
    },
  );
};
</script>

<style scoped>
    @import "../assets/Doc.css";
</style>
