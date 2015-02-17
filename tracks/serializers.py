from rest_framework import serializers

from tracks.models import Vote
from tracks.token import get_token


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ('track', 'token',)

    def validate_token(self):
        return get_token(self.context['request'])

    def validate_track(self):
        return self.context['view'].kwargs['service_id']
