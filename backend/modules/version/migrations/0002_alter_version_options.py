# Generated by Django 4.0 on 2021-12-24 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("version", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="version",
            options={"verbose_name": "版本", "verbose_name_plural": "版本"},
        ),
    ]