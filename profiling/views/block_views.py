from rest_framework import generics, status
from rest_framework.response import Response
from profiling.serializers.block_serializer import BlockSerializer
from rest_framework import throttling
from rest_framework.exceptions import Throttled
from django.conf import settings


class SetUserRateThrottle(throttling.UserRateThrottle):
    scope = 'user'
    rate = '10/day' if settings.INTERNAL_FEATURE_FLAGS['api_throttle'] else '1000/day'


class BlockCreateView(generics.CreateAPIView):
    serializer_class = BlockSerializer
    throttle_classes = [SetUserRateThrottle]

    def throttled(self, request, wait):
        raise Throttled(detail={
            'success': False,
            'data': {
                'message': 'You are abusing this reporting feature. Please slow down.'
            }
        })

    def post(self, request, *args, **kwargs):
        # blocked_user = request.data.get('blocked_user')
        data = request.data
        serializer = self.serializer_class(
            data=data, context={'request': self.request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                'success': True,
                'data': 'User Blocked',
            }, status=status.HTTP_200_OK)

        return Response({
            'success': False,
            'data': {
                'message': serializer.errors
            }
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
