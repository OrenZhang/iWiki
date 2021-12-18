"""
Django 4.0
"""

import json
import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _

from utils.logs import get_logging_config_dict
from utils.tools import getenv_or_raise

# 目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 环境配置
try:
    with open(
        os.path.join(BASE_DIR, "entry", "settings.json"), "r", encoding="utf-8"
    ) as env_setting_file:
        env_settings = json.loads(env_setting_file.read())
        for key, val in env_settings.items():
            os.environ[key] = val
except FileNotFoundError:
    pass

# DEBUG
DEBUG = True if os.getenv("DEBUG", "False") == "True" else False

# APP_CODE & SECRET
APP_CODE = getenv_or_raise("APP_CODE")
SECRET_KEY = getenv_or_raise("APP_SECRET_KEY")

# 允许的host
ALLOWED_HOSTS = [getenv_or_raise("BACKEND_HOST")]
CORS_ALLOW_CREDENTIALS = os.getenv("CORS_ALLOW_CREDENTIALS", True)
CORS_ORIGIN_WHITELIST = [getenv_or_raise("FRONTEND_URL")]
CSRF_TRUSTED_ORIGINS = [getenv_or_raise("FRONTEND_URL")]

# APPs
INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "modules.account",
    "modules.sms",
    "modules.repo",
    "modules.doc",
    "modules.cos",
    "modules.i18n",
]

# 中间件
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
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
        "HOST": os.getenv("DB_HOST", "127.0.0.1"),
        "PORT": int(os.getenv("DB_PORT", 3306)),
        "OPTIONS": {"charset": "utf8mb4"},
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
REDIS_DB = int(os.getenv("REDIS_DB", 0))
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

# 日志
LOG_LEVEL = "INFO"
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOGGING = get_logging_config_dict(LOG_LEVEL, LOG_DIR)

# rest_framework
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["utils.renderers.APIRenderer"],
    "DEFAULT_PAGINATION_CLASS": "utils.paginations.NumPagination",
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    "DEFAULT_THROTTLE_RATES": {"loginScope": "5/m", "unAuthSmsSendScope": "1/m"},
    "EXCEPTION_HANDLER": "utils.exceptions.exception_handler",
    "UNAUTHENTICATED_USER": "modules.account.models.CustomAnonymousUser",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "utils.authenticators.LoginAuthenticate",
    ],
}

# tencent cloud
TCLOUD_SECRET_ID = getenv_or_raise("TCLOUD_SECRET_ID")
TCLOUD_SECRET_KEY = getenv_or_raise("TCLOUD_SECRET_KEY")

# sms
SMS_APP_ID = getenv_or_raise("SMS_APP_ID")
SMS_SIGN_NAME = getenv_or_raise("SMS_SIGN_NAME")
SMS_SECRET_ID = TCLOUD_SECRET_ID
SMS_SECRET_KEY = TCLOUD_SECRET_KEY
SMS_PHONE_CODE_TID = getenv_or_raise("SMS_PHONE_CODE_TID")
SMS_PHONE_CODE_EX = 120
SMS_PHONE_CODE_PERIOD = 60
SMS_REPO_EXPORT_FAIL_TID = getenv_or_raise("SMS_REPO_EXPORT_FAIL_TID")
SMS_REPO_EXPORT_SUCCESS_TID = getenv_or_raise("SMS_REPO_EXPORT_SUCCESS_TID")

# cos
COS_SECRET_ID = TCLOUD_SECRET_ID
COS_SECRET_KEY = TCLOUD_SECRET_KEY
COS_REGION = getenv_or_raise("COS_REGION")
COS_BUCKET = getenv_or_raise("COS_BUCKET")
COS_RANDOM_PATH_LENGTH = 10
COS_DOMAIN = getenv_or_raise("COS_DOMAIN")
COS_MAX_FILE_SIZE = os.getenv("COS_MAX_FILE_SIZE", 120) * 1024 * 1024  # Bytes
COS_MAX_AVATAR_SIZE = os.getenv("COS_MAX_AVATAR_SIZE", 2) * 1024 * 1024  # Bytes

# init
DEFAULT_REPO_NAME = getenv_or_raise("DEFAULT_REPO_NAME")
