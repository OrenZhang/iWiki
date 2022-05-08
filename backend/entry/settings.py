# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2021 Oren Zhang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from utils.logs import get_logging_config_dict
from utils.tools import getenv_or_raise

# 目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 环境配置
try:
    with open(
        os.path.join(BASE_DIR, ".env"), "r", encoding="utf-8"
    ) as env_setting_file:
        while True:
            env_setting = env_setting_file.readline()
            if env_setting:
                env_split = env_setting.strip("\n").split("=")
                key = env_split[0]
                val = "=".join(env_split[1:])
                os.environ[key] = val
            else:
                break
except FileNotFoundError:
    pass

# DEBUG
DEBUG = True if os.getenv("DEBUG", "False") == "True" else False
SERVICE_CLOSED = True if os.getenv("SERVICE_CLOSED", "False") == "True" else False

# APP_CODE & SECRET
APP_CODE = getenv_or_raise("APP_CODE")
SECRET_KEY = getenv_or_raise("APP_SECRET_KEY")
APP_SECRET = SECRET_KEY

# INCV API
INCV_API_DOMAIN = os.getenv("INCV_API_DOMAIN")

# 允许的host
ALLOWED_HOSTS = [getenv_or_raise("BACKEND_HOST")]
CORS_ALLOW_CREDENTIALS = os.getenv("CORS_ALLOW_CREDENTIALS", True)
CORS_ORIGIN_WHITELIST = [getenv_or_raise("FRONTEND_URL")]
CSRF_TRUSTED_ORIGINS = [getenv_or_raise("FRONTEND_URL")]

# APPs
INSTALLED_APPS = [
    "corsheaders",
    "django_duration_log",
    "simpleui",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "modules.conf",
    "modules.log",
    "modules.home",
    "modules.account",
    "modules.repo",
    "modules.doc",
    "modules.cos",
    "modules.sms",
    "modules.i18n",
    "modules.version",
    "modules.notice",
]

# 中间件
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django_duration_log.middlewares.DjangoDurationLogMiddleware",
    "utils.middlewares.CSRFExemptMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "utils.middlewares.SQLDebugMiddleware",
    "utils.middlewares.UnHandleExceptionMiddleware",
]

# 路由
ROOT_URLCONF = "entry.urls"

# 模板
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = "entry.wsgi.application"

# 数据库与缓存
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": getenv_or_raise("DB_NAME"),
        "USER": getenv_or_raise("DB_USER"),
        "PASSWORD": getenv_or_raise("DB_PASSWORD"),
        "HOST": getenv_or_raise("DB_HOST"),
        "PORT": int(getenv_or_raise("DB_PORT")),
        "CHARSET": "utf8mb4",
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
REDIS_HOST = getenv_or_raise("REDIS_HOST")
REDIS_PORT = int(getenv_or_raise("REDIS_PORT"))
REDIS_PASSWORD = getenv_or_raise("REDIS_PASSWORD")
REDIS_DB = int(getenv_or_raise("REDIS_DB"))
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
    }
}

# Celery
CELERY_TIMEZONE = "Asia/Shanghai"
CELERY_ENABLE_UTC = False
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_ACCEPT_CONTENT = [
    "pickle",
    "json",
]
BROKER_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

# 用户认证
ADMIN_USERNAME = "Admin"
AUTH_USER_MODEL = "account.User"
AUTHENTICATION_BACKENDS = [
    "modules.account.backends.ModelBackend",
]
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# 国际化
LANGUAGE_CODE = os.getenv("DEFAULT_LANGUAGE", "zh-Hans")
TIME_ZONE = os.getenv("DEFAULT_TIME_ZONE", "Asia/Shanghai")
USE_I18N = True
USE_L10N = True
USE_TZ = False
LANGUAGES = (
    ("en", _("English")),
    ("zh-hans", _("中文简体")),
)
LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)

# 静态文件
STATIC_URL = "/static/"
# STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Session
SESSION_COOKIE_NAME = os.getenv("SESSION_COOKIE_NAME", f"{APP_CODE}-sessionid")
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7
SESSION_COOKIE_DOMAIN = os.getenv("SESSION_COOKIE_DOMAIN")
AUTH_TOKEN_NAME = os.getenv("AUTH_TOKEN_NAME", f"{APP_CODE}-auth-token")

# 日志
LOG_LEVEL = "INFO"
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOGGING = get_logging_config_dict(LOG_LEVEL, LOG_DIR)
IS_USING_DURATION_LOG = (
    True if os.getenv("IS_USING_DURATION_LOG", "False") == "True" else False
)
DURATION_LOG_ASYNC_SAVE_FUNC = "modules.cel.tasks.create_duration_log"
INFLUXDB_ACCESS_TOKEN = os.getenv("INFLUXDB_ACCESS_TOKEN")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET")
INFLUXDB_URL = os.getenv("INFLUXDB_URL")

# rest_framework
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["utils.renderers.APIRenderer"],
    "DEFAULT_PAGINATION_CLASS": "utils.paginations.NumPagination",
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    "DEFAULT_THROTTLE_RATES": {"loginScope": "5/m", "unAuthSmsSendScope": "1/m"},
    "EXCEPTION_HANDLER": "utils.exceptions.exception_handler",
    "UNAUTHENTICATED_USER": "modules.account.models.CustomAnonymousUser",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "utils.authenticators.SessionAuthenticate",
        "utils.authenticators.AuthTokenAuthenticate",
    ],
}

