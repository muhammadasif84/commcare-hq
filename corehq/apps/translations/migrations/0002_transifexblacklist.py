# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-01-09 19:35
from __future__ import absolute_import
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('translations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransifexBlacklist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=255)),
                ('app_id', models.CharField(max_length=32)),
                ('module_id', models.CharField(max_length=32)),
                ('field_type', models.CharField(choices=[('detail', 'Case Detail'), ('list', 'Case List')], max_length=100)),
                ('field_name', models.TextField(help_text="\nThis is the same string that appears in the bulk translations download.\nUsually the string in either case list or detail under 'property'.\nThis could be an xpath or case property name.\nIf it is an ID Mapping then the property should be '<property> (ID Mapping Text)'.\nFor the values each value should be '<id mapping value> (ID Mapping Value)'.\nExample: case detail for tasks_type would have entries:\n    tasks_type (ID Mapping Text)\n    child (ID Mapping Value)\n    pregnancy (ID Mapping Value)\n")),
                ('display_text', models.TextField(help_text="The default language's translation for this detail/list. If display_text is not filled out then all translations that match the field_type and field_name will be blacklisted")),
            ],
        ),
    ]
