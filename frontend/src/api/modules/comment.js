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

export const loadCommentAPI = (docId, size, page) => new Promise((resolve, reject) => {
  http.get(`/doc/comments/?doc_id=${docId}&size=${size}&page=${page}`).then(res => resolve(res), err => reject(err));
});

export const createCommentAPI = (docId, replyTo, content) => new Promise((resolve, reject) => {
  http.post(
    '/doc/comment/',
    { doc_id: docId, reply_to: replyTo, content },
  ).then(res => resolve(res), err => reject(err));
});

export const updateCommentAPI = (id, text) => new Promise((resolve, reject) => {
  http.patch(
    `/doc/comment/${id}/`,
    {
      content: text,
    },
  ).then(res => resolve(res), err => reject(err));
});

export const deleteCommentAPI = id => new Promise((resolve, reject) => {
  http.delete(`/doc/comment/${id}/`).then(res => resolve(res), err => reject(err));
});

export const loadUserCommentAPI = (page, size, searchKey) => new Promise((resolve, reject) => {
  http.get(`/doc/comment/all/?page=${page}&size=${size}&search_key=${searchKey}`).then(res => resolve(res), err => reject(err));
});
