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
  <div class="login-container">
    <div class="login-box">
      <el-aside width="400px">
        <div style="width: 100%; height: 100%; overflow: hidden;" />
      </el-aside>
      <el-main style="width:100%">
        <el-header>
          <el-link
            :class="{ 'el-link--primary': curTab === 'sign-in' }"
            @click="changeCurTab('sign-in')"
          >
            {{ $t('login') }}
          </el-link>
          <span class="mg-20-left-right">/</span>
          <el-link
            :class="{ 'el-link--primary': curTab === 'sign-up' }"
            @click="changeCurTab('sign-up')"
          >
            {{ $t('signup') }}
          </el-link>
        </el-header>
        <el-main>
          <component :is="curComponent" />
        </el-main>
        <el-divider style="margin: 0 0 10px 0" />
        <el-footer>
          <el-link @click="store.commit('setLogin', false)">
            {{ $t('exitLogin') }}
          </el-link>
          <el-link
            class="edit-user"
            v-show="curTab === 'sign-in'"
            @click="showEdit"
          >
            {{ $t('updatePassword') }}
          </el-link>
        </el-footer>
      </el-main>
    </div>
  </div>
</template>

<script setup>
import LoginForm from '../components/LoginForm.vue';
import RegisterForm from '../components/RegisterForm.vue';
import { computed, ref } from 'vue';
import { useStore } from 'vuex';

const store = useStore();

// 标签
const curTab = ref('sign-in');
const changeCurTab = (tab) => {
  curTab.value = tab;
};

// 组件
const curComponent = computed(() => {
  switch (curTab.value) {
    case 'sign-in':
      return LoginForm;
    case 'sign-up':
      return RegisterForm;
    default:
      return LoginForm;
  }
});

const showEdit = () => {
  store.commit('setLogin', false);
  store.commit('setEditUser', true);
};
</script>

<style scoped>
    @import "../assets/Login.css";
</style>
