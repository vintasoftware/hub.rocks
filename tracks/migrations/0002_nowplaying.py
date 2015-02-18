# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NowPlaying',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('track', models.ForeignKey(to='tracks.Track')),
            ],
            options={
                'verbose_name': 'Now playing',
            },
            bases=(models.Model,),
        ),
    ]
