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

import modules.conf.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Conf",
            fields=[
                (
                    "c_key",
                    models.CharField(
                        max_length=255,
                        primary_key=True,
                        serialize=False,
                        verbose_name="配置项",
                    ),
                ),
                (
                    "c_type",
                    models.SmallIntegerField(
                        choices=[(1, "布尔"), (2, "字典")], default=1, verbose_name="配置类型"
                    ),
                ),
                (
                    "c_val",
                    models.JSONField(
                        blank=True,
                        default=modules.conf.models.get_default_c_val,
                        null=True,
                        verbose_name="配置内容字典",
                    ),
                ),
                ("c_bool", models.BooleanField(default=True, verbose_name="配置内容布尔")),
            ],
            options={
                "verbose_name": "配置",
                "verbose_name_plural": "配置",
                "db_table": "conf_conf",
            },
        ),
    ]
