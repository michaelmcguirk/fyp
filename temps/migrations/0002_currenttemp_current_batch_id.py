# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temps', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='currenttemp',
            name='current_batch_id',
            field=models.ForeignKey(to='temps.Batch', null=True),
        ),
    ]
