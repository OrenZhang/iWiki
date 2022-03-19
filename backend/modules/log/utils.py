from modules.cel.tasks import create_doc_log


class LogHandler:
    def doc_log(self, instance, visitor):
        create_doc_log.delay(instance.id, visitor)


db_logger = LogHandler()
