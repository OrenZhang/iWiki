import datetime
import os
import random
import time
import uuid
from itertools import chain

from django.conf import settings
from django.core.cache import cache


def uniq_id():
    uniq = uuid.uuid3(uuid.uuid1(), uuid.uuid4().hex).hex
    return "%s%s" % (str(int(time.time() * 1000)), str(uniq))


def get_auth_token(uid: str):
    uniq = f"{uniq_id()}{uid}"
    in_use = cache.get(uniq)
    if in_use is None:
        cache.set(uniq, uid, settings.SESSION_COOKIE_AGE)
        return uniq
    return get_auth_token(uid)


def simple_uniq_id(length: int):
    base = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
    random.seed(uniq_id())
    uniq = ""
    for i in range(length):
        uniq += base[random.randint(0, len(base) - 1)]
    return uniq


def num_code(length: int):
    random.seed(uniq_id())
    uniq = ""
    for i in range(length):
        uniq += str(random.randint(0, 9))
    return uniq


def get_ip(request):
    if request.META.get("HTTP_X_REAL_IP"):
        return request.META.get("HTTP_X_REAL_IP")
    if request.META.get("HTTP_X_FORWARDED_FOR"):
        return request.META.get("HTTP_X_FORWARDED_FOR").replace(" ", "").split(",")[0]
    if request.META.get("HTTP_X_FORWARD_FOR"):
        return request.META.get("HTTP_X_FORWARD_FOR").replace(" ", "").split(",")[0]
    return request.META.get("REMOTE_ADDR")


def field_handler(data):
    if isinstance(data, datetime.datetime):
        return data.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(data, datetime.date):
        return data.strftime("%Y-%m-%d")
    else:
        return data


def model_to_dict(instance, fields=None, exclude=None):
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        if fields is not None and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        data[f.name] = field_handler(f.value_from_object(instance))
    return data


def getenv_or_raise(key: str):
    val = os.getenv(key)
    if val is None:
        raise Exception(f"Env Not Set, Key [{key}]")
    return val
