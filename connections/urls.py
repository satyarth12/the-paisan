from django.urls import path, include
from rest_framework import routers

from .views import FriendRequestViewSet, FriendViewset, FriendActivites

app = 'connections'
router = routers.DefaultRouter()
router.register(r'manage-connections', FriendRequestViewSet,
                basename='manage-connections')

urlpatterns = [

    path('', include(router.urls)),
    path('manage-connections/my-connections/', FriendViewset.as_view()),
    path('manage-connections/activities/', FriendActivites.as_view())
]
