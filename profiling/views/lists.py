from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from profiling.throttling import SetUserRateThrottle, custom_throttled
from profiling.models.profile import Profile
from profiling.serializers.list_serializer import (
    FavoriteSerializer,
    WatchlistSerializer,
    WatchedlistSerializer
)
from profiling.utils import media_key_check
from profiling.services.list_services import (profile_favoritelist_logic,
                                              profile_watchlist_logic,
                                              profile_watchedlist_logic)

# from django.utils.decorators import method_decorator

User = get_user_model()


class FavourtelistView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    throttle_classes = [SetUserRateThrottle]

    def throttled(self, request, wait):
        custom_throttled(self, request, wait)

    def get_queryset(self):
        user = self.request.user
        return Profile.objects.select_related('user').filter(user=user)

    @action(detail=True, methods=['PATCH'])
    def fav_toggle(self, request, pk=None):
        """Toggling Movie/TV shows from the Fav list

        ``
        id : Movie/TV instance ID in the URL
        ``

        Pass the key value pair of the media that has to be toggled

        If Movie instance has to be added then in form data,
        ``{'type':movies}``
        else for TV instance,
        ``{'type':tv_shows}``

        """
        type = self.request.data.get('type')
        user = self.request.user
        media_instance, key = media_key_check(pk, type)
        if media_instance and key:

            profile = Profile.objects.get(user=user)

            logic_response = profile_favoritelist_logic(
                profile, media_instance, key, user)
            return Response(logic_response[0], status=logic_response[1])

        return Response('Type is Invalid', status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['GET'])
    def get_favoritelist(self, request):
        profile = Profile.objects.get(user=self.request.user)
        return Response(FavoriteSerializer(profile).data)


class WatchlistView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    throttle_classes = [SetUserRateThrottle]

    def throttled(self, request, wait):
        custom_throttled(self, request, wait)

    def get_queryset(self):
        user = self.request.user
        return Profile.objects.select_related('user').filter(user=user)

    @action(detail=True, methods=['PATCH'])
    def watchlist_toggle(self, request, pk=None):
        """Toggling Movie/TV shows from the watch list

        ``
        id : Movie/TV instance ID in the URL
        ``

        Pass the key value pair of the media that has to be toggled

        If Movie instance has to be added then in form data, ``{'type':movie}``
        else for TV instance, ``{'type':tv_show}``

        """
        type = self.request.data.get('type')

        media_instance, key = media_key_check(pk, type)
        if media_instance and key:
            profile = Profile.objects.get(user=self.request.user)

            user = self.request.user
            logic_response = profile_watchlist_logic(
                profile, media_instance, key, user)
            return Response(logic_response[0], status=logic_response[1])

        return Response('Type is Invalid', status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['GET'])
    def get_watchlist(self, request, pk=None):
        profile = Profile.objects.get(user=self.request.user)
        return Response(WatchlistSerializer(profile).data)


class WatchedlistView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    throttle_classes = [SetUserRateThrottle]

    def throttled(self, request, wait):
        custom_throttled(self, request, wait)

    def get_queryset(self):
        user = self.request.user
        return Profile.objects.select_related('user').filter(user=user)

    @action(detail=True, methods=['PATCH'])
    def watchedlist_toggle(self, request, pk=None):
        """Toggling Movie/TV shows from the watched list

        ``
        id : Movie/TV instance ID in the URL
        ``

        Pass the key value pair of the media that has to be toggled

        If Movie instance has to be added then in form data, ``{'type':movie}``
        else for TV instance, ``{'type':tv_show}``

        """
        type = self.request.data.get('type')

        media_instance, key = media_key_check(pk, type)
        if media_instance and key:
            profile = Profile.objects.get(user=self.request.user)

            user = self.request.user
            logic_response = profile_watchedlist_logic(
                profile, media_instance, key, user)
            return Response(logic_response[0], status=logic_response[1])

        return Response('Type is Invalid', status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['GET'])
    def get_watchedlist(self, request, pk=None):
        profile = Profile.objects.get(user=self.request.user)
        return Response(WatchedlistSerializer(profile).data)
