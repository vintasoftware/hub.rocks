from rest_framework import serializers

from tracks.models import Track, Vote


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ('track', 'token',)


class TrackSerializer(serializers.ModelSerializer):
    votes = VoteSerializer(many=True, read_only=True)
    voters = serializers.SerializerMethodField()
    skippers = serializers.SerializerMethodField()

    class Meta:
        model = Track
        fields = ('id', 'service_id', 'artist', 'title',
                  'votes', 'voters', 'skippers', 'service')
        read_only_fields = ('id', 'artist', 'title')

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

    def create(self, validated_data):
        establishment = self.context['establishment']
        return Track.fetch_and_save_track(
            establishment=establishment, service=validated_data['service'],
            service_id=validated_data['service_id'])


class TrackListSerializer(serializers.Serializer):
    tracks = TrackSerializer(many=True)
    now_playing = TrackSerializer()
