from modules.cel.tasks import create_doc_log
from utils.tools import get_ip


class LogHandler:
    def doc_log(self, instance, request):
        doc_id = instance.id
        uid = request.user.uid
        ip = get_ip(request)
        ua = request.META.get("HTTP_USER_AGENT")
        create_doc_log.delay(doc_id, uid, ip, ua)


db_logger = LogHandler()
