# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2021 Oren Zhang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from typing import List

from django.db import transaction

from modules.notice.models import NoticeReadLog
from modules.notice.serializers import NoticeSerializer


class NoticeHandler:
    @transaction.atomic()
    def send(
        self,
        receivers: List[str],
        title: str,
        content: str,
        button_text: str = None,
        url: str = None,
    ):
        receivers = list(set(receivers))
        serializer = NoticeSerializer(
            data={
                "title": title,
                "content": content,
                "button_text": button_text,
                "url": url,
            }
        )
        serializer.is_valid(raise_exception=True)
        notice = serializer.save()
        receiver_notices = [
            NoticeReadLog(uid=receiver, notice_id=notice.id) for receiver in receivers
        ]
        NoticeReadLog.objects.bulk_create(receiver_notices)


notice_handler = NoticeHandler()
