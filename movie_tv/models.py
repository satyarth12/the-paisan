from django.db import models
from user.models import User


class Movie(models.Model):
    id = models.IntegerField(blank=True, primary_key=True, default=0)
    name = models.CharField(max_length=300, blank=True)

    favorites = models.ManyToManyField(
        User, related_name='user_added_this_in_favs', blank=True)
    watch_list = models.ManyToManyField(
        User, related_name='user_added_in_watch_list', blank=True)
    watched_list = models.ManyToManyField(
        User, related_name='user_added_in_watched_list', blank=True)

    def __str__(self):
        return f'{str(self.id)} - {self.name}'

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(Movie, self).save(*args, **kwargs)


class TV(models.Model):
    id = models.IntegerField(blank=True, primary_key=True, default=0)
    name = models.CharField(max_length=300, blank=True)

    favorites = models.ManyToManyField(
        User, related_name='user_added_tv_in_favs_list', blank=True)
    watch_list = models.ManyToManyField(
        User, related_name='user_added_tv_in_watch_list', blank=True)
    watched_list = models.ManyToManyField(
        User, related_name='user_added_tv_in_watched_list', blank=True)

    def __str__(self):
        return f'{str(self.id)} - {self.name}'

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(TV, self).save(*args, **kwargs)
