from django.conf import settings
from rest_framework import throttling
from rest_framework.exceptions import Throttled


class SetUserRateThrottle(throttling.UserRateThrottle):
    scope = 'user'
    rate = '10/day' if settings.INTERNAL_FEATURE_FLAGS['api_throttle'] else '1000/day'


def custom_throttled(self, request, wait):
    raise Throttled(detail={
        'success': False,
        'data': {
            'message': '''You are abusing this reporting feature.
                            Please slow down.'''
        }
    })
