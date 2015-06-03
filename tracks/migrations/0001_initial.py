# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('service_id', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('artist', models.CharField(max_length=255)),
                ('now_playing', models.BooleanField(default=False)),
                ('establishment', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Track',
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('token', models.CharField(max_length=255)),
                ('skip_request_by', models.CharField(default=b'', max_length=255, blank=True)),
                ('track', models.ForeignKey(related_name='votes', to='tracks.Track')),
            ],
            options={
                'verbose_name': 'Vote',
            },
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('track', 'token')]),
        ),
        migrations.AlterUniqueTogether(
            name='track',
            unique_together=set([('service_id', 'establishment')]),
        ),
    ]
