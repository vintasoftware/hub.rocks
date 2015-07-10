# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0003_track_service'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='track',
            unique_together=set([('service_id', 'establishment', 'service')]),
        ),
    ]
