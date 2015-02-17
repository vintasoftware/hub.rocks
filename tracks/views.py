from django.views import generic


class VoteView(generic.TemplateView):
    template_name = 'tracks/vote.html'
