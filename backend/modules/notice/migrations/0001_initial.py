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


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Notice",
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
                ("title", models.CharField(max_length=12, verbose_name="标题")),
                ("content", models.TextField(verbose_name="内容")),
                (
                    "button_text",
                    models.CharField(
                        blank=True, max_length=6, null=True, verbose_name="按钮文本"
                    ),
                ),
                ("url", models.TextField(blank=True, null=True, verbose_name="跳转链接")),
                (
                    "create_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
            ],
            options={
                "verbose_name": "通知",
                "verbose_name_plural": "通知",
                "db_table": "notice_notice",
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="NoticeReadLog",
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
                ("notice_id", models.BigIntegerField(verbose_name="消息ID")),
                ("uid", models.CharField(max_length=24, verbose_name="用户ID")),
                ("is_read", models.BooleanField(default=False, verbose_name="阅读状态")),
                ("read_at", models.DateTimeField(null=True, verbose_name="阅读时间")),
            ],
            options={
                "verbose_name": "通知读取",
                "verbose_name_plural": "通知读取",
                "db_table": "notice_read",
                "ordering": ["-id"],
                "unique_together": {("notice_id", "uid")},
            },
        ),
    ]
