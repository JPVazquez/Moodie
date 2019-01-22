from django.contrib.postgres.fields import JSONField
from django.db import models

# Built in table for converting moods to
# movie genres. To see the actual contents
# of this table, open initial_data.json  within
# cs411_project/mood_to_movie/fixtures/initial_data.json
class MoodToMovie(models.Model):
    anger = models.FloatField(null=False)
    fear = models.FloatField(null=False)
    joy = models.FloatField(null=False)
    sadness = models.FloatField(null=False)
    analytical = models.FloatField(null=False)
    confident = models.FloatField(null=False)
    tentative = models.FloatField(null=False)
    genre_name = models.CharField(max_length=20)
    genre_id = models.IntegerField(null=False)

# Table for storing movie recommendations after
# obtaining tonal analysis and running results
# through MoodToMovie table to obtain conversions

class MovieRecommendations(models.Model):
    movie_data = JSONField()


class TwitterMessages(models.Model):
    fb_username = models.CharField(max_length= 50)
    messages = JSONField()
    anger = models.FloatField(null=False)
    fear = models.FloatField(null=False)
    joy = models.FloatField(null=False)
    sadness = models.FloatField(null=False)
    analytical = models.FloatField(null=False)
    confident = models.FloatField(null=False)
    tentative = models.FloatField(null=False)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.fb_username)

# class LoggedInUser(models.Model): TO IMPLEMENT LATER