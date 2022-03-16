from modules.cel.tasks import create_doc_log, create_log
from modules.log.serializers import LogSaveSerializer


class LogHandler:
    def __call__(self, *args, **kwargs):
        serializer = LogSaveSerializer(data=kwargs)
        serializer.is_valid(raise_exception=True)
        create_log.delay(**kwargs)

    def doc_log(self, instance, visitor):
        create_doc_log.delay(instance.id, visitor)


db_logger = LogHandler()
