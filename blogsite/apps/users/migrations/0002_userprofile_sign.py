# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-05-15 01:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='sign',
            field=models.CharField(blank=True, max_length=80, verbose_name='个性签名'),
        ),
    ]