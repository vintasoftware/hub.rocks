from django.views import generic

from braces.views import LoginRequiredMixin, StaffuserRequiredMixin


class PlayerView(LoginRequiredMixin,
                 StaffuserRequiredMixin,
                 generic.TemplateView):
    template_name = 'player/player.html'
    login_url = '/admin/login'

    def get_context_data(self, *args, **kwargs):
        context = super(PlayerView, self).get_context_data(*args, **kwargs)
        context['establishment'] = self.request.user.username
        return context
