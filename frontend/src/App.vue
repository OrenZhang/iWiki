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
  <el-config-provider :locale="locale">
    <div
      v-if="!screenCheck"
      class="small-screen"
    >
      <div><span style="letter-spacing: 20px">iWik</span>i</div>
      <div style="font-size: 16px; text-align: center;">
        {{ $t('mobileNotice') }}
      </div>
    </div>
    <div
      v-loading="mainLoading"
      v-if="screenCheck"
      class="app-container"
    >
      <transition name="el-fade-in">
        <Login v-if="showLogin" />
      </transition>
      <transition name="el-fade-in">
        <EditUserInfo v-if="showEditUser" />
      </transition>
      <transition name="el-fade-in">
        <VersionLog v-if="showVersion" />
      </transition>
      <el-header
        class="app-header"
        height="61px"
        v-if="!isMobile"
      >
        <div class="el-menu-demo">
          <div class="menu">
            <router-link
              to="/"
              class="header-menu-home"
            >
              <img
                src="/favicon.webp"
                alt="logo.jpg"
                style="width: 32px; height: 32px; margin: 0 10px 0 0;"
              >
              <h2 class="header-menu-home-title">
                iWiki
              </h2>
            </router-link>
            <el-menu
              :default-active="activeIndex"
              :router="true"
              mode="horizontal"
              :ellipsis="false"
            >
              <el-menu-item
                v-for="item in menu"
                v-show="!item.disabled"
                :key="item.index"
                :route="item.route"
                :index="item.index"
              >
                {{ item.name }}
              </el-menu-item>
            </el-menu>
          </div>
          <div class="right-bar">
            <el-link
              v-for="item in navLinks"
              :key="item"
              :underline="false"
              target="_blank"
              :href="item.url"
              class="extra-links"
            >
              <i :class="item.icon" />
            </el-link>
            <el-link
              :underline="false"
              class="notice"
              @click="toggleNotice"
            >
              <i
                class="fa-regular fa-bell"
                :class="hasNoReadNotice ? 'icon-red' : ''"
              />
            </el-link>
            <el-link
              :underline="false"
              class="version"
              @click="showVersionTab"
            >
              <i class="fa-regular fa-question-circle" />
            </el-link>
            <el-link
              :underline="false"
              class="locale"
              @click="toggleLang"
            >
              <i class="fa-solid fa-globe" />
            </el-link>
            <div class="user-login">
              <el-link
                :underline="false"
                type="primary"
                v-show="!user.auth"
                @click="store.commit('setLogin', true)"
              >
                {{ $t('loginLogout') }}
              </el-link>
              <el-link
                :underline="false"
                class="logout-button"
                type="primary"
                v-show="user.auth"
                @click="showLogout"
              >
                <i class="fa-solid fa-user" />
                {{ user.username }}
              </el-link>
            </div>
          </div>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </div>
    <el-drawer
      v-model="noticeVisible"
      direction="rtl"
      custom-class="notice-drawer"
      :size="480"
    >
      <template #title>
        <div style="font-size: 18px; font-weight: bold; display: flex; align-items: center;">
          {{ $t('noticeCenter') }}
          <el-link
            v-if="hasNoReadNotice"
            @click="readAllNotice"
            :underline="false"
            type="primary"
            style="margin-left: 6px;"
          >
            {{ $t('readAllNotice') }}
          </el-link>
        </div>
      </template>
      <template #default>
        <NoticeItem
          v-for="item in notices"
          :key="item.id"
          :data="item"
          @read-notice="readNotice"
        />
        <div
          class="paginator"
          v-if="notices.length > 0"
        >
          <el-pagination
            layout="prev, pager, next"
            :pager-count="5"
            :total="noticePaginator.count"
            :page-size="noticePaginator.size"
            :current-page="noticePaginator.page"
            :hide-on-single-page="true"
            @current-change="handleNoticePageChange"
          />
        </div>
        <el-empty
          v-if="notices.length <= 0"
          :description="$t('noMoreNotice')"
        />
      </template>
    </el-drawer>
  </el-config-provider>
</template>

