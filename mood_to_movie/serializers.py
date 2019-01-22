from rest_framework import serializers
from .models import TwitterMessages, MovieRecommendations, MoodToMovie

class MoodToMovieSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'anger',
            'fear',
            'joy',
            'sadness',
            'analytical',
            'confident',
            'tentative',
            'genre_name',
            'genre_id'
        )
        model = MoodToMovie

class MovieRecommendationsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'movie_data'
        )
        model = MovieRecommendations

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'twitter_username',
            'messages',
            'anger',
            'fear',
            'joy',
            'sadness',
            'analytical',
            'confident',
            'tentative'
        )
        model = TwitterMessages