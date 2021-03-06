# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-25 14:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_auto_20170625_1342'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_infor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('pwd', models.CharField(max_length=64)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='user_infor',
            unique_together=set([('name', 'pwd')]),
        ),
    ]
