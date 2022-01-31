import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import copy

from profiling.models.profile import Profile
from django_celery_beat.models import PeriodicTask, IntervalSchedule


class TweetConsumer(AsyncWebsocketConsumer):

    @sync_to_async
    def select_user_interests(self):
        user = self.scope["user"]
        profile = Profile.objects.get(user=user)
        interest_dict = profile.interests
        user_interests = []

        for key, value in interest_dict.items():
            user_interests = user_interests+value
        return user_interests

    @sync_to_async
    def add_celery_beat(self):
        # every 10 minutes
        task = PeriodicTask.objects.filter(name="every-15-seconds")

        user = self.scope["user"]
        profile = Profile.objects.get(user=user)
        interest_dict = profile.interests
        interests = []
        for key, value in interest_dict.items():
            interests = interests+value
        print('ALL INTERESTS ARE: ', interests)

        # this if statement is to check if the stock is already present
        # in the celery task list or not to reduce the unrequired API calls
        if len(task) > 0:
            task = task.first()
            args = json.loads(task.args)
            args = args[0]

            for x in interests:
                if x not in args:
                    args.append(x)

            task.args = json.dumps([args])
            task.save()

        else:
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=15, period=IntervalSchedule.SECONDS
            )
            task = PeriodicTask.objects.create(
                interval=schedule,
                name="every-15-seconds",
                task="notifications.tasks.tagsTracker",
                args=json.dumps([interests])
            )

    @sync_to_async
    def delete_celery_beat(self):
        task = PeriodicTask.objects.filter(
            name="every-15-seconds", task="notifications.tasks.tagsTracker")
        if len(task) > 0:
            task.delete()

    """
    ASYNC Functions
    """
    async def connect(self):
        self.room_name = 'interest_tracker'
        self.room_group_name = 'tweet_interest_tracker'
        print(self.room_group_name)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # add to celery beat
        print('Creating')
        await self.add_celery_beat()
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.delete_celery_beat()

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                # type is the function that will actually
                # send the data to channels
                "type": "tweet_update",
                "message": message,
            },
        )

    # Receive message from room group
    async def send_tweet_update(self, event):
        message = event["message"]
        new_message = copy.copy(message)

        user_interests = await self.select_user_interests()
        keys = new_message.keys()

        # sending user specific data only
        for key in list(keys):
            if key in user_interests:
                pass
            else:
                del new_message[key]

        # Send message to WebSocket
        await self.send(text_data=json.dumps(new_message))
