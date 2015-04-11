from django.views import generic

from braces.views import LoginRequiredMixin, SuperuserRequiredMixin


class VoteView(generic.TemplateView):
    template_name = 'tracks/vote.html'


class PlayerView(LoginRequiredMixin,
                 SuperuserRequiredMixin,
                 generic.TemplateView):
    template_name = 'tracks/player.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PlayerView, self).get_context_data(*args, **kwargs)
        context['establishment'] = self.request.user.username
        return context
