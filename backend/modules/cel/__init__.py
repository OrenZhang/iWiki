from modules.cel.tasks import app as celery_app

__all__ = ("celery_app",)

"""
nohup celery -A modules.cel worker -l INFO -P solo -f ./logs/celery-worker.log &
nohup celery -A modules.cel worker -l INFO -f ./logs/celery-worker.log &
nohup celery -A modules.cel beat -l INFO -f ./logs/celery-beat.log &
"""
