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

import { createStore } from 'vuex';
import { getUserInfoAPI } from '../api/modules/user';
import { getConfAPI } from '../api/modules/common';

const store = createStore({
  state() {
    return {
      mainLoading: true,
      showLogin: false,
      showEditUser: false,
      showVersion: false,
      user: {
        uid: '',
        username: '',
        avatar: '',
        date_joined: '',
        property: {},
        auth: false,
      },
      footerInfo: {
        copyright: '',
        showFooter: false,
        siteStartup: '',
      },
      navLinks: [],
    };
  },
  mutations: {
    setMainLoading(state, payload) {
      state.mainLoading = payload;
    },
    setUser(state, payload) {
      state.user = payload;
    },
    setEditUser(state, payload) {
      state.showEditUser = payload;
    },
    setLogin(state, payload) {
      state.showLogin = payload;
    },
    setVersion(state, payload) {
      state.showVersion = payload;
    },
    setFooterInfo(state, payload) {
      state.footerInfo = payload;
    },
    setNavLinks(state, payload) {
      state.navLinks = payload;
    },
  },
  actions: {
    setMainLoading({ commit }, payload) {
      if (payload) {
        commit('setMainLoading', true);
      } else {
        setTimeout(() => {
          commit('setMainLoading', false);
        }, 600);
      }
    },
    getUserInfo({ commit, dispatch }) {
      dispatch('setMainLoading', true);
      getUserInfoAPI().then((res) => {
        if (res.result) {
          commit('setUser', {
            uid: res.data.uid,
            username: res.data.username,
            avatar: res.data.avatar,
            property: res.data.property,
            date_joined: res.data.date_joined,
            auth: true,
          });
        } else {
          commit('setUser', {
            uid: res.data.uid,
            username: res.data.username,
            avatar: res.data.avatar,
            property: res.data.property,
            date_joined: res.data.date_joined,
            auth: false,
          });
        }
      })
        .finally(() => {
          dispatch('setMainLoading', false);
        });
    },
    getFooterInfo({ commit }) {
      getConfAPI('footer_info').then((res) => {
        if (res.result) {
          commit('setFooterInfo', res.data);
        }
      });
    },
    getNavLinks({ commit }) {
      getConfAPI('nav_link').then((res) => {
        if (res.result) {
          commit('setNavLinks', res.data);
        }
      });
    },
  },
});

export default store;
