
from rest_framework import serializers

from player.models import PlayerStatus


class PlayerStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerStatus
        fields = ('playing', 'establishment')
