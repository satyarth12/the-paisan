from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class RecommendationManager(models.Manager):
    def all(self):
        qs = super(RecommendationManager, self).all()
        return qs

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(RecommendationManager, self).filter(
            content_type=content_type, object_id=obj_id)
        return qs

    def create_by_modeltype(self, model_type, pk, from_user, to_user):
        model_qs = ContentType.objects.filter(model=model_type)

        if model_qs.exists():
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(id=pk)

            if not obj_qs.exists() or obj_qs.count() == 1:

                instance = self.model()
                instance.from_user = from_user
                instance.to_user = to_user
                instance.content_type = model_qs.first()
                instance.object_id = obj_qs.first().id

                instance.save()
                return instance

        return None
