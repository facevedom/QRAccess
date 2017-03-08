# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-07 22:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_event_event_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=150)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('security_level', models.IntegerField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Company')),
            ],
        ),
        migrations.AddField(
            model_name='permission',
            name='room',
            field=models.ManyToManyField(to='app.Room'),
        ),
    ]
