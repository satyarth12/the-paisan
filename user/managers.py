from django.contrib.auth.base_user import BaseUserManager
import uuid
from django.contrib.contenttypes.models import ContentType
from django.db import models

from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError(_('User must have a password'))

        if not password:
            password = str(uuid.uuid4()).replace('-', '')[:9]
            # print(password)

        if not email:
            email = ''
        else:
            email = self.normalize_email(email)

        user = self.model(username=username, email=email)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save()
        return user


class UserActivityManager(models.Manager):
    def all(self):
        qs = super(UserActivityManager, self).all()
        return qs

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(UserActivityManager, self).filter(
            content_type=content_type, object_id=obj_id)
        return qs

    def create_by_modeltype(self, model_type, pk, user, action):
        model_qs = ContentType.objects.filter(model=model_type)

        if model_qs.exists():
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(id=pk)

            if not obj_qs.exists() or obj_qs.count() == 1:

                instance = self.model()
                instance.user = user
                instance.action = action
                instance.content_type = model_qs.first()
                instance.object_id = obj_qs.first().id

                instance.save()
                return instance

        return None
