import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from player.models import PlayerStatus

import django_fanout


@receiver(post_save, sender=PlayerStatus)
def broadcast_status_changed(sender, instance, created, **kwargs):
    if created:
        return
    if instance.playing_tracker.changed():
        channel = 'player-status-{}'.format(instance.establishment)
        data = {'playing': instance.playing}
        if settings.FANOUT_REALM and settings.FANOUT_KEY:
            django_fanout.publish(channel, data)
        else:
            logging.info("Fanout not setup, would push {} to /{}".format(
                data, channel))
