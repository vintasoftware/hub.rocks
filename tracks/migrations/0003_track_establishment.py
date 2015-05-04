# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings



def default_establishment(apps, schema_editor):
    Track = apps.get_model("tracks", "Track")
    User = apps.get_model("auth", 'User')
    try:
        vinta = User.objects.get(username='vinta')
    except User.DoesNotExist:
        vinta = User.objects.create(username='vinta')
        vinta.save()
    for track in Track.objects.all():
        track.establishment = vinta
        track.save()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tracks', '0002_vote_skip_request_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='establishment',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.RunPython(default_establishment),
    ]
