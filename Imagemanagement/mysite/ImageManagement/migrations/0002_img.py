# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ImageManagement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IMG',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('img', models.ImageField(upload_to='img')),
                ('img_date', models.CharField(max_length=50)),
                ('sex', models.CharField(max_length=250)),
                ('worm_stage', models.CharField(max_length=250)),
                ('name', models.CharField(max_length=20)),
                ('acquisition', models.ForeignKey(to='ImageManagement.Acquisition')),
            ],
        ),
    ]
