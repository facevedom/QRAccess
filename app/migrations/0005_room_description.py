# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-08 03:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20170307_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='description',
            field=models.CharField(default='No description', max_length=1000),
        ),
    ]
