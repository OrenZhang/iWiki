from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from modules.repo.models import Repo, RepoUser


@admin.register(Repo)
class RepoAdmin(admin.ModelAdmin):
    list_display = ["name", "r_type", "creator_name", "create_at", "is_deleted"]
    search_fields = ["name"]
    list_filter = ["is_deleted"]

    @admin.display(description=_("创建人"))
    def creator_name(self, obj):
        return get_user_model().objects.get(uid=obj.creator).username


@admin.register(RepoUser)
class RepoUserAdmin(admin.ModelAdmin):
    list_display = ["repo_name", "username", "u_type", "operator_name", "join_at"]
    list_filter = ["u_type"]
    search_fields = ["repo_name", "username"]

    @admin.display(description=_("库名"))
    def repo_name(self, obj):
        return Repo.objects.get(id=obj.repo_id).name

    @admin.display(description=_("用户名"))
    def username(self, obj):
        return get_user_model().objects.get(uid=obj.uid).username

    @admin.display(description=_("处理人"))
    def operator_name(self, obj):
        if obj.operator:
            return get_user_model().objects.get(uid=obj.uid).username
        return "-"

    def get_search_results(self, request, queryset, search_term):
        if not search_term:
            return queryset, False
        repo_ids = Repo.objects.filter(name__icontains=search_term)
        uids = get_user_model().objects.filter(username__icontains=search_term)
        queryset = queryset.filter(Q(repo_id__in=repo_ids) | Q(uid__in=uids))
        return queryset, False
