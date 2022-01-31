from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

# from PIL import Image
from jsonfield import JSONField
from user.models import UserActivity
from utils.media_compression import compress_media

User = get_user_model()


class Profile(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=32, null=True)
    about = models.TextField(blank=True)
    image_url = models.URLField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(blank=True, null=True)

    # All these three lists will have two keys, Movie and TVshow
    favoritelist = JSONField(null=True)
    watchlist = JSONField(null=True)
    watchedlist = JSONField(null=True)

    # interest is having three keys in it. Genre, TvSHow/Movie, Actor/Actoress
    interests = JSONField(null=True)

    activities = models.ManyToManyField(
        UserActivity, related_name="my_activities", blank=True)

    class Meta:
        app_label = 'profiling'

    def __str__(self):
        return str(self.user)

    # def save(self, *args, **kwargs):
    #     self.image = compress_media(self.image)
    #     super(Profile, self).save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    This module will create a profile model for a user
    as soon as the user model is created
    """
    if created:
        Profile.objects.create(user=instance, name=instance.username)
