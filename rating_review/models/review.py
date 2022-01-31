from __future__ import unicode_literals

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver

from channels.layers import get_channel_layer
import json
import asyncio

from django.contrib.auth import get_user_model
from utils.models import Timestamps

from user.models import UserActivity
from rating_review.managers import ReviewManager

User = get_user_model()


class Review(Timestamps):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()

    objects = ReviewManager()

    class Meta:
        app_label = 'rating_review'
        ordering = ['-id']

    def __str__(self):
        return f'{self.user} comment thread on {self.content_type}-{self.object_id}'

    def children(self):  # replies
        print(self.parent)
        return Review.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True


@receiver(post_save, sender=Review)
def review_handler(sender, instance, created, **kwargs):

    channel_layer = get_channel_layer()
    loop = asyncio.new_event_loop()

    if channel_layer:
        if created and instance.parent:
            asyncio.set_event_loop(loop)

            message = {'title': f'Someone added to your comment thread on media id {instance.content_object}',
                    'parent_id': instance.parent.id}
            loop.run_until_complete(channel_layer.group_send(
                "user_notification",
                {
                    'type': 'send_reviews',
                    'message': json.dumps(message),
                }))

            UserActivity.objects.create_by_modeltype(
                model_type='review', pk=instance.id,
                user=instance.user, action='created_review')

            print(message)

        else:
            UserActivity.objects.create_by_modeltype(
                model_type='review', pk=instance.id,
                user=instance.user, action='created_review')

            print("Created but not a parent")
    
    print("NO CHANNEL LAYER FOUND")
