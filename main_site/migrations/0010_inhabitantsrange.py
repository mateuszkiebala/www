# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-04-05 14:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0009_auto_20160405_1403'),
    ]

    operations = [
        migrations.CreateModel(
            name='InhabitantsRange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('begin', models.IntegerField(default=0)),
                ('end', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=42)),
            ],
        ),
    ]
