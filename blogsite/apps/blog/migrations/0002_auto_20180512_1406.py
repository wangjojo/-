# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-05-12 14:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.ImageField(blank=True, default='/static/images/blog_default.png', upload_to='images/blog/%Y/%m', verbose_name='封面'),
        ),
    ]
