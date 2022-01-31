from django.db import models
from django.contrib.auth import get_user_model


USER = get_user_model()


class Block(models.Model):
    user = models.ForeignKey(
        USER, on_delete=models.CASCADE, related_name='blocked_by')
    blocked_user = models.ForeignKey(
        USER, on_delete=models.CASCADE, related_name='blocked_user')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'profiling'

    @classmethod
    def block_object(cls, blocked_by, blocked_user):
        obj, created = cls.objects.get_or_create(
            user=blocked_by, blocked_user=blocked_user)
        return obj
