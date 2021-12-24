import datetime
import json
import logging
import os
import shutil
import time
import traceback
import zipfile

import django
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "entry.settings")
os.environ.setdefault("C_FORCE_ROOT", "True")
django.setup()

from celery import Celery  # noqa
from celery.schedules import crontab  # noqa
from django.core.cache import cache  # noqa
from django.conf import settings  # noqa
from django.db import connection  # noqa

from constents import DocAvailableChoices, UserTypeChoices  # noqa
from modules.account.models import User  # noqa
from modules.doc.models import PinDoc  # noqa
from modules.cel.serializers import StatisticSerializer  # noqa
from modules.doc.models import Doc  # noqa
from modules.repo.models import Repo, RepoUser  # noqa
from utils.client import get_client_by_user  # noqa

app = Celery("main", broker=settings.BROKER_URL)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

logger = logging.getLogger("celery")

# 周期任务
app.conf.beat_schedule = {
    "auto_update_active_index": {
        "task": "modules.cel.tasks.auto_update_active_index",
        "schedule": crontab(minute=0, hour=0),
        "args": (),
    },
    "auto_check_pin_doc": {
        "task": "modules.cel.tasks.auto_check_pin_doc",
        "schedule": crontab(minute="*"),
        "args": (),
    },
    "remind_apply_info": {
        "task": "modules.cel.tasks.remind_apply_info",
        "schedule": crontab(minute=20, hour=17),
        "args": (),
    },
}


@app.task
def auto_update_active_index():
    """自动更新用户活跃度"""
    sql_path = os.path.join(
        settings.BASE_DIR, "modules", "cel", "sql", "auto_update_active_index.sql"
    )
    with connection.cursor() as cursor:
        with open(sql_path) as sql_file:
            cursor.execute(sql_file.read())

    cache.delete("UserInfoView:active_user")

    statistics = User.objects.values("uid", "username", "active_index")
    serializer = StatisticSerializer(statistics, many=True)
    data = serializer.data
    for info in data:
        logger.info(info)


@app.task
def auto_check_pin_doc():
    """自动取消置顶到期的文章"""
    now = datetime.datetime.now()
    PinDoc.objects.filter(in_use=True, pin_to__lt=now).update(
        in_use=False, operator=settings.ADMIN_USERNAME
    )


@app.task
def export_all_docs(repo_id, uid):
    """导出仓库所有文章"""
    client = get_client_by_user(uid)
    # 获取用户和库对象
    user = User.objects.get(uid=uid)
    repo = Repo.objects.get(id=repo_id)
    # 导出文章
    docs = Doc.objects.filter(
        repo_id=repo.id,
        is_deleted=False,
        is_publish=True,
        available=DocAvailableChoices.PUBLIC,
    )
    try:
        file_dir = os.path.join(settings.BASE_DIR, "tmp", uid, str(repo.id))
        if os.path.exists(file_dir):
            shutil.rmtree(file_dir)
        os.makedirs(file_dir)
        for doc in docs:
            filename = "[{}]{}.md".format(
                doc.id, doc.title.replace(" ", "").replace("/", "")
            )
            file_path = os.path.join(file_dir, filename)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(doc.content)
        zip_file_path = "{}.zip".format(
            os.path.join(os.path.dirname(file_dir), repo.name)
        )
        zip_file = zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED)
        for dir_path, dir_names, filenames in os.walk(file_dir):
            f_path = dir_path.replace(file_dir, "")
            f_path = f_path and f_path + os.sep or ""
            for filename in filenames:
                zip_file.write(os.path.join(dir_path, filename), f_path + filename)
        zip_file.close()
        with open(zip_file_path, "rb") as zip_file:
            result, url = client.cos.upload("{}.zip".format(repo.name), zip_file.raw)
        shutil.rmtree(file_dir)
        os.remove(zip_file_path)
        if result:
            logger.info("库 %s 导出上传成功 (%s)", repo.name, url)
        else:
            raise Exception("Upload Error")
        client.sms.send_sms(
            user.phone, settings.SMS_REPO_EXPORT_SUCCESS_TID, [user.username, repo.name]
        )
    except Exception as err:
        logger.error(err, traceback.print_exc())
        client.sms.send_sms(
            user.phone, settings.SMS_REPO_EXPORT_FAIL_TID, [user.username, repo.name]
        )


@app.task
def remind_apply_info():
    """向管理员发送申请通知"""
    sql_path = os.path.join(
        settings.BASE_DIR, "modules", "cel", "sql", "remind_apply_info.sql"
    )
    sql = ""
    with open(sql_path) as sql_file:
        sql = sql_file.read()
    sql = sql.format(
        UserTypeChoices.VISITOR,
        UserTypeChoices.ADMIN,
        UserTypeChoices.OWNER,
    )
    user_model = get_user_model()
    visitor_count = user_model.objects.raw(sql)
    send_kwargs = {}
    for c in visitor_count:
        if c.uid not in send_kwargs.keys():
            send_kwargs[c.uid] = {"repos": [c.name], "count": c.count, "phone": c.phone}
        else:
            send_kwargs[c.uid]["repos"].append(c.name)
            send_kwargs[c.uid]["count"] += c.count
    logger.info("[remind_apply_info] %s", json.dumps(send_kwargs))
    client = get_client_by_user(settings.ADMIN_USERNAME)
    for u in send_kwargs.values():
        client.sms.send_sms(
            u["phone"],
            settings.SMS_REPO_APPLY_TID,
            [" / ".join(u["repos"]), str(u["count"])],
        )
        time.sleep(0.1)