<script setup>
import Login from './views/Login.vue';
import { computed, onMounted, ref } from 'vue';
import { useStore } from 'vuex';
import { useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';
import zhCn from 'element-plus/es/locale/lang/zh-cn';
import en from 'element-plus/es/locale/lang/en';
import EditUserInfo from './components/EditUserInfo.vue';
import VersionLog from './components/VersionLog.vue';
import { changeLangAPI } from './api/modules/common';
import { isManagerAPI, signOutAPI } from './api/modules/user';
import { getNoticeCommonAPI, readAllNoticeAPI, readNoticeAPI } from './api/modules/notice';
import NoticeItem from './components/NoticeItem.vue';
import { ElMessageBox } from 'element-plus';
import message from './utils/message';

// 国际化
const { t } = useI18n();
const userLocale = ref(localStorage.getItem('locale'));
const locale = computed(() => (userLocale.value === 'en' ? en : zhCn));
const toggleLang = () => {
  if (userLocale.value === 'en') {
    userLocale.value = 'zh';
    localStorage.setItem('locale', 'zh');
    changeBackendLang('zh-Hans');
  } else {
    userLocale.value = 'en';
    localStorage.setItem('locale', 'en');
    changeBackendLang('en');
  }
};
const changeBackendLang  = (langCode) => {
  store.commit('setMainLoading', true);
  changeLangAPI(langCode).finally(() => {
    setTimeout(() => {
      window.location.reload();
    }, 2000);
  });
};

const showVersionTab = () => {
  store.commit('setVersion', true);
};

// 宽度控制
const width = ref(window.innerWidth);
const height = ref(window.innerHeight);
const isMobile = computed(() => width.value < 1000 || height.value < 600);
const screenCheck = computed(() => route.meta.allowMobile || (width.value >= 1000 && height.value >= 600));
onMounted(() => {
  window.addEventListener('resize', () => {
    width.value = window.innerWidth;
    height.value = window.innerHeight;
  });
});

// vuex
const store = useStore();
const user = computed(() => store.state.user);
const mainLoading = computed(() => store.state.mainLoading);
const showLogin = computed(() => store.state.showLogin);
const showEditUser = computed(() => store.state.showEditUser);
const showVersion = computed(() => store.state.showVersion);
const navLinks = computed(() => store.state.navLinks);

// 菜单
const menu = ref([
  {
    name: t('Home'),
    route: {
      name: 'Home',
    },
    index: 'home',
    disabled: false,
  },
  {
    name: t('Repo'),
    route: {
      name: 'Repo',
    },
    index: 'repo',
    disabled: false,
  },
  {
    name: t('User'),
    route: {
      name: 'Self',
    },
    index: 'user',
    disabled: false,
  },
  {
    name: t('New'),
    route: {
      name: 'Publish',
    },
    index: 'publish',
    disabled: false,
  },
  {
    name: t('AdminTab'),
    route: {
      name: 'Admin',
    },
    index: 'admin',
    disabled: computed(() => !isManager.value),
  },
]);

// 管理员检测
const isManager = ref(false);
const checkManager = () => {
  isManagerAPI().then((res) => {
    if (res.result && res.data) {
      isManager.value = true;
    }
  });
};
checkManager();

// 路由匹配
const route = useRoute();
const activeIndex = computed(() => {
  if (route.path === '/') {
    return 'home';
  }
  return route.path.split('/')[1];
});

// 用户信息
onMounted(() => {
  store.dispatch('getUserInfo');
});

// 登录登出
const showLogout = () => {
  const msg = t('logoutConfirm');
  ElMessageBox.alert(msg, t('logout'), {
    confirmButtonText: t('logoutConfirmed'),
    callback: (action) => {
      if (action === 'confirm') {
        doLogout();
      }
    },
  });
};
const doLogout = () => {
  store.commit('setMainLoading', true);
  signOutAPI().then(() => {
    window.location.reload();
  })
    .finally(() => {
      store.dispatch('setMainLoading', false);
    });
};

// 加载页尾信息，导航栏信息
onMounted(() => {
  store.dispatch('getFooterInfo');
  store.dispatch('getNavLinks');
});

// 通知消息
const noticeVisible = ref(false);
const notices = ref([]);
const noticePaginator = ref({
  page: 1,
  count: 0,
  size: 20,
});
const toggleNotice = () => {
  noticeVisible.value = !noticeVisible.value;
};
const hasNoReadNotice = computed(() => {
  for (const notice of notices.value) {
    if (!notice.is_read) {
      return true;
    }
  }
  return false;
});
const loadNotice = () => {
  getNoticeCommonAPI(noticePaginator.value.page, noticePaginator.value.size).then(
    (res) => {
      notices.value = res.data.results;
      noticePaginator.value.count = res.data.count;
    },
    err => message(err.data.msg, 'error'),
  );
};
const readNotice = (id) => {
  readNoticeAPI(id).then(
    () => loadNotice(),
    err => message(err.data.msg, 'error'),
  );
};
const handleNoticePageChange = (page) => {
  noticePaginator.value.page = page;
  loadNotice();
};
const readAllNotice = () => {
  readAllNoticeAPI().then(
    () => {
      noticePaginator.value.page = 1;
      loadNotice();
    },
    err => message(err.data.msg, 'error'),
  );
};
onMounted(loadNotice);
</script>

<style>
    @import "./assets/App.css";
</style>
