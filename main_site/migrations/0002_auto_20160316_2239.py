# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-16 22:39
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='province',
            name='id',
        ),
        migrations.AddField(
            model_name='province',
            name='nr',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='province',
            name='num_of_distributed_ballots',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='province',
            name='num_of_entitled_inhabitants',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='province',
            name='num_of_inhabitants',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='province',
            name='num_of_valid_votes',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='province',
            name='num_of_votes',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='province',
            name='name',
            field=models.CharField(max_length=42),
        ),
    ]