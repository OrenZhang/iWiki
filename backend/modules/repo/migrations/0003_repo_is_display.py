# Generated by Django 4.0.7 on 2022-09-23 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("repo", "0002_repo_is_allow_apply"),
    ]

    operations = [
        migrations.AddField(
            model_name="repo",
            name="is_display",
            field=models.BooleanField(default=True, verbose_name="展示"),
        ),
    ]
