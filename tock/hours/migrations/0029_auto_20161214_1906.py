# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-15 00:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hours', '0028_auto_20161201_1408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timecardobject',
            name='expense_profit_loss_account',
        ),
        migrations.RemoveField(
            model_name='timecardobject',
            name='grade',
        ),
    ]
