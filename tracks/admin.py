from django.contrib import admin

from tracks.models import Track, Vote, NowPlaying


admin.site.register(Track)
admin.site.register(Vote)
admin.site.register(NowPlaying)
