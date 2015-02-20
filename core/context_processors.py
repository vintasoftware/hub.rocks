from pusher import pusher_from_url

try:
    pusher = pusher_from_url()
except KeyError:
    pusher = None


def pusher_api_key(request):
    if pusher:
        return dict(PUSHER_API_KEY=pusher.key)
    else:
        return dict()
