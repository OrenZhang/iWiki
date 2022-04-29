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


def get_logging_config_dict(log_level: str, log_dir: str):
    log_class = "logging.handlers.RotatingFileHandler"
    logging_format = {
        "format": (
            "%(levelname)s [%(asctime)s] %(pathname)s "
            "%(lineno)d %(funcName)s "
            "\n \t %(message)s \n"
        ),
        "datefmt": "%Y-%m-%d %H:%M:%S",
    }
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": logging_format,
            "simple": {"format": "%(levelname)s %(message)s"},
        },
        "handlers": {
            "null": {"level": "DEBUG", "class": "logging.NullHandler"},
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "simple",
            },
            "root": {
                "class": log_class,
                "formatter": "verbose",
                "filename": os.path.join(log_dir, "django.log"),
                "maxBytes": 1024 * 1024 * 10,
                "backupCount": 5,
                "encoding": "utf8",
            },
            "mysql": {
                "class": log_class,
                "formatter": "verbose",
                "filename": os.path.join(log_dir, "mysql.log"),
                "maxBytes": 1024 * 1024 * 10,
                "backupCount": 5,
                "encoding": "utf8",
            },
            "sms": {
                "class": log_class,
                "formatter": "verbose",
                "filename": os.path.join(log_dir, "sms.log"),
                "maxBytes": 1024 * 1024 * 10,
                "backupCount": 5,
                "encoding": "utf8",
            },
            "cos": {
                "class": log_class,
                "formatter": "verbose",
                "filename": os.path.join(log_dir, "cos.log"),
                "maxBytes": 1024 * 1024 * 10,
                "backupCount": 5,
                "encoding": "utf8",
            },
            "cel": {
                "class": log_class,
                "formatter": "verbose",
                "filename": os.path.join(log_dir, "celery.log"),
                "maxBytes": 1024 * 1024 * 10,
                "backupCount": 5,
                "encoding": "utf8",
            },
            "error": {
                "class": log_class,
                "formatter": "verbose",
                "filename": os.path.join(log_dir, "error.log"),
                "maxBytes": 1024 * 1024 * 10,
                "backupCount": 5,
                "encoding": "utf8",
            },
            "notice": {
                "class": log_class,
                "formatter": "verbose",
                "filename": os.path.join(log_dir, "notice.log"),
                "maxBytes": 1024 * 1024 * 10,
                "backupCount": 5,
                "encoding": "utf8",
            },
        },
        "loggers": {
            "django": {"handlers": ["null"], "level": "INFO", "propagate": True},
            "django.server": {
                "handlers": ["console"],
                "level": log_level,
                "propagate": True,
            },
            "django.request": {
                "handlers": ["root"],
                "level": "ERROR",
                "propagate": True,
            },
            "django.db.backends": {
                "handlers": ["mysql"],
                "level": log_level,
                "propagate": True,
            },
            "root": {"handlers": ["root"], "level": log_level, "propagate": True},
            "app": {"handlers": ["root"], "level": log_level, "propagate": True},
            "mysql": {"handlers": ["mysql"], "level": log_level, "propagate": True},
            "sms": {"handlers": ["sms"], "level": log_level, "propagate": True},
            "cos": {"handlers": ["cos"], "level": log_level, "propagate": True},
            "cel": {"handlers": ["cel"], "level": log_level, "propagate": True},
            "error": {"handlers": ["error"], "level": log_level, "propagate": True},
            "notice": {"handlers": ["notice"], "level": log_level, "propagate": True},
        },
    }
