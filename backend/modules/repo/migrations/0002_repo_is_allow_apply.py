# Generated by Django 4.0.4 on 2022-06-06 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("repo", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="repo",
            name="is_allow_apply",
            field=models.BooleanField(default=True, verbose_name="允许申请"),
        ),
    ]
