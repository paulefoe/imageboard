# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-11 19:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0009_auto_20171011_2152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='board',
        ),
        migrations.AddField(
            model_name='post',
            name='board',
            field=models.ManyToManyField(to='board.Board'),
        ),
    ]
