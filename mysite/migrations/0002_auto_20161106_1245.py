# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-06 12:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='question_input',
            new_name='question_text',
        ),
    ]
