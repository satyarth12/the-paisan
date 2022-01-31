"""
Module for the interest attribute of the profile model
"""

from profiling.validation import validate_user
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from profiling.models.profile import Profile
from profiling.services.interest_services import profile_interest_logic

User = get_user_model()


class InterestView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, ]

    @action(detail=True, methods=['PUT'])
    @method_decorator(validate_user)
    def toggle_interests(self, request, pk=None):
        """Toggling interests from the interests attr of the profile model

        ``
        id : ID of the user in the URL
        ``

        Pass the key value pair in the form-data

        ``
        {'interest_type': cast/genre/media},
        {'interest'}: Name of the intrests in list format,
                        example: name of the cast or name of the genre
        ``

        """

        key = request.data.get('interest_type')
        key = key.lower()

        interest = request.data.get('interest', [])
        interest = list(map(lambda x: x.lower(), interest.split(',')))
        print(interest)

        user = self.request.user
        profile = Profile.objects.get(user=user)

        if key == 'cast' or key == 'genre' or key == 'media':
            result = profile_interest_logic(
                profile=profile, key=key, interest_instance=interest)

            if result == 'updated':
                return Response("ADDED INTO INTEREST")
            elif result == 'exceeded':
                return Response("MAX 5 INTEREST ARE ALLOWED",
                                status=status.HTTP_409_CONFLICT)

        return Response('NOT A VALID INTEREST KEY',
                        status=status.HTTP_406_NOT_ACCEPTABLE)
