from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from channels.layers import get_channel_layer
import json
import asyncio

from .managers import RecommendationManager
User = get_user_model()


class Recommendation(models.Model):
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='recommendation_for',
        on_delete=models.CASCADE)
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='recommendation_to',
        on_delete=models.CASCADE)

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    timestamp = models.DateTimeField(blank=True, null=True, auto_now=True)

    objects = RecommendationManager()

    def __str__(self):
        return f'''{self.from_user.username} recommends
                    {self.content_object} to
                    {self.to_user.username}'''


@receiver(post_save, sender=Recommendation)
def recommendation_handler(sender, instance, created, **kwargs):
    """
    This module will handle recommendation notification for the current user
    """
    if created:
        channel_layer = get_channel_layer()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        message = {'title': f'''You have received a recommendation
                                from {instance.from_user}''',
                   'instance_id': instance.id}
        loop.run_until_complete(channel_layer.group_send(
            "user_notification",
            {
                'type': 'send_recommendation',
                'message': json.dumps(message),
            }))

        print(message)