# tencent cloud
TCLOUD_SECRET_ID = os.getenv("TCLOUD_SECRET_ID")
TCLOUD_SECRET_KEY = os.getenv("TCLOUD_SECRET_KEY")

# sms
SMS_SECRET_ID = TCLOUD_SECRET_ID
SMS_SECRET_KEY = TCLOUD_SECRET_KEY
SMS_PHONE_CODE_TID = os.getenv("SMS_PHONE_CODE_TID")
SMS_PHONE_CODE_EX = 120
SMS_PHONE_CODE_PERIOD = 60
SMS_REPO_EXPORT_FAIL_TID = os.getenv("SMS_REPO_EXPORT_FAIL_TID")
SMS_REPO_EXPORT_SUCCESS_TID = os.getenv("SMS_REPO_EXPORT_SUCCESS_TID")
SMS_REPO_APPLY_TID = os.getenv("SMS_REPO_APPLY_TID")
SMS_REPO_APPLY_RESULT_TID = os.getenv("SMS_REPO_APPLY_RESULT_TID")

# cos
COS_SECRET_ID = TCLOUD_SECRET_ID
COS_SECRET_KEY = TCLOUD_SECRET_KEY
COS_REGION = os.getenv("COS_REGION")
COS_BUCKET = os.getenv("COS_BUCKET")
COS_RANDOM_PATH_LENGTH = 10
COS_DOMAIN = os.getenv("COS_DOMAIN")
COS_MAX_FILE_SIZE = os.getenv("COS_MAX_FILE_SIZE", 120) * 1024 * 1024  # Bytes
COS_MAX_AVATAR_SIZE = os.getenv("COS_MAX_AVATAR_SIZE", 1) * 1024 * 1024  # Bytes

# Admin Site
SIMPLEUI_INDEX = getenv_or_raise("FRONTEND_URL")
SIMPLEUI_HOME_INFO = False
SIMPLEUI_HOME_QUICK = True
SIMPLEUI_HOME_ACTION = False
SIMPLEUI_STATIC_OFFLINE = True
SIMPLEUI_ANALYSIS = False
SIMPLEUI_HOME_TITLE = "iWiki"
SIMPLEUI_LOGO = "https://wiki.incv.net/favicon.ico"
SIMPLEUI_DEFAULT_ICON = True
SIMPLEUI_ICON = {
    "对象存储": "far fa-circle",
    "COS Module": "far fa-circle",
    "上传日志": "fas fa-upload",
    "Upload Log": "fas fa-upload",
    "文库模块": "far fa-folder",
    "Repo Module": "far fa-folder",
    "库": "far fa-folder",
    "Repo": "far fa-folder",
    "库成员": "far fa-user",
    "Repo Member": "far fa-user",
    "文档模块": "far fa-file-alt",
    "Doc Module": "far fa-file-alt",
    "协作成员": "far fa-user",
    "Collaborator": "far fa-user",
    "文档": "far fa-file-alt",
    "Doc": "far fa-file-alt",
    "文档版本": "far fa-file",
    "Doc Version": "far fa-file",
    "置顶文章": "fas fa-book-open",
    "Pin Doc": "fas fa-book-open",
    "评论": "far fa-comment-dots",
    "Comment": "far fa-comment-dots",
    "评论版本": "far fa-comment",
    "Comment Version": "far fa-comment",
    "日志模块": "far fa-bookmark",
    "Log Module": "far fa-bookmark",
    "日志": "far fa-bookmark",
    "Log": "far fa-bookmark",
    "版本模块": "fas fa-code-branch",
    "Version Module": "fas fa-code-branch",
    "版本": "fas fa-code-branch",
    "Version": "fas fa-code-branch",
    "用户模块": "far fa-user",
    "User Module": "far fa-user",
    "成员": "far fa-user",
    "User": "far fa-user",
    "短信模块": "far fa-comment-alt",
    "SMS Module": "far fa-comment-alt",
    "短信": "far fa-comment-alt",
    "SMS": "far fa-comment-alt",
    "配置模块": "fas fa-cog",
    "Conf Module": "fas fa-cog",
    "配置": "fas fa-cog",
    "Conf": "fas fa-cog",
}
SIMPLEUI_CONFIG = {"system_keep": False}

# init
DEFAULT_REPO_NAME = getenv_or_raise("DEFAULT_REPO_NAME")

# opentracing
JAEGER_HOST = os.getenv("JAEGER_HOST", "localhost")
TRACE_PROVIDER = TracerProvider(resource=Resource.create({SERVICE_NAME: APP_CODE}))
JAEGER_EXPORTER = JaegerExporter(agent_host_name=JAEGER_HOST, agent_port=6831)
SPAN_PROCESSOR = BatchSpanProcessor(JAEGER_EXPORTER)
TRACE_PROVIDER.add_span_processor(SPAN_PROCESSOR)
trace.set_tracer_provider(TRACE_PROVIDER)
DjangoInstrumentor().instrument()
