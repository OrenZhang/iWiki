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
  <div class="h-100 user-view">
    <el-scrollbar always>
      <div class="head-box" />
      <HUserInfoBox :user-info="userInfo" />
      <div class="content-box">
        <div>
          <el-aside width="120px">
            <el-menu :default-active="activeMenu">
              <el-menu-item
                v-for="item in menu"
                :key="item.index"
                :index="item.index"
                @click="activeMenu = item.index"
              >
                <i :class="item.icon" />
                <span>{{ item.name }}</span>
              </el-menu-item>
            </el-menu>
          </el-aside>
          <el-main>
            <keep-alive>
              <component :is="curComponent" />
            </keep-alive>
          </el-main>
        </div>
      </div>
    </el-scrollbar>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { useStore } from 'vuex';
import HUserInfoBox from '../components/HUserInfoBox.vue';
import DocManage from '../components/DocManage.vue';
import CommentManage from '../components/CommentManage.vue';
import CollectManage from '../components/CollectManage.vue';
import RepoManage from '../components/RepoManage.vue';
import { useI18n } from 'vue-i18n';
import { loginCheckAPI } from '../api/modules/user';
import { setTitle } from '../utils/controller';
import { useRoute } from 'vue-router';

const { t } = useI18n();

const route = useRoute();
const store = useStore();
const userInfo = computed(() => store.state.user);

onMounted(() => {
  setTitle(t('User'));
});

const checkLogin = () => {
  loginCheckAPI().then(() => {}, () => {
    store.commit('setLogin', true);
  });
};
onMounted(checkLogin);

const curComponent = computed(() => {
  switch (activeMenu.value) {
    case 'doc':
      return DocManage;
    case 'repo':
      return RepoManage;
    case 'comment':
      return CommentManage;
    case 'collect':
      return CollectManage;
    default:
      return DocManage;
  }
});
const activeMenu = ref('doc');
const menu = ref([
  {
    index: 'doc',
    name: t('docManage'),
    icon: 'fa-solid fa-copy',
  },
  {
    index: 'collect',
    name: t('collectManage'),
    icon: 'fa-solid fa-star',
  },
  {
    index: 'comment',
    name: t('commentManage'),
    icon: 'fa-solid fa-message',
  },
  {
    index: 'repo',
    name: t('repoManage'),
    icon: 'fa-solid fa-cube',
  },
]);

onMounted(() => {
  if (route.params.hasOwnProperty('tab')) {
    if (route.params.tab) {
      activeMenu.value = route.params.tab;
    }
  }
});
</script>

<style scoped>
    @import "../assets/UserSelf.css";
</style>
