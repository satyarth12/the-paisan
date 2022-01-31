import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from recommendation.models import Recommendation
from rating_review.models.review import Review
import copy


class NotificationConsumer(AsyncWebsocketConsumer):
    """
    Sync functions
    """
    @sync_to_async
    def get_recommendation_to_user(self, id):
        """
        This sync module will get the to_user of the recommendation instance
        """
        instance = Recommendation.objects.get(id=id)
        # print("into get_recommendation_to_user")
        # print(instance.to_user)
        return instance.to_user

    @sync_to_async
    def get_parent_review_user(self, parent_id):
        instance = Review.objects.get(id=parent_id)
        print("into get_parent_review_user")
        print(instance.user)
        return instance.user

    """
    Async functions
    """
    async def connect(self):
        # self.scope['url_route']['kwargs']['room_name']
        self.room_name = 'notification'
        self.room_group_name = 'user_notification'  # % self.room_name

        # Authenticate
        if self.scope["user"].is_anonymous:
            self.disconnect(close_code=401)  # Unauthorized
            return

        print(self.scope["user"])
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(
            f"Because you are unauthenticated. UserStatus: {self.scope['user']}")

    # Receive message from room group

    async def send_announcement(self, event):
        """
        This function is for sending the superuser announcements
        """
        message = json.loads(event['message'])

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))

    async def send_recommendation(self, event):
        """
        This function is for sending the recommendations
        """
        message = json.loads(event['message'])
        new_message = copy.copy(message)
        user = self.scope["user"]
        instance_id = new_message['instance_id']
        to_user = await self.get_recommendation_to_user(instance_id)

        if user == to_user:
            # Send message to WebSocket
            await self.send(text_data=json.dumps(new_message))

    async def send_reviews(self, event):
        """
        This function is for sending the reviews
        """
        message = json.loads(event['message'])
        new_message = copy.copy(message)
        user = self.scope["user"]
        parent_id = new_message['parent_id']
        parent_user = await self.get_parent_review_user(parent_id)

        if user == parent_user:
            # Send message to WebSocket
            await self.send(text_data=json.dumps(message))
