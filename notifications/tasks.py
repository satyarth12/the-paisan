from celery import shared_task
from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
from .models import Anouncement
import json
from celery.exceptions import Ignore
import asyncio

import concurrent.futures
from .twitter_bot import stream


@shared_task(bind=True)
def broadcast_announcement(self, data):
    print(data)
    try:
        notification = Anouncement.objects.filter(id=int(data))
        if len(notification) > 0:
            notification = notification.first()
            channel_layer = get_channel_layer()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(channel_layer.group_send(
                "user_notification",
                {
                    'type': 'send_announcement',
                    'message': json.dumps({'type': 'Superuser Announcement',
                                           'message': notification.message}),
                }))
            notification.sent = True
            notification.save()
            return 'Done'

        else:
            self.update_state(
                state='FAILURE',
                meta={'exe': "Not Found"}
            )

            raise Ignore()

    except Exception:
        self.update_state(
            state='FAILURE',
            meta={
                'exe': "Failed"
            }
        )

        raise Ignore()


# MAIN TASK
@shared_task(bind=True)
def tagsTracker(self, interest_tags):
    """
    Module for tracking data of the selected tags.
    """
    # tags = interest_tags  # list
    data = {}

    try:
        # using threadpool for concurrent scrapping of data
        with concurrent.futures.ThreadPoolExecutor(len(interest_tags)) as executor:
            result = executor.map(stream, [i for i in interest_tags])
            executor.shutdown(wait=True)

        final_result = list(result)
        for i in range(len(interest_tags)):
            data[interest_tags[i]] = final_result[i]

        print(data)

        # send data to the websocket group
        channel_layer = get_channel_layer()
        loop = asyncio.new_event_loop()

        asyncio.set_event_loop(loop)
        loop.run_until_complete(
            channel_layer.group_send(
                "tweet_interest_tracker",
                {
                    "type": "send_tweet_update",
                    "message": data,
                }
            )
        )

        return "Done"

    except Exception:
        self.update_state(
            state='FAILURE',
            meta={
                'exe': "Failed"
            }
        )

        raise Ignore()
