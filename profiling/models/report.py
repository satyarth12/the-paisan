from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import get_user_model
from utils.models import Timestamps
from django.utils.text import slugify

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from profiling.managers import ReportManager

USER = get_user_model()


class ReportCategory(models.Model):

    id = models.SlugField(primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        app_label = 'profiling'

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = slugify(self.name)
        if not self.name.isupper():
            self.name = self.name.upper()
        super(ReportCategory, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.name}'


class Report(Timestamps):
    user = models.ForeignKey(
        USER, on_delete=models.CASCADE, related_name='reported_by')

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField()

    content_object = GenericForeignKey('content_type', 'object_id')

    category = models.ForeignKey(ReportCategory, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=300, blank=True)
    is_resolved = models.BooleanField(default=False)

    objects = ReportManager()

    class Meta:
        app_label = 'profiling'

    def __str__(self) -> str:
        return f'{self.user}'
