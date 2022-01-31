from django.contrib import admin
from .models import User, UserActivity

admin.site.register(User)
admin.site.register(UserActivity)
