from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import CustomUserManager, UserActivityManager
# from django.utils.translation import ugettext_lazy as _


from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from .validators import email_validator


class User(AbstractBaseUser):
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(validators=[email_validator],
                              blank=True, null=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    def __str__(self):
        return f'{self.username}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class UserActivity(models.Model):
    user = models.ForeignKey(User, related_name='actor',
                             on_delete=models.CASCADE)

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    action = models.CharField(max_length=100, null=True)
    created_on = models.DateTimeField(auto_now=True)

    objects = UserActivityManager()

    def __str__(self):
        return f'{self.user} - {self.content_object}'
