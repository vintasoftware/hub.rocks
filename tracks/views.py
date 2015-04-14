from django.views import generic


from tracks.mixins import EstablishmentViewMixin


class VoteView(EstablishmentViewMixin,
               generic.TemplateView):
    template_name = 'tracks/vote.html'
