from drf_queryfields import QueryFieldsMixin
from rest_framework import serializers
from profiling.models.profile import Profile
from user.serializers import UserSerializer


class ProfileSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    """
    Serializer for performing on the Profile model
    """
    # making the media model keys as global for increasing scope
    global all_media_keys
    all_media_keys = ['movie', 'tv_show']

    user = serializers.SerializerMethodField()
    interests = serializers.SerializerMethodField()
    favoritelist = serializers.SerializerMethodField()
    watchlist = serializers.SerializerMethodField()
    watchedlist = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ['id', 'user', 'my_connections']

    def get_user(self, obj):
        return UserSerializer(obj.user, context={'curr_user': obj.user}).data

    def get_interests(self, obj):
        try:
            return {
                'cast': [values for values in obj.interests['cast']],
                'genre': [values for values in obj.interests['genre']],
                # 'media': [values for values in obj.interests['media']],
            }
        except Exception:
            return {
                'cast': [],
                'genre': [],
                'media': [],
            }

    def get_favoritelist(self, obj):
        profile = Profile.objects.get(user=obj.user)
        d = {}

        try:
            """
            checking if the favlist keys are present in the global media key
            if yes then storing the id of that media
            else []
            """
            media_keys = [key for key in profile.favoritelist.keys()]
            for key in all_media_keys:
                if key in media_keys:
                    media_id = [id for id in profile.favoritelist[key]]
                else:
                    media_id = []
                d[key] = media_id
            return d
        except Exception:
            return {'movie': [], 'tv_show': []}

    def get_watchlist(self, obj):
        profile = Profile.objects.get(user=obj.user)
        d = {}

        try:
            """
            checking if the watchlist keys are present in the global media key
            if yes then storing the id of that media
            else []"""

            media_keys = [key for key in profile.watchlist.keys()]
            for key in all_media_keys:
                if key in media_keys:
                    media_id = [id for id in profile.watchlist[key]]
                else:
                    media_id = []
                d[key] = media_id
            return d
        except Exception:
            return {'movie': [], 'tv_show': []}

    def get_watchedlist(self, obj):

        profile = Profile.objects.get(user=obj.user)
        d = {}
        try:
            """
            checking if the watchedlist keys are present in the global
            media key, if yes then storing the id of that media
            else []"""
            media_keys = [key for key in profile.watchedlist.keys()]
            for key in all_media_keys:
                if key in media_keys:
                    media_id = [id for id in profile.watchedlist[key]]
                else:
                    media_id = []
                d[key] = media_id
            return d

        except Exception:
            return {'movie': [], 'tv_show': []}
