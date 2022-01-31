from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from django.contrib.auth import get_user_model

from rating_review.models.rating import Rating
User = get_user_model()


class RatingCreateSerializer(serializers.ModelSerializer):
    object_type = serializers.CharField(write_only=True)

    class Meta:
        model = Rating
        fields = ('id', 'user', "object_type",
                  "object_id", 'stars', 'created_on',)
        read_only_fields = [
            "user",
        ]
        ref_name = "Rating Create_Update"

    def validate(self, data):
        model_type = data.get('object_type')
        object_id = data.get('object_id')
        model_qs = ContentType.objects.filter(model=model_type)

        if not model_qs.exists() or model_qs.count() != 1:
            raise serializers.ValidationError(
                "This is not a valid content type")

        SomeModel = model_qs.first().model_class()
        obj_qs = SomeModel.objects.filter(id=object_id)

        if not obj_qs.exists() or obj_qs.count() != 1:
            raise serializers.ValidationError(
                "This is not the id for this content type")

        return data

    def create(self, validated_data):
        """
        This module'll check if the rating_instance is already present or not,
        If present then the instance will get updated with the received stars,
        else, a new instance will be created
        """
        stars = validated_data.get('stars')
        user = self.context["request"].user
        object_type = validated_data.get('object_type')
        model_type_id = validated_data.get('object_id')

        model = ContentType.objects.filter(model=object_type).first()
        rating_instance = Rating.objects.filter(
            user=user, content_type=model, object_id=model_type_id)

        if rating_instance.exists():
            rating_instance = rating_instance.first()
            rating_instance.stars = stars
            rating_instance.save()

            return rating_instance

        rating = Rating.objects.create_by_modeltype(
            model_type=object_type,
            pk=model_type_id,
            stars=stars,
            user=user)

        return rating


class RatingListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(source='user')

    class Meta:
        model = Rating
        # 'content_type', 'object_id', 'parent',
        fields = ('id', 'user', 'stars', 'created_on')

    def get_user(self, obj):
        return {
            'user_id': obj.user.id,
            'username': obj.user.username,
            'image': obj.user.profile.image_url

        }


class RatingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        # 'content_type', 'object_id',
        fields = ('id', 'user', 'stars', 'created_on', 'object_id')
        read_only_fields = ('object_id',)  # 'content_type', 'object_id',
