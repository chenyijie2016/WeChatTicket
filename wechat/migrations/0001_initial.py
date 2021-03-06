# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-18 11:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('key', models.CharField(db_index=True, max_length=64)),
                ('description', models.TextField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('place', models.CharField(max_length=256)),
                ('book_start', models.DateTimeField(db_index=True)),
                ('book_end', models.DateTimeField(db_index=True)),
                ('total_tickets', models.IntegerField()),
                ('status', models.IntegerField()),
                ('pic_url', models.CharField(max_length=256)),
                ('remain_tickets', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(db_index=True, max_length=32)),
                ('unique_id', models.CharField(max_length=64, unique=True)),
                ('activity_id', models.IntegerField()),
                ('status', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open_id', models.CharField(db_index=True, max_length=64, unique=True)),
                ('student_id', models.CharField(db_index=True, max_length=32)),
            ],
        ),
    ]
