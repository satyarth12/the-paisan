from django.urls import re_path

from . import consumers, feed_consumers

websocket_urlpatterns = [
    re_path(r'ws/web-socket/(?P<user_id>\w+)/(?P<room_name>\w+)/$',
            consumers.NotificationConsumer.as_asgi()),
    re_path(r'ws/feed-socket/(?P<user_id>\w+)/(?P<room_name>\w+)/$',
            feed_consumers.TweetConsumer.as_asgi()),
]
