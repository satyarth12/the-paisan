from __future__ import unicode_literals

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model

from utils.models import Timestamps
from rating_review.managers import RatingManager

User = get_user_model()


class Rating(Timestamps):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    stars = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])

    objects = RatingManager()

    class Meta:
        app_label = 'rating_review'
        ordering = ['-id']

    def __str__(self):
        return f'{self.user} rating\'s on {self.content_type}-{self.object_id}'
