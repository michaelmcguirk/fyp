# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateTimeField(null=True, blank=True)),
                ('end_date', models.DateTimeField(null=True, blank=True)),
                ('batch_name', models.CharField(max_length=100)),
                ('beer_type', models.CharField(max_length=100)),
                ('volume_l', models.FloatField(null=True, blank=True)),
                ('initial_gravity', models.FloatField(null=True, blank=True)),
                ('final_gravity', models.FloatField(null=True, blank=True)),
                ('initial_temp', models.FloatField(null=True, blank=True)),
                ('body_rating', models.IntegerField(null=True, blank=True)),
                ('taste_rating', models.IntegerField(null=True, blank=True)),
                ('notes', models.CharField(max_length=100)),
                ('temp_high_c', models.FloatField(null=True, blank=True)),
                ('temp_low_c', models.FloatField(null=True, blank=True)),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'db_table': 'batch',
            },
        ),
        migrations.CreateModel(
            name='CurrentTemp',
            fields=[
                ('temp_id', models.IntegerField(serialize=False, primary_key=True)),
                ('tempc', models.FloatField(null=True, blank=True)),
                ('tempf', models.FloatField(null=True, blank=True)),
                ('timestp', models.DateTimeField(null=True, blank=True)),
                ('temp_high_c', models.FloatField(null=True, blank=True)),
                ('temp_low_c', models.FloatField(null=True, blank=True)),
                ('current_batch_id', models.ForeignKey(to='temps.Batch', null=True)),
            ],
            options={
                'db_table': 'current_temp',
            },
        ),
        migrations.CreateModel(
            name='Temps',
            fields=[
                ('temp_id', models.AutoField(serialize=False, primary_key=True)),
                ('tempc', models.FloatField(null=True, blank=True)),
                ('tempf', models.FloatField(null=True, blank=True)),
                ('timestp', models.DateTimeField(null=True, blank=True)),
                ('seq_no', models.IntegerField(null=True, blank=True)),
                ('batch_id', models.ForeignKey(to='temps.Batch', null=True)),
            ],
            options={
                'ordering': ['timestp'],
                'db_table': 'temps',
            },
        ),
        migrations.CreateModel(
            name='UserBatchSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('def_temp_low', models.FloatField(null=True, blank=True)),
                ('def_temp_high', models.FloatField(null=True, blank=True)),
                ('def_temp_format', models.CharField(default='C', max_length=1, choices=[('C', 'Celsius'), ('F', 'Faranheit')])),
                ('user_id', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_batch_settings',
            },
        ),
    ]
