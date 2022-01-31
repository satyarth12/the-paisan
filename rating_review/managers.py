from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class ReviewManager(models.Manager):
    def all(self):
        qs = super(ReviewManager, self).filter(parent=None)
        return qs

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(ReviewManager, self).filter(
            content_type=content_type, object_id=obj_id)  # .filter(parent=None)
        return qs

    def create_by_modeltype(self, model_type, pk, content, user, parent_obj):
        model_qs = ContentType.objects.filter(model=model_type)
        if model_qs.exists():
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(id=pk)

            if not obj_qs.exists() or obj_qs.count() == 1:
                instance = self.model()
                instance.content = content
                instance.content_type = model_qs.first()
                instance.object_id = obj_qs.first().id
                instance.user = user
                if parent_obj:
                    instance.parent = parent_obj
                instance.save()
                return instance
        return None


class RatingManager(models.Manager):
    def all(self):
        qs = super(RatingManager, self).all()
        return qs

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(RatingManager, self).filter(
            content_type=content_type, object_id=obj_id)  # .filter(parent=None)
        return qs

    def create_by_modeltype(self, model_type, pk, stars, user):
        model_qs = ContentType.objects.filter(model=model_type)
        if model_qs.exists():
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(id=pk)

            if not obj_qs.exists() or obj_qs.count() == 1:
                instance = self.model()
                instance.stars = stars
                instance.content_type = model_qs.first()
                instance.object_id = obj_qs.first().id
                instance.user = user

                instance.save()
                return instance
        return None
