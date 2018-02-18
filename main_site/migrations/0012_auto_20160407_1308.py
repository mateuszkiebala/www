# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-04-07 13:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0011_auto_20160407_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commune',
            name='distributed_ballots',
            field=models.IntegerField(default=0, null=True, verbose_name='Distributed ballots'),
        ),
        migrations.AlterField(
            model_name='commune',
            name='entitled_inhabitants',
            field=models.IntegerField(default=0, null=True, verbose_name='Entitled inhabitants'),
        ),
        migrations.AlterField(
            model_name='commune',
            name='inhabitants',
            field=models.IntegerField(default=0, null=True, verbose_name='Inhabitants'),
        ),
        migrations.AlterField(
            model_name='commune',
            name='province',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_site.Province', verbose_name='Province'),
        ),
        migrations.AlterField(
            model_name='commune',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_site.CommuneType', verbose_name='Commune type'),
        ),
        migrations.AlterField(
            model_name='commune',
            name='valid_votes',
            field=models.IntegerField(default=0, null=True, verbose_name='Valid votes'),
        ),
        migrations.AlterField(
            model_name='commune',
            name='votes',
            field=models.IntegerField(default=0, null=True, verbose_name='Votes'),
        ),
        migrations.AlterField(
            model_name='voting',
            name='votes',
            field=models.IntegerField(default=0, null=True, verbose_name='Votes'),
        ),
    ]
