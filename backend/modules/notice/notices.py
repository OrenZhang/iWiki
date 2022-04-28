import datetime
import logging
import traceback
from functools import wraps

from django.conf import settings
from django.contrib.auth import get_user_model

from constents import UserTypeChoices
from modules.cel.tasks import send_notice
from modules.doc.models import Doc
from modules.repo.models import Repo, RepoUser

logger = logging.getLogger("notice")

USER_MODEL = get_user_model()


def error_wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as err:
            msg = traceback.format_exc()
            logger.error("[%s Failed] %s\n%s", str(func), err, msg)

    return wrapper


class Notice:
    receivers = []
    title = ""
    content = ""
    button_text = None
    url = None

    def __call__(self, *args, **kwargs):
        if not self.validate():
            return
        send_notice.delay(
            self.receivers, self.title, self.content, self.button_text, self.url
        )

    def validate(self):
        validate_params = ["receivers", "title", "content"]
        for item in validate_params:
            value = getattr(self, item, None)
            if not value:
                logger.warning("[Notice Validate Failed] %s is %s", item, value)
                return False
        if self.button_text and not self.url:
            logger.warning(
                "[Notice Validate Failed] button is %s while url is %s",
                self.button_text,
                self.url,
            )
            return False
        return True

    def get_superuser_uids(self):
        return list(
            USER_MODEL.objects.filter(is_superuser=True).values_list("uid", flat=True)
        )

    def format_datetime(self, datetime_obj: datetime.datetime):
        return datetime_obj.strftime("%Y-%m-%d %H:%M:%S")

    def get_repo_admins(self, repo_id):
        return list(
            RepoUser.objects.filter(
                repo_id=repo_id,
                u_type__in=[UserTypeChoices.OWNER, UserTypeChoices.ADMIN],
            ).values_list("uid", flat=True)
        )

    def get_user_url(self, username):
        return "{}/user/{}".format(settings.SIMPLEUI_INDEX, username)

    def get_repo_url(self, repo_id):
        return "{}/repo/{}".format(settings.SIMPLEUI_INDEX, repo_id)

    def get_doc_url(self, doc_id):
        return "{}/doc/{}".format(settings.SIMPLEUI_INDEX, doc_id)


class RegistryNotice(Notice):
    title = "新用户注册"
    content = "用户<a href={url} target='_blank'>{username}</a>注册成功"

    @error_wrapper
    def __init__(self, user: USER_MODEL):
        self.receivers = self.get_superuser_uids()
        self.content = self.content.format(
            url=self.get_user_url(user.username),
            username=user.username,
        )


class DocMigrateNotice(Notice):
    title = "文章迁移"
    content = (
        "用户<a href={url0} target='_blank'>{username0}</a>"
        "在<a href={url_repo} target='_blank'>{repo_name}</a>的所有文章已全部迁移给"
        "<a href={url1} target='_blank'>{username1}</a>"
    )

    @error_wrapper
    def __init__(self, old_uid: str, new_uid: str, repo_id: int):
        self.receivers = [old_uid, new_uid, *self.get_superuser_uids()]
        old_user = USER_MODEL.objects.get(uid=old_uid)
        new_user = USER_MODEL.objects.get(uid=new_uid)
        repo = Repo.objects.get(id=repo_id)
        self.content = self.content.format(
            url0=self.get_user_url(old_user.username),
            username0=old_user.username,
            repo_name=repo.name,
            url_repo=self.get_repo_url(repo.id),
            url1=self.get_user_url(new_user.username),
            username1=new_user.username,
        )


class CollaboratorNotice(Notice):
    title = "协作者变更"
    content = "您已被{method}<a href={doc_url} target='_blank'>《{doc_name}》</a>的协作者"
    button_text = "前往查看"

    @error_wrapper
    def __init__(self, receiver: str, doc: Doc, method: str):
        self.receivers = [receiver]
        self.content = self.content.format(
            method=method,
            doc_name=doc.title,
            doc_url=self.get_doc_url(doc.id),
        )
        self.url = self.get_doc_url(doc.id)


