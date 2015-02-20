from django.conf import settings

from pusher import pusher_from_url

try:
    pusher = pusher_from_url()
except KeyError:
    pusher = None


class PusherMixin(object):
    pusher_channel = None
    pusher_event = None

    def dispatch(self, request, *args, **kwargs):
        response = super(PusherMixin,
            self).dispatch(request, *args, **kwargs)

        if (200 <= response.status_code < 300 and
            request.method in ['POST', 'PUT', 'DELETE']):
            if not settings.LOCAL:
                pusher[self.pusher_channel].trigger(
                    self.pusher_event)
            else:
                print ('Sending push to channel {}, '
                       'event {}').format(
                            self.pusher_channel,
                            self.pusher_event)

        return response
