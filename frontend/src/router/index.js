/*
 * MIT License
 *
 * Copyright (c) 2021 Oren Zhang
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

import * as vueRouter from 'vue-router';
import store from '../store';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
  },
  {
    path: '/publish',
    name: 'Publish',
    component: () => import('../views/Publish.vue'),
  },
  {
    path: '/publish/:id',
    name: 'Edit',
    component: () => import('../views/Publish.vue'),
  },
  {
    path: '/user',
    name: 'Self',
    component: () => import('../views/UserSelf.vue'),
  },
  {
    path: '/user/:username',
    name: 'User',
    component: () => import('../views/User.vue'),
  },
  {
    path: '/doc/:id',
    name: 'Doc',
    component: () => import('../views/Doc.vue'),
    meta: {
      allowMobile: true,
    },
  },
  {
    path: '/m/doc/:id',
    name: 'DocMobile',
    component: () => import('../views/DocMobile.vue'),
    meta: {
      allowMobile: true,
    },
  },
  {
    path: '/repo',
    name: 'Repo',
    component: () => import('../views/Repo.vue'),
  },
  {
    path: '/repo/:id',
    name: 'RepoDetail',
    component: () => import('../views/RepoDetail.vue'),
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('../views/Admin.vue'),
  },
  {
    path: '/:pathMatch(.*)*',
    name: '404',
    component: () => import('../components/ErrorPage.vue'),
  },
];

const router = vueRouter.createRouter({
  history: vueRouter.createWebHistory(),
  routes,
});

router.beforeEach(() => {
  store.dispatch('setMainLoading', true);
});

router.afterEach(() => {
  store.dispatch('setMainLoading', false);
});

export default router;
