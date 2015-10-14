from django.views import generic
from django.core.urlresolvers import reverse_lazy


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


class HomeView(generic.RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse_lazy('accounts:login')
