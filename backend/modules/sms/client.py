import json
import logging

from django.conf import settings
from tencentcloud.common import credential
from tencentcloud.sms.v20210111 import sms_client, models

from modules.sms.models import SMSLog
from utils.tools import model_to_dict

logger = logging.getLogger("sms")


class SMSClient(object):
    def __init__(self, operator):
        self.secretId = settings.SMS_SECRET_ID
        self.secretKey = settings.SMS_SECRET_KEY
        self.app_id = settings.SMS_APP_ID
        self.sign_name = settings.SMS_SIGN_NAME
        self.operator = operator

    def send_sms(
        self, phone_number: str, template_id: str, template_params: list = None
    ):
        # 记录日志
        sms_log = SMSLog.objects.create(
            phone=phone_number,
            template_id=template_id,
            template_params=template_params,
            operator=self.operator,
        )
        try:
            # 实例化要请求产品(sms)的client对象
            cred = credential.Credential(self.secretId, self.secretKey)
            client = sms_client.SmsClient(cred, "ap-guangzhou")

            # 实例化一个请求对象
            req = models.SendSmsRequest()
            req.SmsSdkAppId = self.app_id
            req.SignName = self.sign_name
            req.PhoneNumberSet = [phone_number]
            req.TemplateId = template_id
            req.TemplateParamSet = (
                template_params if template_params is not None else []
            )

            # 发送短信
            resp = client.SendSms(req)
            resp = json.loads(resp.to_json_string(indent=2))

            # 补充日志
            sms_log.send_status = resp

            # 判断发送结果
            if resp["SendStatusSet"][0]["Code"] == "Ok":
                send_flag = True
            else:
                send_flag = False

        except Exception as err:
            sms_log.send_status = err if isinstance(err, dict) else str(err)
            send_flag = False

        sms_log.save()
        logger.info("[sms send] %s", json.dumps(model_to_dict(sms_log)))

        return send_flag
