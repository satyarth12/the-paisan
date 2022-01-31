from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404  # permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from profiling.throttling import SetUserRateThrottle, custom_throttled
from profiling.validation import validate_user
from profiling.models.profile import Profile
from profiling.serializers.profile_serializer import (ProfileSerializer,)

User = get_user_model()


class ProfileViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    throttle_classes = [SetUserRateThrottle]
    http_method_names = ['put', 'delete', 'get', 'patch']

    def throttled(self, request, wait):
        custom_throttled(self, request, wait)

    def get_queryset(self):
        return Profile.objects.prefetch_related('user').all()

    @method_decorator(validate_user)
    def update(self, request, pk=None):
        """
        This module will get data from cache while updating
        the profile blob.
        """
        # user = self.request.user
        profile = get_object_or_404(Profile, id=pk)

        serializer_data = self.serializer_class(profile, data=request.data)
        if serializer_data.is_valid(raise_exception=True):
            serializer_data.save()

            return Response({'success': True,
                             'data': 'Profile Got Updated',
                             }, status=status.HTTP_200_OK)

        return Response({
            'success': False,
            'data': {
                'message': serializer_data.errors
            }
        }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    @ action(detail=False, methods=['GET'])
    def me(self, request):
        """
        This'll show the profile data of the current logged in user
        """
        user = self.request.user
        profile = Profile.objects.get(user=user)
        serializer_data = ProfileSerializer(profile).data
        return Response(serializer_data)
