# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-16 13:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20170315_2226'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='description',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
