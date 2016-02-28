# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temps', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='batch',
            name='temp_high_c',
        ),
        migrations.RemoveField(
            model_name='batch',
            name='temp_low_c',
        ),
    ]
