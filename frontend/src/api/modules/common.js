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

export const changeLangAPI = langCode => new Promise((resolve, reject) => {
  http.post(
    '/i18n/',
    {
      language: langCode,
    },
  ).then(res => resolve(res), err => reject(err));
});

export const getConfAPI = key => new Promise((resolve, reject) => {
  http.get(`/conf/common/${key}/`).then(res => resolve(res), err => reject(err));
});

export const uploadFileAPI = (url, data) => new Promise((resolve, reject) => {
  http({
    url,
    method: 'POST',
    headers: { 'Content-Type': 'multipart/form-data' },
    data,
  }).then(res => resolve(res), err => reject(err));
});

export const sendRepassCodeAPI = (username, phone) => new Promise((resolve, reject) => {
  http.post(
    '/sms/send/repass_code/',
    { username, phone },
  ).then(res => resolve(res), err => reject(err));
});

export const sendRegistryCodeAPI = phone => new Promise((resolve, reject) => {
  http.post(
    '/sms/send/register_code/',
    {
      phone,
    },
  ).then(res => resolve(res), err => reject(err));
});

export const loadVersionDataAPI = vid => new Promise((resolve, reject) => {
  http.get(`/version/log/${vid}/`).then(res => resolve(res), err => reject(err));
});

export const listVersionAPI = () => new Promise((resolve, reject) => {
  http.get('/version/log/').then(res => resolve(res), err => reject(err));
});

export const loadIPInfoAPI = () => new Promise((resolve, reject) => {
  http.get('/account/ip_info/').then(res => resolve(res), err => reject(err));
});
