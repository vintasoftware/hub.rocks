from rest_framework import serializers

from tracks.models import Vote


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ('track', 'token',)
