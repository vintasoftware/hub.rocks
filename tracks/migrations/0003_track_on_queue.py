# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0002_auto_20150219_1749'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='on_queue',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
