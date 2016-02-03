# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('temps', '0002_currenttemp_current_batch_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='user_id',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
