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

export const getDocCommonAPI = docId => new Promise((resolve, reject) => {
  http.get(`/doc/common/${docId}/`).then(res => resolve(res), err => reject(err));
});

export const loadDocPublicAPI = (size, page) => new Promise((resolve, reject) => {
  http.get(`/doc/public/?size=${size}&page=${page}`).then(res => resolve(res), err => reject(err));
});

export const loadUserDocPublicAPI = (username, page) => new Promise((resolve, reject) => {
  http.get(`/doc/public/user_doc/?username=${username}&page=${page}`).then(res => resolve(res), err => reject(err));
});

export const searchDocAPI = (keywords, page, size) => new Promise((resolve, reject) => {
  http.post(
    `/doc/search/?page=${page}&size=${size}`,
    {
      searchKey: keywords,
    },
  ).then(res => resolve(res), err => reject(err));
});

export const createOrUpdateDocAPI = (url, method, data) => new Promise((resolve, reject) => {
  http({ url, method, data }).then(res => resolve(res), err => reject(err));
});

export const loadDocDataManageAPI = docId => new Promise((resolve, reject) => {
  http.get(`/doc/manage/${docId}/`).then(res => resolve(res), err => reject(err));
});

export const listDocManageAPI = (page, keyword) => new Promise((resolve, reject) => {
  http.get(`/doc/manage/?page=${page}&searchKey=${keyword}`).then(res => resolve(res), err => reject(err));
});

export const loadDocCollaboratorAPI = docId => new Promise((resolve, reject) => {
  http.get(`/doc/manage/${docId}/list_collaborator/`).then(res => resolve(res), err => reject(err));
});

export const removeDocCollaboratorAPI = (docId, uid) => new Promise((resolve, reject) => {
  http.post(
    `/doc/manage/${docId}/remove_collaborator/`,
    { uid },
  ).then(res => resolve(res), err => reject(err));
});

export const addDocCollaboratorAPI = (docId, uid) => new Promise((resolve, reject) => {
  http.post(
    `/doc/manage/${docId}/add_collaborator/`,
    { uid },
  ).then(res => resolve(res), err => reject(err));
});

export const checkDocEditingAPI = docId => new Promise((resolve, reject) => {
  http.get(`/doc/manage/${docId}/edit_status/`).then(res => resolve(res), err => reject(err));
});

export const loadRepoDocAPI = (repoId, keyword, page) => new Promise((resolve, reject) => {
  http.get(`/doc/common/?repo_id=${repoId}&searchKey=${keyword}&page=${page}`).then(res => resolve(res), err => reject(err));
});

export const loadDocChartDataAPI = () => new Promise((resolve, reject) => {
  http.get('/doc/public/recent_chart/').then(res => resolve(res), err => reject(err));
});

export const loadHotRepoAPI = () => new Promise((resolve, reject) => {
  http.get('/repo/public/hot_repo/').then(res => resolve(res), err => reject(err));
});

export const loadRecentDocAPI = () => new Promise((resolve, reject) => {
  http.get('/doc/public/recent/').then(res => resolve(res), err => reject(err));
});

export const loadDocByRepoAdminAPI = (repoId, page, size, keyword) => new Promise((resolve, reject) => {
  http.get(`/repo/manage/${repoId}/load_doc/?page=${page}&size=${size}&searchKey=${keyword}`).then(res => resolve(res), err => reject(err));
});

export const deleteDocAdminAPI = (repoId, docID) => new Promise((resolve, reject) => {
  http({
    url: `/repo/manage/${repoId}/delete_doc/`,
    method: 'DELETE',
    data: { docID },
  }).then(res => resolve(res), err => reject(err));
});

export const changeDocStatusAdminAPI = (docId, data) => new Promise((resolve, reject) => {
  http.patch(
    `/doc/manage/${docId}/`,
    data,
  ).then(res => resolve(res), err => reject(err));
});

export const unPinDocAdminAPI = (repoId, docId) => new Promise((resolve, reject) => {
  http.post(
    `/repo/manage/${repoId}/unpin_doc/`,
    {
      doc_id: docId,
    },
  ).then(res => resolve(res), err => reject(err));
});

export const pinDocAdminAPI = (repoId, data) => new Promise((resolve, reject) => {
  http.post(
    `/repo/manage/${repoId}/pin_doc/`,
    data,
  ).then(res => resolve(res), err => reject(err));
});

export const deleteDocAPI = docId => new Promise((resolve, reject) => {
  http.delete(`/doc/manage/${docId}/`).then(res => resolve(res), err => reject(err));
});

export const checkDocCollaboratorAPI = docId => new Promise((resolve, reject) => {
  http.get(`/doc/common/${docId}/is_collaborator/`).then(res => resolve(res), err => reject(err));
});

export const loadPinDocAPI = repoId => new Promise((resolve, reject) => {
  http.get(`/doc/common/load_pin_doc/?repo_id=${repoId}`).then(res => resolve(res), err => reject(err));
});

export const getDocCollectStatusAPI = docId => new Promise((resolve, reject) => {
  http.get(`/doc/common/${docId}/is_collect/`).then(res => resolve(res), err => reject(err));
});

export const collectDocAPI = docId => new Promise((resolve, reject) => {
  http.post(`/doc/common/${docId}/collect/`).then(res => resolve(res), err => reject(err));
});

export const unCollectDocAPI = docId => new Promise((resolve, reject) => {
  http.post(`/doc/common/${docId}/uncollect/`).then(res => resolve(res), err => reject(err));
});

export const loadCollectDocAPI = (page, searchKey) => new Promise((resolve, reject) => {
  http.get(`/doc/common/collect_list/?page=${page}&size=10&search_key=${searchKey}`).then(res => resolve(res), err => reject(err));
});
