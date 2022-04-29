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

export const changeRepoTypeAPI = (repoId, value) => new Promise((resolve, reject) => {
  http.patch(
    `/repo/manage/${repoId}/`,
    {
      r_type: value,
    },
  ).then(res => resolve(res), err => reject(err));
});

export const loadManageRepoAPI = () => new Promise((resolve, reject) => {
  http.get('/repo/manage/load_repo/').then(res => resolve(res), err => reject(err));
});

export const checkOwnerAPI = repoId => new Promise((resolve, reject) => {
  http.get(`/repo/manage/${repoId}/is_owner/`).then(res => resolve(res), err => reject(err));
});

export const deleteRepoAPI = repoId => new Promise((resolve, reject) => {
  http.delete(`/repo/manage/${repoId}/`).then(res => resolve(res), err => reject(err));
});

export const loadRepoAPI = (page = 0, searchKey = '') => {
  const url = page ? `/repo/common/?page=${page}&searchKey=${searchKey}` : '/repo/common/';
  return new Promise((resolve, reject) => {
    http.get(url).then(res => resolve(res), err => reject(err));
  });
};

export const loadRepoDetailAPI = repoId => new Promise((resolve, reject) => {
  http.get(`/repo/common/${repoId}/`).then(res => resolve(res), err => reject(err));
});

export const loadRepoWithUserAPI = (page, keyword) => new Promise((resolve, reject) => {
  http.get(`/repo/common/with_user/?page=${page}&searchKey=${keyword}`).then(res => resolve(res), err => reject(err));
});

export const createRepoAPI = data => new Promise((resolve, reject) => {
  http.post(
    '/repo/manage/',
    data,
  ).then(res => resolve(res), err => reject(err));
});

export const applyForRepoAPI = repoId => new Promise((resolve, reject) => {
  http.post(`/repo/common/${repoId}/apply/`).then(res => resolve(res), err => reject(err));
});

export const applyByDocAPI = docId => new Promise((resolve, reject) => {
  http.post(
    '/repo/common/apply_by_doc/',
    { doc_id: docId },
  ).then(res => resolve(res), err => reject(err));
});

export const exitRepoAPI = repoId => new Promise((resolve, reject) => {
  http.post(`/repo/common/${repoId}/exit/`).then(res => resolve(res), err => reject(err));
});

export const loadRepoUserAdminAPI = (repoId, page, size, keyword) => new Promise((resolve, reject) => {
  http.get(`/repo/manage/${repoId}/load_user/?page=${page}&size=${size}&searchKey=${keyword}`).then(res => resolve(res), err => reject(err));
});

export const removeRepoUserAdminAPI = (repoId, uid) => new Promise((resolve, reject) => {
  http.post(
    `/repo/manage/${repoId}/remove_user/`,
    { uid },
  ).then(res => resolve(res), err => reject(err));
});

export const dealRepoUserApplyAdminAPI = (repoId, status, uid) => new Promise((resolve, reject) => {
  http.post(
    `/repo/manage/${repoId}/deal_apply/`,
    { status, uid },
  ).then(res => resolve(res), err => reject(err));
});

export const changeRepoUserTypeAdminAPI = (repoId, uid, uType) => new Promise((resolve, reject) => {
  http.post(
    `/repo/manage/${repoId}/change_u_type/`,
    { uid, uType },
  ).then(res => resolve(res), err => reject(err));
});
