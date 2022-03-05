from modules.cel.tasks import create_doc_log, create_log
from utils.tools import get_ip, model_to_dict


class LogHandler:
    def view_log(self, request, view, model, result, instance):
        if hasattr(view, "action"):
            function = f"{view.__class__.__name__}:{view.action}"
        else:
            function = view.__class__.__name__
        create_log.delay(
            request.user.uid,
            model.__name__,
            function,
            result,
            model_to_dict(instance) if instance is not None else {},
            get_ip(request),
        )

    def doc_log(self, instance, visitor):
        create_doc_log.delay(instance.id, visitor)


db_logger = LogHandler()
