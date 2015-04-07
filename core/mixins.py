from django.conf import settings

import django_fanout as fanout


class FanOutMixin(object):
    fanout_channel = None
    fanout_data = None

    def dispatch(self, request, *args, **kwargs):
        response = super(FanOutMixin, self).dispatch(request, *args, **kwargs)

        if (200 <= response.status_code < 300 and
                request.method in ['POST', 'PUT', 'DELETE']):
            if settings.FANOUT_REALM and settings.FANOUT_KEY:
                fanout.publish(self.fanout_channel, self.fanout_data)
            else:
                print ('Sending push to channel {}, '
                       'data {}').format(
                            self.fanout_channel,
                            self.fanout_data)

        return response
