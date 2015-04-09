from rest_framework import serializers

from tracks.models import Track, Vote


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ('track', 'token',)


class TrackSerializer(serializers.ModelSerializer):
    votes = VoteSerializer(many=True)
    voters = serializers.SerializerMethodField()
    skippers = serializers.SerializerMethodField()

    class Meta:
        model = Track
        fields = ('service_id', 'artist', 'title',
                  'votes', 'voters', 'skippers')

    def get_voters(self, track):
        return list(track.votes.values_list('token', flat=True))

    def get_skippers(self, track):
        return [vote.skip_request_by for vote in
                track.votes.exclude(skip_request_by='')]

    def to_representation(self, instance):
        rep = super(TrackSerializer, self).to_representation(instance)
        rep['left_to_skip'] = (len(rep['votes']) + 1 -
                               len(rep['skippers']))
        return rep


class TrackListSerializer(serializers.Serializer):
    tracks = TrackSerializer(many=True)
    now_playing = TrackSerializer()


class TrackUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Track
        fields = ('service_id', 'now_playing')
