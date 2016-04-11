from django.contrib import admin

from tracks.models import Track, Vote


class TrackAdmin(admin.ModelAdmin):
	list_filter = ('establishment',)


admin.site.register(Track, TrackAdmin)
admin.site.register(Vote)
