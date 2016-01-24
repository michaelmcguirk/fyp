# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CurrentTemp',
            fields=[
                ('temp_id', models.IntegerField(serialize=False, primary_key=True)),
                ('tempc', models.FloatField(null=True, blank=True)),
                ('tempf', models.FloatField(null=True, blank=True)),
                ('timestp', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'current_temp',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Temps',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tempc', models.FloatField(null=True, blank=True)),
                ('tempf', models.FloatField(null=True, blank=True)),
                ('timestp', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'temps',
                'managed': False,
            },
        ),
    ]
