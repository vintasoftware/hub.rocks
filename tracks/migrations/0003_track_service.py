# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0002_track_played_on_random'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='service',
            field=models.CharField(default=b'deezer', max_length=20, choices=[(b'deezer', b'Deezer'), (b'youtube', b'YouTube')]),
        ),
    ]
