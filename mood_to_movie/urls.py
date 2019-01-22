# from django.conf.urls import url, include
from . import api_calls
from django.urls import path
from django.conf.urls import url, include


LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'home'

urlpatterns = [
    path('api/lead/', api_calls.ListTweets.as_view()),
    path('api/login', api_calls.twitter_verify),
    path('api/logged_in', api_calls.twitter_access),
]