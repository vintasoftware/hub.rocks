from django.db import models
from django.conf import settings

from model_utils.models import TimeStampedModel
from model_utils import FieldTracker


class PlayerStatus(TimeStampedModel):
    playing = models.BooleanField(default=False)
    establishment = models.OneToOneField(settings.AUTH_USER_MODEL,
                                         related_name='player_status')

    playing_tracker = FieldTracker(fields=['playing'])

from player.signal_receivers import *
