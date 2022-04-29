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

from django.db import migrations, models

import modules.log.models


class Migration(migrations.Migration):

    dependencies = [
        ("log", "0005_delete_log"),
    ]

    operations = [
        migrations.CreateModel(
            name="Log",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "operator",
                    models.CharField(
                        blank=True, max_length=24, null=True, verbose_name="操作人"
                    ),
                ),
                ("path", models.TextField(verbose_name="请求地址")),
                ("code", models.SmallIntegerField(default=200, verbose_name="响应码")),
                (
                    "detail",
                    models.JSONField(
                        default=modules.log.models.get_default_detail,
                        null=True,
                        verbose_name="详细信息",
                    ),
                ),
                ("duration", models.IntegerField(default=0, verbose_name="请求时长(ms)")),
                ("ip", models.GenericIPAddressField(verbose_name="IP地址")),
                (
                    "create_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
            ],
            options={
                "verbose_name": "日志",
                "verbose_name_plural": "日志",
                "db_table": "log_log",
                "ordering": ["-id"],
            },
        ),
    ]
