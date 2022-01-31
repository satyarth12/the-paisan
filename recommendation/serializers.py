from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from django.contrib.auth import get_user_model
import re

from .models import Recommendation
from user.serializers import UserSerializer
from movie_tv.serializers import TvDetailSeriazlier, MovieDetailSerializer
from movie_tv.models import Movie, TV
User = get_user_model()


def create_recommendation_serializer(model_type=None, object_id=None):

    class RecommendationCreateSerializer(serializers.ModelSerializer):
        item_recommended = serializers.SerializerMethodField()

        class Meta:
            model = Recommendation
            fields = ('id','from_user', 'to_user',
                      'item_recommended', 'timestamp',)
            
            read_only_fields = ['from_user',]
            ref_name = "Recommendation Create"

        def get_item_recommended(self, obj):
            dic = {
                'type': str(obj.content_type.model_class()),
                'pk': str(obj.object_id)
            }
            return dic
    
        def get_to_user(self, obj):
            return UserSerializer(obj.to_user).data

        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.object_id = object_id

            return super(RecommendationCreateSerializer, self).__init__(*args, **kwargs)

        def validate(self, data):
            model_type = self.model_type
            model_qs = ContentType.objects.filter(model=model_type)
            from_user = self.context['request'].user
            to_user = data.get('to_user')

            if not model_qs.exists() or model_qs.count() != 1:
                raise serializers.ValidationError(
                    "This is not a valid content type")

            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(id=self.object_id)

            if not obj_qs.exists() or obj_qs.count() != 1:
                raise serializers.ValidationError(
                    "This is not the id for this content type")

            if Recommendation.objects.filter(from_user=from_user,
                                             to_user=to_user,
                                             content_type=model_qs.first(),
                                             object_id=obj_qs.first().id).count() == 1:
                raise serializers.ValidationError('Item Already Exists')

            return data

        def create(self, validated_data):
            from_user = self.context['request'].user
            to_user = validated_data.get('to_user')
            model_type = self.model_type
            pk = self.object_id

            recommendation = Recommendation.objects.create_by_modeltype(
                model_type, pk, from_user, to_user)

            return recommendation

    return RecommendationCreateSerializer


class RecommendationListSerializer(serializers.ModelSerializer):
    # to_user = serializers.SerializerMethodField()
    item_recommended = serializers.SerializerMethodField()

    class Meta:
        model = Recommendation
        # 'content_type', 'object_id', 'parent',
        fields = ('id', 'from_user', 'to_user',
                  'item_recommended', 'timestamp')

    # def get_to_user(self, obj):
    #     curr_user = self.context['curr_user']
    #     return UserSerializer(obj.to_user,context={'curr_user':curr_user}).data

    def get_item_recommended(self, obj):
        try:
            try:
                if Movie.objects.get(id=obj.object_id):
                    return {'type':'movie', 'id': obj.object_id}
            except:
                if TV.objects.get(id=obj.object_id):
                    return {'type':'tv_show', 'id': obj.object_id}
        except:
            return 0
