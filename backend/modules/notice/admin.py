from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from modules.notice.models import Notice, NoticeReadLog

USER_MODEL = get_user_model()


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "content", "create_at"]
    search_fields = ["content"]
    list_filter = ["title"]


@admin.register(NoticeReadLog)
class NoticeReadLogAdmin(admin.ModelAdmin):
    list_display = ["id", "notice_id", "notice_title", "receiver", "is_read", "read_at"]
    list_filter = ["is_read"]

    @admin.display(description=_("标题"))
    def notice_title(self, obj: NoticeReadLog):
        try:
            return Notice.objects.get(id=obj.notice_id).title
        except Notice.DoesNotExist:
            return None

    @admin.display(description=_("接受人"))
    def receiver(self, obj: NoticeReadLog):
        try:
            return USER_MODEL.objects.get(uid=obj.uid).username
        except USER_MODEL.DoesNotExist:
            return None
