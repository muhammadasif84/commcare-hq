# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-11-22 18:53

from django.db import migrations

from corehq.apps.app_manager.management.commands.populate_sql_global_app_config import Command


def _migrate_from_migration(apps, schema_editor):
    sql_class = Command.sql_class()
    sql_class.objects.model._meta.db_table = "app_manager_sqlglobalappconfig"
    Command.migrate_from_migration(apps, schema_editor)
    sql_class.objects.model._meta.db_table = "app_manager_globalappconfig"


class Migration(migrations.Migration):

    dependencies = [
        ('app_manager', '0009_add_sqlglobalappconfig'),
    ]

    operations = [
        migrations.RunPython(_migrate_from_migration,
                             reverse_code=migrations.RunPython.noop,
                             elidable=True),
    ]
