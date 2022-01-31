from rest_framework import generics
from rest_framework.response import Response
from profiling.serializers.report_serializer import ReportCreateSerializer
from rest_framework import status
from rest_framework import throttling
from rest_framework.exceptions import Throttled
from django.conf import settings


class SetUserRateThrottle(throttling.UserRateThrottle):
    scope = 'user'
    rate = '10/day' if settings.INTERNAL_FEATURE_FLAGS['api_throttle'] else '1000/day'


class ReportCreateView(generics.CreateAPIView):
    throttle_classes = [SetUserRateThrottle]
    serializer_class = ReportCreateSerializer

    def throttled(self, request, wait):
        raise Throttled(detail={
            'success': False,
            'data': {
                'message': 'You are abusing this reporting feature. Please slow down.'
            }
        })

    def post(self, request):
        data = request.data
        # data._mutable = True

        serializer = self.serializer_class(
            data=data, context={'request': self.request})

        if serializer.is_valid(raise_exception=True):
            resp = serializer.save()

            # # to show response if the user gets autoblocked
            # if resp.__class__.__name__ == 'Block':
            #     return Response({
            #         'success': True,
            #         'data': 'User Blocked because of more than 5 reports',
            #     }, status=status.HTTP_200_OK)

            return Response({
                'success': True,
                'data': 'User reported',
            }, status=status.HTTP_200_OK)

        return Response({
            'success': False,
            'data': {
                'message': serializer.errors
            }
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
