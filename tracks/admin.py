from django.contrib import admin

from tracks.models import Track, Vote


admin.site.register(Track)
admin.site.register(Vote)
