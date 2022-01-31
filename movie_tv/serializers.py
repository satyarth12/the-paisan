from drf_queryfields import QueryFieldsMixin
from rest_framework import serializers

from .models import Movie, TV
from rating_review.models.rating import Rating
from rating_review.models.review import Review
from rating_review.serializers.review_serializers import ReviewListSerializer
from rating_review.serializers.rating_serializers import RatingListSerializer
from user.serializers import UserSerializer


class MovieListSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    ratings_count = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    favorites_count = serializers.SerializerMethodField()
    watch_list_count = serializers.SerializerMethodField()
    watched_list_count = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'name', "ratings_count", "reviews_count",
                  "favorites_count", "watch_list_count", "watched_list_count"]

    def get_ratings_count(self, obj):
        ratings = Rating.objects.filter_by_instance(obj)
        return ratings.count()

    def get_reviews_count(self, obj):
        reviews = Review.objects.filter_by_instance(obj)
        return reviews.count()

    def get_favorites_count(self, obj):
        return obj.favorites.count()

    def get_watch_list_count(self, obj):
        return obj.watch_list.count()

    def get_watched_list_count(self, obj):
        return obj.watched_list.count()


class TVListSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    ratings_count = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    favorites_count = serializers.SerializerMethodField()
    watch_list_count = serializers.SerializerMethodField()
    watched_list_count = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'name', "ratings_count", "reviews_count",
                  "favorites_count", "watch_list_count", "watched_list_count"]

    def get_ratings_count(self, obj):
        ratings = Rating.objects.filter_by_instance(obj)
        return ratings.count()

    def get_reviews_count(self, obj):
        reviews = Review.objects.filter_by_instance(obj)
        return reviews.count()

    def get_favorites_count(self, obj):
        return obj.favorites.count()

    def get_watch_list_count(self, obj):
        return obj.watch_list.count()

    def get_watched_list_count(self, obj):
        return obj.watched_list.count()


class MovieDetailSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()
    all_ratings = serializers.SerializerMethodField()
    all_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ["id", 'name', "avg_rating", "all_ratings", 'all_reviews',
                  "favorites", "watch_list", "watched_list"]

    def get_avg_rating(self, obj):
        try:
            s = 0
            ratings = Rating.objects.filter_by_instance(obj)
            stars = (i.stars for i in ratings)
            stars = list(stars)
            s = sum(stars)
            avg_rating = s/ratings.count()
            return avg_rating
        except Exception:
            return 0

    def get_all_ratings(self, obj):
        # returns rating instance
        ratings = Rating.objects.filter_by_instance(obj)
        return RatingListSerializer(ratings, many=True).data

    def get_all_reviews(self, obj):
        # returns review instance
        reviews = Review.objects.filter_by_instance(obj)
        return ReviewListSerializer(reviews, many=True).data

    def get_favorites(self, obj):
        # returns user ID
        return UserSerializer(obj.favorites, many=True).data

    def get_watch_list(self, obj):
        # returns user ID
        return UserSerializer(obj.watch_list, many=True).data

    def get_watched_list(self, obj):
        # returns user ID
        return UserSerializer(obj.watched_list, many=True).data


class TvDetailSeriazlier(QueryFieldsMixin, serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()
    all_ratings = serializers.SerializerMethodField()
    all_reviews = serializers.SerializerMethodField()

    class Meta:
        model = TV
        fields = ['id', 'name', "avg_rating", "all_ratings", 'all_reviews',
                  "favorites", "watch_list", "watched_list"]

    def get_avg_rating(self, obj):
        try:
            s = 0
            ratings = Rating.objects.filter_by_instance(obj)
            stars = (i.stars for i in ratings)
            stars = list(stars)
            s = sum(stars)
            avg_rating = s/ratings.count()
            return avg_rating
        except Exception:
            return 0

    def get_all_ratings(self, obj):
        # returns rating instance
        ratings = Rating.objects.filter_by_instance(obj)
        return RatingListSerializer(ratings, many=True).data

    def get_all_reviews(self, obj):
        # returns review instance
        reviews = Review.objects.filter_by_instance(obj)
        return ReviewListSerializer(reviews, many=True).data

    def get_favorites(self, obj):
        # returns user ID
        return UserSerializer(obj.favorites, many=True).data

    def get_watch_list(self, obj):
        # returns user ID
        return UserSerializer(obj.watch_list, many=True).data

    def get_watched_list(self, obj):
        # returns user ID
        return UserSerializer(obj.watched_list, many=True).data
