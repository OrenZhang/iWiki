# Generated by Django 4.0.2 on 2022-03-05 21:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("doc", "0012_doc_pv_docversion_pv"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="doc",
            name="pv",
        ),
        migrations.RemoveField(
            model_name="docversion",
            name="pv",
        ),
    ]