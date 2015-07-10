from django.conf import settings


def fanout_realm(request):
    if settings.FANOUT_REALM:
        return dict(FANOUT_REALM=settings.FANOUT_REALM)
    else:
        return dict()


def youtube_key(request):
    if settings.YOUTUBE_KEY:
        return dict(YOUTUBE_KEY=settings.YOUTUBE_KEY)
    else:
        return dict()
