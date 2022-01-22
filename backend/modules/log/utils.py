from modules.log.models import Log
from utils.tools import model_to_dict, get_ip


class LogHandler:
    def create_log(
        self,
        operator: str,
        model: str,
        function: str,
        result: bool,
        detail: dict,
        ip: str,
    ):
        Log.objects.create(
            operator=operator,
            model=model,
            function=function,
            result=result,
            detail=detail,
            ip=ip,
        )

    def view_log(self, request, view, model, result, instance):
        if hasattr(view, "action"):
            function = f"{view.__class__.__name__}:{view.action}"
        else:
            function = view.__class__.__name__
        self.create_log(
            request.user.uid,
            model.__name__,
            function,
            result,
            model_to_dict(instance) if instance is not None else {},
            get_ip(request),
        )


db_logger = LogHandler()
