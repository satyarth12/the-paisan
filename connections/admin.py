from django.contrib import admin
from .models import Friends, FriendRequest

admin.site.register(FriendRequest)
admin.site.register(Friends)
