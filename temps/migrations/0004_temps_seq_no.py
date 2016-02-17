# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temps', '0003_auto_20160202_2121'),
    ]

    operations = [
        migrations.AddField(
            model_name='temps',
            name='seq_no',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
