# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vote',
            options={'verbose_name': 'Vote'},
        ),
        migrations.AddField(
            model_name='track',
            name='now_playing',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
