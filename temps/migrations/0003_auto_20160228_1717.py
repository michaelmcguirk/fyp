# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temps', '0002_auto_20160228_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='temp_high_c',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='batch',
            name='temp_low_c',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
