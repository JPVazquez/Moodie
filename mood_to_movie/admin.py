from django.contrib import admin

# Register your models here.

from .models import MoodToMovie, TwitterMessages, MovieRecommendations

admin.site.register(MoodToMovie)
admin.site.register(TwitterMessages)
admin.site.register(MovieRecommendations)