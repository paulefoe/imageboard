# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-27 14:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0006_auto_20170926_1930'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thread',
            name='board',
        ),
    ]