class CommentNotice(Notice):
    title = "评论通知"
    content = "用户<a href={url} target='_blank'>{username}</a>在<a href={doc_url} target='_blank'>《{doc_name}》</a>写了一条评论"
    button_text = "前往查看"

    @error_wrapper
    def __init__(self, operator: USER_MODEL, doc_id: int):
        doc = Doc.objects.get(id=doc_id)
        self.receivers = [doc.creator]
        self.content = self.content.format(
            url=self.get_user_url(operator.username),
            username=operator.username,
            doc_url=self.get_doc_url(doc.id),
            doc_name=doc.title,
        )
        self.url = self.get_doc_url(doc.id)


class RepoApplyResultNotice(Notice):
    title = "申请结果"
    content = "管理员{method}加入{repo_name}的申请"

    @error_wrapper
    def __init__(self, receiver: str, repo_name: str, method: str):
        self.receivers = [receiver]
        self.content = self.content.format(repo_name=repo_name, method=method)


class RemoveRepoUserNotice(Notice):
    title = "移除通知"
    content = "管理员已移除你在{repo_name}的成员身份"

    @error_wrapper
    def __init__(self, receiver: str, repo_name: str):
        self.receivers = [receiver]
        self.content = self.content.format(repo_name=repo_name)


class ChangeUserTypeNotice(Notice):
    title = "身份变更"
    content = "你在{repo_name}的身份已变更为{u_type}"

    @error_wrapper
    def __init__(self, receiver: str, repo_name: str, u_type: str):
        self.receivers = [receiver]
        self.content = self.content.format(
            repo_name=repo_name, u_type=UserTypeChoices.get_name(u_type)
        )


class DocHandlerNotice(Notice):
    title = "文章通知"
    content = "你的文章《{doc_name}》已被管理员{method}"

    @error_wrapper
    def __init__(self, doc_id: int, method: str):
        doc = Doc.objects.get(id=doc_id)
        self.receivers = [doc.creator]
        self.content = self.content.format(doc_name=doc.title, method=method)


class RepoApplyNotice(Notice):
    title = "申请通知"
    content = "用户<a href={url} target='_blank'>{username}</a>正在申请加入<a href={repo_url} target='_blank'>{repo_name}</a>"
    button_text = "前往处理"
    url = "{}/admin".format(settings.SIMPLEUI_INDEX)

    @error_wrapper
    def __init__(self, repo: Repo, uid: str):
        self.receivers = self.get_repo_admins(repo.id)
        user = USER_MODEL.objects.get(uid=uid)
        self.content = self.content.format(
            url=self.get_user_url(user.username),
            username=user.username,
            repo_url=self.get_repo_url(repo.id),
            repo_name=repo.name,
        )


class ExitRepoNotice(Notice):
    title = "退出通知"
    content = "用户<a href={url} target='_blank'>{username}</a>已退出<a href={repo_url} target='_blank'>{repo_name}</a>"

    @error_wrapper
    def __init__(self, repo: Repo, username: str):
        self.receivers = self.get_repo_admins(repo.id)
        self.content = self.content.format(
            url=self.get_user_url(username),
            username=username,
            repo_url=self.get_repo_url(repo.id),
            repo_name=repo.name,
        )


class CollectDocNotice(Notice):
    title = "收藏通知"
    content = (
        "用户<a href={url} target='_blank'>{username}</a>"
        "收藏了你的文章<a href={doc_url} target='_blank'>《{doc_name}》</a>"
    )

    @error_wrapper
    def __init__(self, doc: Doc, username: str):
        self.receivers = [doc.creator]
        self.content = self.content.format(
            url=self.get_user_url(username),
            username=username,
            doc_url=self.get_doc_url(doc.id),
            doc_name=doc.title,
        )
