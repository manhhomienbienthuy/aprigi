# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-06 01:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Withdraw',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='amount')),
                ('date', models.DateField(auto_now_add=True, verbose_name='withdrawn on')),
                ('is_open', models.BooleanField(db_index=True, default=True, verbose_name='is open')),
            ],
            options={
                'verbose_name': 'Withdraw',
                'verbose_name_plural': 'Withdraws',
            },
        ),
        migrations.AlterModelOptions(
            name='passbook',
            options={'verbose_name': 'Passbook', 'verbose_name_plural': 'Passbooks'},
        ),
    ]