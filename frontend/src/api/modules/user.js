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

import http from '../index';

export const getUserInfoAPI = () => new Promise((resolve, reject) => {
  http.get('/account/user_info/').then(res => resolve(res), err => reject(err));
});

export const getExactUserInfoAPI = searchUser => new Promise((resolve, reject) => {
  http.get(`/account/user_info/${searchUser}/`).then(res => resolve(res), err => reject(err));
});

export const isManagerAPI = () => new Promise((resolve, reject) => {
  http.get('/account/user_info/is_manager/').then(res => resolve(res), err => reject(err));
});

export const signOutAPI = () => new Promise((resolve, reject) => {
  http.get('/account/sign_out/').then(res => resolve(res), err => reject(err));
});

export const checkSuperAdminAPI = () => new Promise((resolve, reject) => {
  http.get('/account/user_info/is_superuser/').then(res => resolve(res), err => reject(err));
});

export const searchUserAPI = keyword => new Promise((resolve, reject) => {
  http.post(
    '/account/search/search_user/',
    {
      searchKey: keyword,
    },
  ).then(res => resolve(res), err => reject(err));
});

export const loginCheckAPI = () => new Promise((resolve, reject) => {
  http.get('/account/login_check/').then(res => resolve(res), err => reject(err));
});

export const loadActiveUserAPI = () => new Promise((resolve, reject) => {
  http.get('/account/user_info/active_user/').then(res => resolve(res), err => reject(err));
});

export const repassAPI = (username, password, code, phone) => new Promise((resolve, reject) => {
  http.post(
    '/account/user_info/re_pass/',
    { username, password, code, phone },
  ).then(res => resolve(res), err => reject(err));
});

export const signInAPI = data => new Promise((resolve, reject) => {
  http.post(
    '/account/sign_in/',
    data,
  ).then(res => resolve(res), err => reject(err));
});

export const checkUserNameAPI = username => new Promise((resolve, reject) => {
  http.post(
    '/account/search/check_username/',
    {
      username,
    },
  ).then(res => resolve(res), err => reject(err));
});

export const signUpAPI = data => new Promise((resolve, reject) => {
  http.post(
    '/account/sign_up/',
    data,
  ).then(res => resolve(res), err => reject(err));
});
