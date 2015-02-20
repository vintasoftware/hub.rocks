from rest_framework import serializers

from tracks.models import Track, Vote


class TrackSerializer(serializers.ModelSerializer):
    votes = serializers.SerializerMethodField('_votes')

    class Meta:
        model = Track
        fields = ('service_id', 'artist', 'title',
                  'votes')

    def _votes(self, track):
        return track.votes.values_list('token', flat=True)


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ('track', 'token',)


class TrackUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Track
        fields = ('service_id', 'now_playing')
