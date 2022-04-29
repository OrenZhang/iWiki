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

import modules.doc.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Comment",
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
                ("doc_id", models.BigIntegerField(verbose_name="文档id")),
                (
                    "reply_to",
                    models.BigIntegerField(blank=True, null=True, verbose_name="父级评论"),
                ),
                ("content", models.TextField(verbose_name="内容")),
                ("creator", models.CharField(max_length=24, verbose_name="创建人")),
                ("update_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                ("is_deleted", models.BooleanField(default=False, verbose_name="软删除")),
            ],
            options={
                "verbose_name": "评论",
                "verbose_name_plural": "评论",
                "db_table": "doc_comment",
            },
        ),
        migrations.CreateModel(
            name="CommentVersion",
            fields=[
                ("doc_id", models.BigIntegerField(verbose_name="文档id")),
                (
                    "reply_to",
                    models.BigIntegerField(blank=True, null=True, verbose_name="父级评论"),
                ),
                ("content", models.TextField(verbose_name="内容")),
                ("creator", models.CharField(max_length=24, verbose_name="创建人")),
                ("update_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                ("is_deleted", models.BooleanField(default=False, verbose_name="软删除")),
                (
                    "version_id",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="版本id"
                    ),
                ),
                ("id", models.BigIntegerField(verbose_name="id")),
            ],
            options={
                "verbose_name": "评论版本",
                "verbose_name_plural": "评论版本",
                "db_table": "doc_comment_version",
            },
        ),
        migrations.CreateModel(
            name="Doc",
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
                ("repo_id", models.BigIntegerField(verbose_name="仓库id")),
                (
                    "available",
                    models.CharField(
                        choices=[("public", "公开"), ("private", "私有")],
                        default="public",
                        max_length=12,
                        verbose_name="可见范围",
                    ),
                ),
                ("title", models.CharField(max_length=64, verbose_name="标题")),
                ("content", models.TextField(blank=True, null=True, verbose_name="内容")),
                (
                    "attachments",
                    models.JSONField(
                        default=modules.doc.models.attachments_default,
                        verbose_name="附件",
                    ),
                ),
                ("creator", models.CharField(max_length=24, verbose_name="创建人")),
                ("update_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                ("is_publish", models.BooleanField(default=True, verbose_name="发布状态")),
                ("is_deleted", models.BooleanField(default=False, verbose_name="软删除")),
            ],
            options={
                "verbose_name": "文档",
                "verbose_name_plural": "文档",
                "db_table": "doc_doc",
            },
        ),
        migrations.CreateModel(
            name="DocVersion",
            fields=[
                ("repo_id", models.BigIntegerField(verbose_name="仓库id")),
                (
                    "available",
                    models.CharField(
                        choices=[("public", "公开"), ("private", "私有")],
                        default="public",
                        max_length=12,
                        verbose_name="可见范围",
                    ),
                ),
                ("title", models.CharField(max_length=64, verbose_name="标题")),
                ("content", models.TextField(blank=True, null=True, verbose_name="内容")),
                (
                    "attachments",
                    models.JSONField(
                        default=modules.doc.models.attachments_default,
                        verbose_name="附件",
                    ),
                ),
                ("creator", models.CharField(max_length=24, verbose_name="创建人")),
                ("update_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                ("is_publish", models.BooleanField(default=True, verbose_name="发布状态")),
                ("is_deleted", models.BooleanField(default=False, verbose_name="软删除")),
                (
                    "version_id",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="版本id"
                    ),
                ),
                ("id", models.BigIntegerField(verbose_name="id")),
            ],
            options={
                "verbose_name": "文档版本",
                "verbose_name_plural": "文档",
                "db_table": "doc_version",
            },
        ),
    ]
