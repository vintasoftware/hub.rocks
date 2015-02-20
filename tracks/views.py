from django.views import generic

from braces.views import LoginRequiredMixin, SuperuserRequiredMixin


class VoteView(generic.TemplateView):
    template_name = 'tracks/vote.html'


class PlayerView(LoginRequiredMixin,
                 SuperuserRequiredMixin,
                 generic.TemplateView):
    template_name = 'tracks/player.html'
