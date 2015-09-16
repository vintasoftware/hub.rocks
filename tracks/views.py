from django.views import generic


from tracks.mixins import EstablishmentViewMixin
from player.models import PlayerStatus


class VoteView(EstablishmentViewMixin,
               generic.TemplateView):
    template_name = 'tracks/vote.html'

    def get_context_data(self, **kwargs):
        context = super(VoteView, self).get_context_data(**kwargs)
        context['player_status'] = PlayerStatus.objects.get_or_create(
            establishment=self.establishment)[0].playing
        context['can_play_pause'] = self.establishment == self.request.user
        return context
