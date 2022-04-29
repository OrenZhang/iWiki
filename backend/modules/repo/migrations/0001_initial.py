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
            name="Repo",
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
                    "name",
                    models.CharField(max_length=24, unique=True, verbose_name="库名"),
                ),
                (
                    "r_type",
                    models.CharField(
                        choices=[("public", "公开"), ("private", "私有")],
                        default="public",
                        max_length=12,
                        verbose_name="类型",
                    ),
                ),
                ("creator", models.CharField(max_length=24, verbose_name="创建人")),
                (
                    "create_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                ("is_deleted", models.BooleanField(default=False, verbose_name="软删除")),
            ],
            options={
                "verbose_name": "库",
                "verbose_name_plural": "库",
                "db_table": "repo_repo",
            },
        ),
        migrations.CreateModel(
            name="RepoUser",
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
                ("repo_id", models.BigIntegerField(verbose_name="库id")),
                ("uid", models.CharField(max_length=24, verbose_name="用户id")),
                (
                    "u_type",
                    models.CharField(
                        choices=[
                            ("owner", "所有者"),
                            ("admin", "管理员"),
                            ("member", "成员"),
                            ("visitor", "访客"),
                        ],
                        db_index=True,
                        default="member",
                        max_length=12,
                        verbose_name="用户类型",
                    ),
                ),
                (
                    "operator",
                    models.CharField(
                        blank=True, max_length=24, null=True, verbose_name="处理人"
                    ),
                ),
                ("join_at", models.DateTimeField(null=True, verbose_name="加入时间")),
            ],
            options={
                "verbose_name": "库成员",
                "verbose_name_plural": "库成员",
                "db_table": "repo_user",
                "unique_together": {("repo_id", "uid")},
                "index_together": {("repo_id", "u_type")},
            },
        ),
    ]
