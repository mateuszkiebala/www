# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-06-05 12:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0018_auto_20160605_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commune',
            name='last_mod_user',
            field=models.CharField(default='admin', max_length=42),
        ),
    ]
