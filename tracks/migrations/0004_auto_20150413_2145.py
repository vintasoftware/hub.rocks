# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0003_track_establishment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='service_id',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='track',
            unique_together=set([('service_id', 'establishment')]),
        ),
    ]
