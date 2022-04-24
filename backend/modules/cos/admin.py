from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from modules.cos.models import UploadLog


class UploadETagListFilter(admin.SimpleListFilter):
    title = _("上传结果")
    parameter_name = "etag"

    def lookups(self, request, model_admin):
        return (
            (True, _("上传成功")),
            (False, _("上传失败")),
        )

    def queryset(self, request, queryset):
        if self.value() == "True":
            return queryset.filter(response__ETag__isnull=False)
        if self.value() == "False":
            return queryset.filter(response__ETag__isnull=True)
        return queryset


@admin.register(UploadLog)
class UploadLogAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "path", "etag", "operator_name", "upload_at"]
    search_fields = ["name"]
    list_filter = [UploadETagListFilter]
    ordering = ["-id"]

    @admin.display(description=_("上传结果"), boolean=True)
    def etag(self, obj):
        return True if obj.response.get("ETag", False) else False

    @admin.display(description=_("操作人"))
    def operator_name(self, obj):
        return get_user_model().objects.get(uid=obj.operator).username
