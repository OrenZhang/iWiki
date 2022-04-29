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

    dependencies = [
        ("doc", "0007_auto_20211211_1551"),
    ]

    operations = [
        migrations.CreateModel(
            name="PinDoc",
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
                ("doc_id", models.BigIntegerField(verbose_name="文章ID")),
                (
                    "create_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                ("pin_to", models.DateTimeField(verbose_name="置顶到期时间")),
                ("operator", models.CharField(max_length=24, verbose_name="操作人")),
                ("in_use", models.BooleanField(default=True, verbose_name="使用中")),
            ],
            options={
                "verbose_name": "置顶文章",
                "verbose_name_plural": "置顶文章",
                "db_table": "doc_pin",
                "ordering": ["-id"],
                "index_together": {("doc_id", "in_use")},
            },
        ),
    ]
