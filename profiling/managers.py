from __future__ import unicode_literals
from django.contrib.contenttypes.models import ContentType
from django.db import models

from django.conf import settings

USER = settings.AUTH_USER_MODEL


"""
Report model manager
"""


class ReportManager(models.Manager):
    def all(self):
        qs = super(ReportManager, self).all()
        return qs

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(ReportManager, self).filter(
            content_type=content_type, object_id=obj_id
        )  # .filter(parent=None)
        return qs

    def create_by_modeltype(
        self, model_type, model_type_instance_id, user, category, description
    ):
        """
        This module will act as an object label to create a report instance
        """
        model_qs = ContentType.objects.filter(model=model_type)

        if model_qs.exists():
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(id=model_type_instance_id)

            if not obj_qs.exists() or obj_qs.count() == 1:

                instance = self.model()
                instance.user = user
                instance.category = category
                instance.description = description
                instance.content_type = model_qs.first()
                instance.object_id = obj_qs.first().id

                instance.save()
                return instance

        return None
