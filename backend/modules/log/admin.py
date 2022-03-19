from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from modules.doc.models import Doc
from modules.log.models import DocVisitLog

USER_MODEL = get_user_model()


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
