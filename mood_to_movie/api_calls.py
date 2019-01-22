from watson_developer_cloud import ToneAnalyzerV3
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.template import loader
from django.conf import settings
import requests
import twitter
import tweepy
import http.client
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from .models import TwitterMessages, MovieRecommendations, MoodToMovie
from .serializers import TweetSerializer, MovieRecommendationsSerializer, MoodToMovieSerializer
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse


class ListTweets(generics.ListCreateAPIView):
    queryset = TwitterMessages.objects.all()
    serializer_class = TweetSerializer

class ListMovieRecommendations(generics.ListCreateAPIView):
    queryset = MovieRecommendations.objects.all()
    serializer_class = MovieRecommendationsSerializer

class ListMoodToMovie(generics.ListCreateAPIView):
    queryset = MoodToMovie.objects.all()
    serializer_class = MoodToMovieSerializer


# Movie Lookup API Call
def movie_recs(genres):
    url = "https://api.themoviedb.org/3/discover/movie"
    payload = {'api_key': 'INSERT KEY HERE', 'sort_by': 'popularity.desc', 'page': '1', 'with_genres': genres}
    response = requests.get(url, params=payload)
    movies = response.json()
    movie_titles = {x['title']:{'description':x['overview'], 'poster':('https://image.tmdb.org/t/p/w500' + x['poster_path'])} for x in movies['results']}
    return movie_titles


# Watson API Call
def tone_data(message):
    tone_analyzer = ToneAnalyzerV3(
        version='2017-10-26',
        iam_apikey='INSERT API KEY HERE',
        url='https://gateway-wdc.watsonplatform.net/tone-analyzer/api'
    )
    text = message
    tone_analysis = tone_analyzer.tone(
        {'text': text},
        'application/json'
    ).get_result()
    tones = tone_analysis["document_tone"]["tones"]
    return tones

@csrf_exempt
def twitter_verify(request):
    auth = tweepy.OAuthHandler('INSERT APP KEY', 'INSERT APP SECRET', 'https://localhost:8000/api/login')
    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print('Error! Failed to get request token.')
    # print(redirect_url)
    request.session['request_token']= auth.request_token
    print(auth.request_token)
    payload = {'redirect_url':redirect_url, "oauth_token":auth.request_token['oauth_token']}
    url = "https://localhost:8000"
    response = JsonResponse(payload)
    # print(response.content)
    return response

@csrf_exempt
def twitter_access(request):
    # Access Token
    # verifier = 'UWFMfAAAAAAA9DBDAAABZ74neKU'
    auth = tweepy.OAuthHandler('INSERT APP KEY', 'INSERT APP SECRET')
    # token = request.session.get('request_token')
    # request.session.delete('request_token')
    # auth.request_token = {'oauth_token': token,
    #                       'oauth_token_secret': verifier}
    # try:
    #     auth.get_access_token(verifier)
    # except tweepy.TweepError:
    #     print('Error! Failed to get access token.')

    auth.set_access_token('INSERT USER ACCESS TOKEN', 'INSERT USER SECRET')
    api = tweepy.API(auth)
    public_tweets = api.user_timeline()
    tweets_to_analyze = '' # String for concatenating all tweets into before sending to to Watson
    for tweet in public_tweets:
        trimmed_text = tweet.text.split()
        if (trimmed_text[0] == "RT"):
            trimmed_text = trimmed_text[2:]
        if ('https://t.co' in trimmed_text[-1]):
            trimmed_text = trimmed_text[0:-1]
        tweets_to_analyze += " " + ' '.join(trimmed_text) + '\n'
    emotions = tone_data(tweets_to_analyze)
    mood_finder = MoodToMovie.objects
    for emotion in emotions:
        if (emotion['tone_id'] == 'anger'):
            mood_finder = mood_finder.filter(anger__gte = round(emotion['score'], 2))
        elif (emotion['tone_id'] == 'fear'):
            mood_finder = mood_finder.filter(fear__gte = round(emotion['score'], 2))
        elif (emotion['tone_id'] == 'joy'):
            mood_finder = mood_finder.filter(joy__gte = round(emotion['score'], 2))
        elif (emotion['tone_id'] == 'sadness'):
            mood_finder = mood_finder.filter(sadness__gte = round(emotion['score'], 2))
        elif (emotion['tone_id'] == 'analytical'):
            mood_finder = mood_finder.filter(analytical__gte = round(emotion['score'], 2))
        elif (emotion['tone_id'] == 'confident'):
            mood_finder = mood_finder.filter(confident__gte = round(emotion['score'], 2))
        elif (emotion['tone_id'] == 'tentative'):
            mood_finder = mood_finder.filter(tentative__gte = round(emotion['score'], 2))
    genre_suggestions = ''
    for moods in mood_finder.all().values():
        if genre_suggestions == ',':
            genre_suggestions = str(moods["genre_id"])
        else:
            genre_suggestions += ', ' + str(moods["genre_id"])
    movie_list = movie_recs(genre_suggestions)
    response = JsonResponse({"movie_list": movie_list})
    return response



