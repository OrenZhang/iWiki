# Generated by Django 3.2.9 on 2021-11-30 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("doc", "0002_alter_doc_repo_id"),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name="doc",
            index_together={("repo_id", "creator")},
        ),
    ]
