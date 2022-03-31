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
