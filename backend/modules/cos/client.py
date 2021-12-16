import datetime
import logging

from django.db import IntegrityError
from django.conf import settings
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

from modules.cos.models import UploadLog
from utils.tools import simple_uniq_id

logger = logging.getLogger("cos")


class COSClient(object):
    def __init__(self, operator):
        self.operator = operator
        self.client = CosS3Client(
            CosConfig(
                Region=settings.COS_REGION,
                SecretId=settings.TCLOUD_SECRET_ID,
                SecretKey=settings.TCLOUD_SECRET_KEY,
            )
        )
        self.bucket = settings.COS_BUCKET

    def upload(self, filename, file):
        # 文件存储位置
        key = "upload/{date_path}/{random_path}".format(
            date_path=datetime.datetime.now().strftime("%Y%m/%d"),
            random_path=simple_uniq_id(settings.COS_RANDOM_PATH_LENGTH),
        )
        full_path = f"{key}/{filename}"
        # 初始化返回参数
        url = None
        result = False
        try:
            # 创建日志
            log = UploadLog.objects.create(
                name=filename, path=key, operator=self.operator
            )
            # 上传文件
            resp = self.client.put_object(Bucket=self.bucket, Key=full_path, Body=file)
            log.response = resp
            log.save()
            url = "{}/{}".format(settings.COS_DOMAIN, full_path)
            result = True
        except IntegrityError:
            return self.upload(filename, file)
        except Exception as err:
            logger.error("Upload File Error", err)
        return result, url
