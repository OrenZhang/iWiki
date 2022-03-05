from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from modules.doc.models import Doc
from modules.log.models import DocVisitLog, Log

USER_MODEL = get_user_model()


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ["id", "operator_name", "function", "result", "ip", "create_at"]
    list_filter = ["function", "model"]

    @admin.display(description=_("操作人"))
    def operator_name(self, obj):
        try:
            return USER_MODEL.objects.get(uid=obj.operator).username
        except USER_MODEL.DoesNotExist:
            return None


@admin.register(DocVisitLog)
class DocVisitLogAdmin(admin.ModelAdmin):
    list_display = ["id", "visitor_name", "doc_title", "visit_at"]
    ordering = ["-visit_at"]

    @admin.display(description=_("访问人"))
    def visitor_name(self, obj):
        try:
            return USER_MODEL.objects.get(uid=obj.visitor).username
        except USER_MODEL.DoesNotExist:
            return None

    @admin.display(description=_("文章"))
    def doc_title(self, obj):
        try:
            return Doc.objects.get(id=obj.doc_id).title
        except Doc.DoesNotExist:
            return None
