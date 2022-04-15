import datetime
import json
import os
import shutil
import time
import traceback
import zipfile

from celery.schedules import crontab
from celery.utils.log import get_task_logger
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import connection
from django_global_log.utils import SaveLogHandler
from incv_client import INCVUnionClient

from constents import ACTIVE_USER_CACHE_KEY, DocAvailableChoices, UserTypeChoices
from modules.account.models import User
from modules.cel import app
from modules.cel.serializers import StatisticSerializer
from modules.doc.models import Doc
from modules.doc.models import PinDoc
from modules.log.models import DocVisitLog
from modules.notice.utils import notice_handler
from modules.repo.models import Repo
from utils.client import get_client_by_user

logger = get_task_logger("cel")

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
        "schedule": crontab(minute=0, hour=10),
        "args": (),
    },
}


@app.task
def auto_update_active_index():
    """自动更新用户活跃度"""
    logger.info("[auto_update_active_index] Start")

    sql_path = os.path.join(
        settings.BASE_DIR, "modules", "cel", "sql", "auto_update_active_index.sql"
    )
    with connection.cursor() as cursor:
        with open(sql_path) as sql_file:
            cursor.execute(sql_file.read())

    cache.delete(ACTIVE_USER_CACHE_KEY)

    statistics = User.objects.values("uid", "username", "active_index")
    serializer = StatisticSerializer(statistics, many=True)
    data = serializer.data
    for info in data:
        logger.info(info)

    logger.info("[auto_update_active_index] End")


@app.task
def auto_check_pin_doc():
    """自动取消置顶到期的文章"""
    logger.info("[auto_check_pin_doc] Start")
    now = datetime.datetime.now()
    PinDoc.objects.filter(in_use=True, pin_to__lt=now).update(
        in_use=False, operator=settings.ADMIN_USERNAME
    )
    logger.info("[auto_check_pin_doc] End")


@app.task
def export_all_docs(repo_id: int, uid: str):
    """导出仓库所有文章"""
    logger.info("[export_all_docs] Start")
    client = get_client_by_user(uid)
    incv_client = INCVUnionClient()
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
        file_dir = os.path.join(settings.BASE_DIR, "tmp", "repo", uid, str(repo.id))
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
        resp = incv_client.tof.sms.send(
            user.phone, settings.SMS_REPO_EXPORT_SUCCESS_TID, [user.username, repo.name]
        )
    except Exception as err:
        logger.error(err, traceback.print_exc())
        resp = incv_client.tof.sms.send(
            user.phone, settings.SMS_REPO_EXPORT_FAIL_TID, [user.username, repo.name]
        )
    logger.info(resp)
    logger.info("[export_all_docs] End")


@app.task
def remind_apply_info():
    """向管理员发送申请通知"""
    logger.info("[remind_apply_info] Start")
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
    client = INCVUnionClient()
    for u in send_kwargs.values():
        resp = client.tof.sms.send(
            u["phone"],
            settings.SMS_REPO_APPLY_TID,
            [" / ".join(u["repos"]), str(u["count"])],
        )
        logger.info(resp)
        time.sleep(10)
    logger.info("[remind_apply_info] End")


@app.task
def send_apply_result(
    operator: str, repo_id: int, apply_user: str, result: bool = True
):
    """管理员处理结果"""
    logger.info("[send_apply_result] Start")
    result_msg = "已通过" if result else "已拒绝"
    user_model = get_user_model()
    try:
        user = user_model.objects.get(uid=apply_user)
        repo = Repo.objects.get(id=repo_id)
    except (user_model.DoesNotExist, Repo.DoesNotExist):
        return
    if user.phone:
        client = INCVUnionClient()
        resp = client.tof.sms.send(
            user.phone, settings.SMS_REPO_APPLY_RESULT_TID, [repo.name, result_msg]
        )
        logger.info(resp)
    logger.info("[send_apply_result] End")


@app.task
def create_log(detail):
    logger.info("[create_log] Start")
    SaveLogHandler(detail)()
    logger.info("[create_log] End")


@app.task
def create_doc_log(doc_id, uid):
    logger.info("[create_doc_log] Start")
    DocVisitLog.objects.create(doc_id=doc_id, visitor=uid)
    logger.info("[create_doc_log] End")


@app.task
def send_notice(receivers, title, content, button_text, url):
    logger.info("[send_notice] Start")
    notice_handler.send(receivers, title, content, button_text, url)
    logger.info("[send_notice] End")
