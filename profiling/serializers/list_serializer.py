from drf_queryfields import QueryFieldsMixin
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from profiling.models.profile import Profile

from movie_tv.serializers import TVListSerializer, MovieListSerializer
from movie_tv.models import Movie, TV


class FavoriteSerializer(serializers.Serializer):
    """
    Serializer for performing on the favorite_list attr of Profile model
    """
    favorite_movies = serializers.SerializerMethodField()
    favorite_tv_shows = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['favorite_movies', 'favorite_tv_shows']

    def get_favorite_movies(self, obj):
        qs = []
        try:
            for movies in obj.favoritelist['movie']:
                qs.append(get_object_or_404(Movie, id=movies))
            return MovieListSerializer(qs, many=True).data
        except Exception:
            return 0

    def get_favorite_tv_shows(self, obj):
        qs = []
        try:
            for tv_shows in obj.favoritelist['tv_show']:
                qs.append(get_object_or_404(TV, id=tv_shows))
            return TVListSerializer(qs, many=True).data
        except Exception:
            return 0


class WatchlistSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    """
    Serializer for performing on the watch_list attr of Profile model
    """
    movie_watchlist = serializers.SerializerMethodField()
    tv_watchlist = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['movie_watchlist', 'tv_watchlist']

    def get_movie_watchlist(self, obj):
        qs = []
        try:
            for movies in obj.watchlist['movie']:
                qs.append(get_object_or_404(Movie, id=movies))
            return MovieListSerializer(qs, many=True).data
        except Exception:
            return 0

    def get_tv_watchlist(self, obj):
        qs = []
        try:
            for tv_shows in obj.watchlist['tv_show']:
                qs.append(get_object_or_404(TV, id=tv_shows))
            return TVListSerializer(qs, many=True).data
        except Exception:
            return 0


class WatchedlistSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    """
    Serializer for performing on the watched_list attr of Profile model
    """
    movie_watchedlist = serializers.SerializerMethodField()
    tv_watchedlist = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['movie_watchedlist', 'tv_watchedlist']

    def get_movie_watchedlist(self, obj):
        qs = []
        try:
            for movies in obj.watchedlist['movie']:
                qs.append(get_object_or_404(Movie, id=movies))
            return MovieListSerializer(qs, many=True).data
        except Exception:
            return 0

    def get_tv_watchedlist(self, obj):
        qs = []
        try:
            for tv_shows in obj.watchedlist['tv_show']:
                qs.append(get_object_or_404(TV, id=tv_shows))
            return TVListSerializer(qs, many=True).data
        except Exception:
            return 0
