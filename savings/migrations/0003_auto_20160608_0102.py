# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-08 01:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('savings', '0002_auto_20160606_0151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdraw',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='withdrawn on'),
        ),
    ]