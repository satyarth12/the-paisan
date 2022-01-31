import json
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
import json

from django_celery_beat.models import PeriodicTask, CrontabSchedule
# Create your models here.

User = get_user_model()


class Anouncement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    message = models.TextField()
    image = models.ImageField(
        upload_to='announcements/images/', null=True, blank=True)
    broadcast_on = models.DateTimeField()
    sent = models.BooleanField(default=False)

    class Meta:
        ordering = ['-broadcast_on']

    def __str__(self):
        return f'Announcement made on {self.broadcast_on}'


@receiver(post_save, sender=Anouncement)
def notification_handler(sender, instance, created, **kwargs):
    if created:
        schedule, created = CrontabSchedule.objects.get_or_create(
            hour=instance.broadcast_on.hour, minute=instance.broadcast_on.minute, day_of_month=instance.broadcast_on.day, month_of_year=instance.broadcast_on.month)
        task = PeriodicTask.objects.create(crontab=schedule, name="broadcast-announcement-"+str(
            instance.id), task="notifications.tasks.broadcast_announcement", args=json.dumps((instance.id,)))
